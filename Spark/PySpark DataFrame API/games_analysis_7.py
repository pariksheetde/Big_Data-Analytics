import sys
from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.sql.types import *
from pyspark.sql.types import DateType
from pyspark.sql.functions import *
from pyspark.sql.window import Window


if __name__ == "__main__":
    print("Games Analysis")

# set the SparkSession
spark = SparkSession.builder.appName("Games Analysis").master("local[3]").getOrCreate()

games = spark.read.csv(r"D:\Code\DataSet\SparkDataSet\NHL\game.csv", inferSchema=True, header=True)
games.show(5, truncate=False)

# drop unwanted columns from the DF
games = games.drop("date_time_GMT", "away_team_id", "home_team_id", "venue_link", "venue_time_zone_id", "venue_time_zone_offset", "venue_time_zone_tz")

# select the required columns
games_sel = games.selectExpr("game_id", "season", "type", "away_goals", "home_goals",
                         "venue", "outcome", "home_rink_side_start") \
                 .filter(games.type != "P") \
                 .where("home_rink_side_start in ('right', 'left')") \
                 .where("away_goals >= 6 and away_goals > home_goals")

games_agg = games_sel.select("game_id", "season", "venue", "type", "away_goals", "home_goals", "outcome",
                             "home_rink_side_start",
                             f.substring("season", 1, 4).alias("start_season"),
                             f.substring("season", 5, 8).alias("end_season")
                             )

games_agg = games_agg.select("game_id", "season", "venue", "type", "away_goals", "home_goals", "outcome","start_season", "end_season",
                             rank().over(Window.partitionBy('season').orderBy(asc("game_id"))).alias("rank")
                            )

games_win = games_agg.select("game_id", "season", "venue", "type", "away_goals", "home_goals", "outcome","start_season", "end_season", "rank") \
                     .filter(games_agg.rank == 1) \
                     .filter(games_agg.outcome.startswith('away'))

games_win.show(500, truncate=False)
print(f"Records Effected: {games_win.count()}")
print(f"Number of partition: {games_win.rdd.getNumPartitions()}")