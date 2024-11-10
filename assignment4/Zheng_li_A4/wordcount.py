from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col
import sys

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: wordcount.py <input_file> <output_file>")
        sys.exit(-1)
    
    # Get command-line arguments: input and output paths
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Create SparkSession
    spark = SparkSession.builder \
        .appName("Word Count Application") \
        .getOrCreate()
    
    # Read the input file from HDFS
    text_df = spark.read.text(input_path)
    
    # Split words by whitespace without removing punctuation
    word_counts = text_df \
        .select(explode(split(col("value"), "\\s+")).alias("word")) \
        .groupBy("word") \
        .count() \
        .orderBy(col("count").desc())
    
    # Write the result to HDFS in CSV format
    word_counts.write.csv(output_path, header=True)
    
    # Stop SparkSession
    spark.stop()

if __name__ == "__main__":
    main()