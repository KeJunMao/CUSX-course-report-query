import threading
import requests
import hashlib
from bs4 import BeautifulSoup
import re
import time
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
load_dotenv()


Base = declarative_base()
engine = create_engine(os.environ.get("DB_PATH"))
baseUrl = os.getenv('BASE_URL')
Session = sessionmaker(bind=engine)
session = Session()


class Course(Base):
    __tablename__ = 'course'

    username = Column(String(10), primary_key=True)  # 学号
    password = Column(String(16))  # 密码
    realyname = Column(String(16))  # 姓名
    semester = Column(Integer)  # 学期
    course_report = Column(TEXT)  # 课程名

    def check_existing(self):
        existing = session.query(Course).filter_by(
            username=self.username).first()
        if not existing:
            course = self
        else:
            course = existing
        session.close()
        return course


Base.metadata.create_all(engine)


class User:
    def __init__(self, username, password, evaluate=True, force_update=False):
        self.username = username
        self.password = password
        self.evaluate = evaluate  # 是否评教
        self.force_update = force_update  # 是否强制更新
        self.isLogin = False
        self.name = ""
        self.hashPassword = ""
        self.cookies = None
        self.semester = os.getenv('SEMESTER')
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://172-18-2-55.vpn.arft.net:8118/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def getTotal(self, source_list):
        count = 0.0

        for s in source_list:
            if (s['成绩'] < 60):
                print(f"{self.name} - {s['名称']}挂科: {s['成绩']}")

            count += s['成绩']
        return count

    def getSource(self):
        if self.isLogin:
            source = requests.get(
                f"{baseUrl}/eams/teach/grade/course/person!search.action?semesterId={self.semester}", cookies=self.cookies, headers=self.headers)
            soup = BeautifulSoup(source.text, 'html.parser')
            if soup.text.find('完成本学期评教后再查看成绩') != -1 and self.evaluate:
                self.stdEvaluate()
                return self.getSource()
            data_list = []
            for idx, tr in enumerate(soup.find_all('tr')):
                if idx != 0:
                    tds = tr.find_all('td')
                    if len(tds) >= 3 and tds[3].text:
                        name = tds[3].text
                        data_list.append({
                            "名称": ''.join(name.split()),
                            "成绩": float(tds[7].string.strip())
                        })
            if len(data_list) > 0:
                course = Course(username=self.username, password=self.password,
                                realyname=self.name, semester=self.semester, course_report=json.dumps(data_list))
                course = course.check_existing()
                session.add(course)
                session.commit()

            return data_list
        else:
            print(f"{self.username}: 账号或密码错误")
            return []

    def stdEvaluate(self):
        source = requests.get(
            f"{baseUrl}/eams/quality/stdEvaluate.action", cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(source.text, 'html.parser')
        for idx, tr in enumerate(soup.find_all('tr')):
            if idx != 0:
                td = tr.find_all('td')[-1]
                alinks = td.find_all('a')
                for a in alinks:
                    param = a['href'].split('?')[-1].split('&')
                    evaluationLesson = param[0].split('=')[-1]
                    teacher = param[1].split('=')[-1]
                    formData = {
                        'teacher.id': teacher,
                        'semester.id': self.semester,
                        'evaluationLesson.id': evaluationLesson,
                        'result1_0.questionName': '作业（理论课、实践课）批改认真、注重讲评',
                        'result1_0.content': 'A',
                        'result1_0.score': 0.05500000000000001,
                        'result1_1.questionName': '能针对学生特点，因材施教',
                        'result1_1.content': 'A',
                        'result1_1.score': 0.05500000000000001,
                        'result1_2.questionName': '仪表端正，教态大方，为人师表',
                        'result1_2.content': 'A',
                        'result1_2.score': 0.05500000000000001,
                        'result1_3.questionName': '教学目的明确，符合大纲要求',
                        'result1_3.content': 'A',
                        'result1_3.score': 0.05500000000000001,
                        'result1_4.questionName': '教材掌握熟练，观点正确，概念准确内容充实，有一定的深度和广度',
                        'result1_4.content': 'A',
                        'result1_4.score': 0.05500000000000001,
                        'result1_5.questionName': '重点、难点突出能反映本学科发展趋势，将最新理论与研究成果融于教学',
                        'result1_5.content': 'A',
                        'result1_5.score': 0.05500000000000001,
                        'result1_6.questionName': '课堂内容衔接紧密，用正确的方法指导学生领会；注重理论联系实际',
                        'result1_6.content': 'A',
                        'result1_6.score': 0.05500000000000001,
                        'result1_7.questionName': '理论教学板书规范合理；实践教学示范准确；讲课语言表达简洁生动准确',
                        'result1_7.content': 'A',
                        'result1_7.score': 0.05500000000000001,
                        'result1_8.questionName': '在完成教学任务的前提下教学效果好',
                        'result1_8.content': 'A',
                        'result1_8.score': 0.06,
                        'result1Num': 9,
                        'result2Num': 0,
                    }
                    time.sleep(float(os.getenv('SLEEP')))
                    requests.post(f"{baseUrl}/eams/quality/stdEvaluate!finishAnswer.action",
                                  cookies=self.cookies, data=formData)

    def login(self):
        r = self.getHtml()
        self.cookies = {
            'JSESSIONID': r.cookies.get('JSESSIONID'),
            'TWFID': os.getenv('TWFID'),
            'GSESSIONID': r.cookies.get('GSESSIONID'),
        }
        self.hashPassword = self.getShaPassword(r)
        formData = {
            "username": self.username,
            "password": self.hashPassword,
            "encodedPassword": "",
            "session_locale": "zh_CN"
        }
        time.sleep(float(os.getenv('SLEEP')))
        user = requests.post(f"{baseUrl}/eams/login.action",
                             cookies=self.cookies, data=formData, headers=self.headers)
        soup = BeautifulSoup(user.text, 'html.parser')
        c = soup.find('a', {"href": '/eams/security/my.action'})
        if c:
            self.isLogin = True
            self.name = c.string

    def getHtml(self):
        r = requests.get(f"{baseUrl}/eams/login.action",
                         headers=self.headers, cookies=self.cookies)
        return r

    def getCookies(self, r):
        return r.cookies

    def getShaPassword(self, r):
        soup = BeautifulSoup(r.text, 'html.parser')
        pattern = re.compile(r"CryptoJS.SHA1\(\'(.*?)\'")
        script = soup.find("script", text=pattern)
        shabasetext = pattern.search(str(script)).group(1)
        hash_object = hashlib.sha1(str.encode(shabasetext + self.password))
        return hash_object.hexdigest()

    def do(self):
        if self.force_update:
            self.login()
            return self.getSource()
        else:
            course = session.query(Course).filter_by(
                username=self.username, semester=self.semester).first()
            if course is None:
                self.login()
                return self.getSource()
            else:
                self.isLogin = True
                self.name = course.realyname
                return json.loads(course.course_report)


def keeplive():
    test_user = User(
        username='2020202020',
        password='2020202020', force_update=True
    )
    test_user.getHtml()


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


if os.getenv('KEEPLIVE') == '1':
    set_interval(keeplive, 20)
