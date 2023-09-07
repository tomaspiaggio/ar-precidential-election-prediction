from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import expr, col
import requests

# Create a Spark session
spark = SparkSession.builder \
    .appName("SentimentAnalysis") \
    .getOrCreate()

# Define the ClickHouse source configuration
clickhouse_options = {
    "url": "jdbc:clickhouse://<clickhouse-host>:<clickhouse-port>/<database>",
    "driver": "ru.yandex.clickhouse.ClickHouseDriver",
    "dbtable": "<clickhouse-table>",
    "user": "<username>",
    "password": "<password>"
}

# Read data from ClickHouse using readStream
clickhouse_stream = spark.readStream \
    .format("jdbc") \
    .option("url", clickhouse_options["url"]) \
    .option("driver", clickhouse_options["driver"]) \
    .option("dbtable", clickhouse_options["dbtable"]) \
    .option("user", clickhouse_options["user"]) \
    .option("password", clickhouse_options["password"]) \
    .load()

# Define a function to make an HTTP call using requests library
def make_http_call(rows):
    for row in rows:
        # Extract the necessary data from the ClickHouse DataFrame
        message = row.message

        # Make the HTTP call and get the response
        response = requests.get("sentiment:3000", params={"to_predict": message})

        # Create a new DataFrame with the response and matching ID
        result_df = spark.createDataFrame([(row.id, row.message, response["score"], response["label"])],
                                          ["id", "message", "sentiment_score", "sentiment_label"])

        yield result_df

# Use mapPartition to apply the HTTP call function to the ClickHouse stream
http_result_stream = clickhouse_stream.where(col("is_milei") | col("is_massa") | col("is_bullrich")) \
    .rdd \
    .mapPartitions(make_http_call) \
    .toDF()

# Write the results to a new ClickHouse table
http_result_stream.writeStream \
    .format("jdbc") \
    .option("url", clickhouse_options["url"]) \
    .option("driver", clickhouse_options["driver"]) \
    .option("dbtable", "<new-clickhouse-table>") \
    .option("user", clickhouse_options["user"]) \
    .option("password", clickhouse_options["password"]) \
    .start()

# Start the streaming job
spark.streams.awaitAnyTermination()


from pyspark.sql import SparkSession

# Define your ClickHouse JDBC URL
clickhouse_url = "jdbc:clickhouse://clickhouse:8123/messages"

# Set up the Spark session
spark = SparkSession.builder \
    .appName("ClickHouseDataRead") \
    .config("spark.jars", "./lib/clickhouse-jdbc-0.2.4.jar") \
    .getOrCreate()

# Define your connection properties
connection_properties = {
    "user": "clickhouse-user",
    "password": "secret",
    "driver": "ru.yandex.clickhouse.ClickHouseDriver"
}

# Define the table you want to read from
table_name = "messages"

# Read data from ClickHouse
clickhouse_data = spark.read.jdbc(
    url=clickhouse_url,
    table=table_name,
    properties=connection_properties
)

# You can now perform operations on the clickhouse_data DataFrame
clickhouse_data.show()
