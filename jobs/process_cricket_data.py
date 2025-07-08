import sys
from pyspark.sql import SparkSession #type: ignore
from pyspark.sql.functions import col, year as get_year, lit #type: ignore
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, LongType #type: ignore

def run_spark_job(spark, input_path, output_path, match_type):
   
    defined_schema = StructType([
        StructField("city", StringType(), True),
        StructField("dates", ArrayType(StringType()), True),
        StructField("event", StructType([
            StructField("name", StringType(), True),
            StructField("match_number", LongType(), True)
        ]), True),
        StructField("gender", StringType(), True),
        StructField("match_type", StringType(), True),
        StructField("outcome", StructType([
            StructField("winner", StringType(), True),
            StructField("by", StructType([
                StructField("runs", LongType(), True),
                StructField("wickets", LongType(), True)
            ]), True)
        ]), True),
        StructField("overs", StringType(), True),
        StructField("player_of_match", ArrayType(StringType()), True),
        StructField("teams", ArrayType(StringType()), True),
        StructField("toss", StructType([
            StructField("decision", StringType(), True),
            StructField("winner", StringType(), True)
        ]), True),
        StructField("venue", StringType(), True)
    ])

    raw_df = spark.read.schema(defined_schema).option("multiLine", "true").json(input_path)

    final_df = raw_df.select(
        "city",
        col("dates")[0].alias("match_date"),
        col("event.name").alias("event_name"),
        "gender",
        col("match_type").alias("match_type_detail"),
        col("outcome.winner").alias("winner"),
        col("outcome.by.wickets").alias("win_by_wickets"),
        col("outcome.by.runs").alias("win_by_runs"),
        "overs",
        col("player_of_match")[0].alias("player_of_match"),
        col("teams")[0].alias("team_1"),
        col("teams")[1].alias("team_2"),
        col("toss.decision").alias("toss_decision"),
        col("toss.winner").alias("toss_winner"),
        "venue"
    )

    # Add partition columns
    partitioned_df = final_df.withColumn("year", get_year(col("match_date"))) \
                             .withColumn("match_type", lit(match_type)) # <-- THIS LINE IS UPDATED

    partitioned_df.write.partitionBy("match_type", "year").mode("overwrite").parquet(output_path)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: spark-submit script.py <input_gcs_path> <output_gcs_path> <match_type>")
        sys.exit(-1)

    spark = SparkSession.builder.appName("Cricsheet_JSON_to_Parquet").getOrCreate()

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    match_type = sys.argv[3] # Get the match type from the third argument

    run_spark_job(spark, input_path, output_path, match_type)

    spark.stop()