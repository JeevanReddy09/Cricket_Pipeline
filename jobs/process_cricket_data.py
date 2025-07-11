# jobs/process_cricket_data.py

import sys
from pyspark.sql import SparkSession #type: ignore
from pyspark.sql.functions import col, to_date, when #type: ignore
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, LongType #type: ignore

def run_spark_job(spark, input_path, output_path):
    """
    Reads cricket data from GCS, flattens it, and writes it back to GCS
    as non-partitioned Parquet files.
    """
    # Using a defined schema is still a best practice for speed and reliability
    defined_schema = StructType([
        StructField("city", StringType(), True),
        StructField("dates", ArrayType(StringType()), True),
        StructField("gender", StringType(), True),
        StructField("match_type", StringType(), True),
        StructField("outcome", StructType([
            StructField("winner", StringType(), True),
            StructField("result", StringType(), True),
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
        StructField("venue", StringType(), True),
        StructField("event", StructType([
            StructField("name", StringType(), True),
            StructField("match_number", LongType(), True)
        ]), True)
    ])

    raw_df = spark.read.schema(defined_schema).option("multiLine", "true").json(input_path)

    # Flatten the DataFrame
    final_df = raw_df.select(
        "city",
        col("dates")[0].alias("match_date_str"), # Read as a string first
        "gender",
        "match_type",
        col("outcome.winner").alias("winner"),
        col("outcome.result").alias("result"),
        col("outcome.by.runs").alias("win_by_runs"),
        col("outcome.by.wickets").alias("win_by_wickets"),
        "overs",
        col("player_of_match")[0].alias("player_of_match"),
        col("teams")[0].alias("team_1"),
        col("teams")[1].alias("team_2"),
        col("toss.decision").alias("toss_decision"),
        col("toss.winner").alias("toss_winner"),
        "venue",
        col("event.name").alias("event_name")
    )

    # Add outcome_type column based on win_by_runs and win_by_wickets
    final_df = final_df.withColumn(
        "outcome_type",
        when(col("win_by_runs").isNotNull(), "runs")
        .when(col("win_by_wickets").isNotNull(), "wickets")
        .otherwise(None)
    )

    # Convert match_date string to a proper DateType column
    final_df = final_df.withColumn("match_date", to_date(col("match_date_str"))).drop("match_date_str")

    # Write the final data to GCS in Parquet format
    final_df.write.mode("overwrite").parquet(output_path)


if __name__ == "__main__":
    # We only need input and output paths now
    if len(sys.argv) != 3:
        print("Usage: spark-submit script.py <input_gcs_path> <output_gcs_path>")
        sys.exit(-1)

    spark = SparkSession.builder.appName("Cricsheet_JSON_to_Parquet_Final").getOrCreate()

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    run_spark_job(spark, input_path, output_path)

    spark.stop()
