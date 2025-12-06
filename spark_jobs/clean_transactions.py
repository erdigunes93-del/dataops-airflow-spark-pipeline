from pyspark.sql import SparkSession

# -------------------------
# Spark Session
# -------------------------
spark = SparkSession.builder \
    .appName("CleanStoreTransactions") \
    .getOrCreate()

# -------------------------
# MinIO (S3A) Config
# -------------------------
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.endpoint", "http://minio:9000")
hadoop_conf.set("fs.s3a.access.key", "dataopsadmin")
hadoop_conf.set("fs.s3a.secret.key", "dataopsadmin")
hadoop_conf.set("fs.s3a.path.style.access", "true")
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# -------------------------
# Read from MinIO (Bronze)
# -------------------------
input_path = "s3a://dataops-bronze/raw/dirty_store_transactions.csv"

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(input_path)

print(f"Raw count: {df.count()}")

# -------------------------
# Cleaning
# -------------------------
df_clean = (
    df
    .dropDuplicates()
    .dropna()
)

print(f"Clean count: {df_clean.count()}")

# -------------------------
# Write to PostgreSQL
# -------------------------
jdbc_url = "jdbc:postgresql://postgres:5432/traindb"

df_clean.write \
    .mode("overwrite") \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "public.clean_data_transactions") \
    .option("user", "train") \
    .option("password", "train") \
    .option("driver", "org.postgresql.Driver") \
    .save()

spark.stop()

