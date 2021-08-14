from sqlalchemy import create_engine
import os
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.environ.get("DB_PATH"))


def get_rank_info(username):
    course = pd.read_sql('course', engine)
    course["course_report"] = course["course_report"].apply(json.loads)

    for index, row in course.iterrows():
        course_report = map(lambda x: x['成绩'], row["course_report"])
        course.loc[index, "total"] = sum(course_report)

    course = course.drop(["course_report", "semester"], axis=1)

    course['rank'] = course['total'].rank(ascending=False)
    rank_info = {
        "total_users": 1,
        "ranking": 0,
    }
    if len(username) != 10:
        return rank_info
    users = course[course['username'].str.contains(
        username[:-2], regex=False)].copy()
    users['rank'] = users['total'].rank(ascending=False)

    rank_info['total_users'] = len(users)
    rank = users[users['username'] == username]['rank'].values
    if len(rank) != 0:
        rank_info['ranking'] = rank[0]
    return rank_info
