from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize a SparkSession
spark = SparkSession.builder.appName("FilterAndSplit").getOrCreate()

# Assuming 'df' is your PySpark DataFrame
jxc_words = ["pato", "patricia", "bullrich", "jxc", "macri", "larreta", "pelado", "jorge"]
lla_words = ["libertad", "milei", "piparo", "villarruel", "javier", "leon"]
k_words = ["cristina", "kirchner", "fernandez", "massa", "sergio", "tomas", "kicillof", "alberto"]

jxc_condition = col("message").rlike("|".join(jxc_words))
lla_condition = col("message").rlike("|".join(lla_words))
k_condition = col("message").rlike("|".join(k_words))

jxc_df = df.filter(jxc_condition).drop("message")
lla_df = df.filter(lla_condition).drop("message")
k_df = df.filter(k_condition).drop("message")

# Don't forget to stop the SparkSession when you're done
spark.stop()


from pyspark.sql import SparkSession

# Define your ClickHouse JDBC URL
clickhouse_url = "jdbc:clickhouse://clickhouse:8123/messages"

# Set up the Spark session
spark = SparkSession.builder \
    .appName("ClickHouseDataRead") \
    .config("spark.jars", "/path/to/clickhouse-jdbc-driver.jar")  # Provide the path to the ClickHouse JDBC driver JAR
.getOrCreate()

# Define your connection properties
connection_properties = {
    "user": "<clickhouse_username>",
    "password": "<clickhouse_password>",
    "driver": "ru.yandex.clickhouse.ClickHouseDriver"
}

# Define the table you want to read from
table_name = "<clickhouse_table>"

# Read data from ClickHouse
clickhouse_data = spark.read \
    .jdbc(url=clickhouse_url, table=table_name, properties=connection_properties)

# You can now perform operations on the clickhouse_data DataFrame
clickhouse_data.show()

# Stop the Spark session when you're done
spark.stop()
