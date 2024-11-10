from pyspark.sql import SparkSession 
from pyspark.sql.functions import col, lit, sum as sql_sum, count
import sys

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: pagerank_app.py <input_file> <output_file>")
        sys.exit(-1)
    
    # Get command line arguments
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Create SparkSession
    spark = SparkSession.builder.appName("PageRank DataFrame Application").getOrCreate()
    
    # Read input file and ensure it has two columns (from, to), filtering out comment lines
    edges_df = spark.read.csv(input_path, sep="\t", inferSchema=True, comment="#").toDF("from", "to")
    
    # Repartition to improve parallelism
    edges_df = edges_df.repartition("from") # or: .repartition(4)
    
    # Cache edges_df and trigger caching
    edges_df.cache()
    edges_df.count()  # Trigger the cache
    
    
    # Compute out_degree_df and cache it
    out_degree_df = edges_df.groupBy("from").agg(count("to").alias("out_degree"))
    out_degree_df = out_degree_df.repartition("from") # or: edges_df = edges_df.repartition(4)
    out_degree_df.cache()
    out_degree_df.count()  # Trigger the cache
    
    
    # Initialize ranks_df with rank 1.0 for each unique page
    ranks_df = edges_df.select(col("from").alias("id")).union(edges_df.select(col("to").alias("id"))).distinct() \
                       .withColumn("rank", lit(1.0))
    
    # Repartition ranks_df
    ranks_df = ranks_df.repartition("id") # or: .repartition(4)
    print("Initialized ranks_df")
    
    # Iterate PageRank algorithm
    for i in range(10):
        
        
        # Join edges_df with out_degree_df
        edges_with_degree = edges_df.alias("e").join(out_degree_df.alias("o"), col("e.from") == col("o.from")) \
            .select(col("e.from"), col("e.to"), col("o.out_degree"))
        
        # Repartition edges_with_degree
        edges_with_degree = edges_with_degree.repartition("from") # or: .repartition(4)
        
        # Compute contributions
        contributions_df = edges_with_degree.join(ranks_df.alias("r"), col("from") == col("r.id")) \
            .select(col("to").alias("id"), (col("r.rank") / col("out_degree")).alias("contribution"))
        
        # Repartition contributions_df
        contributions_df = contributions_df.repartition("id") # or: .repartition(4)
        
        # Update ranks_df
        ranks_df = contributions_df.groupBy("id").agg(sql_sum("contribution").alias("sum_contribution")) \
            .withColumn("rank", 0.15 + 0.85 * col("sum_contribution")) \
            .select("id", "rank")
        
        # Repartition ranks_df
        ranks_df = ranks_df.repartition("id") # or: .repartition(4)
        
    
    # Save the results using overwrite mode
    ranks_df.write.mode("overwrite").csv(output_path, header=True)
    
    
    # Stop SparkSession
    spark.stop()

if __name__ == "__main__":
    main()