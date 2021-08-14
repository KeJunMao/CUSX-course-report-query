from sqlalchemy import create_engine
import os
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ.get("DB_PATH"))

df = pd.read_sql('course', engine)

df["course_report"] = df["course_report"].apply(json.loads)


for index, row in df.iterrows():
    for item in row["course_report"]:
        df.loc[index, item['名称']] = item['成绩']

df = df.drop(["course_report", "semester"], axis=1)


df = df.describe(exclude=[object])
df = df.drop(["std", "25%", "50%", "75%"])

df = df.T

df.rename(columns={"count": "人数", "mean": "平均分",
          'max': '最高分', 'min': "最低分"}, inplace=True)

df.to_csv("analyze.csv")
