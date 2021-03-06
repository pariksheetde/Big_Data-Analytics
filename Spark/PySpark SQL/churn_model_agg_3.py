import sys
from pyspark.sql import *
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import pyspark.sql.functions


if __name__ == "__main__":
    print("Churn Modelling")

# set the SparkSession
spark = SparkSession.builder.appName("Churn Modeling").master("local[3]").getOrCreate()

# read the datafile from the location
churn = spark.read.csv(r"D:\Code\DataSet\SparkDataSet\ChurnModeling.csv", inferSchema=True, header=True)
churn.show(5, truncate=False)

# select the required columns
churn_agg = churn.createOrReplaceTempView("Churn_Agg")

spark.sql("""select Geography,
                    Gender,
                    round(avg(Age),2) as Age
                    from 
                    Churn_Agg
                    group by Geography, Gender
                    """)\
    .show(5)
