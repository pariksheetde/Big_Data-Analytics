import sys
from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.sql.types import *
from pyspark.sql.window import Window
from pyspark.sql.types import DateType
from pyspark.sql.functions import *


if __name__ == "__main__":
    print("Churn Modelling")

# set the SparkSession
churn_df = SparkSession.builder.appName("Churn Modeling").master("local[3]").getOrCreate()

# read the datafile from the location
churn = churn_df.read.csv(r"D:\Code\DataSet\SparkDataSet\ChurnModeling.csv", inferSchema=True, header=True)
churn.show(5, truncate=False)

# select the required columns
churn = churn.selectExpr("CustomerId", "Surname", "CreditScore", "Geography", "Gender", "Age", "Tenure") \
    .filter((churn.Geography == "France") & (churn.Gender == "Male")) \
    .where(churn.Age >= 18) \
    .orderBy(asc("Age"))

# \
# .where(churn.Geography == "France") \
#     .groupBy("Geography", "Gender") \
#     .agg(avg("Age").alias("Avg_Age")) \
#

churn.show(15)
print(f'Records effected: {churn.count()}')
