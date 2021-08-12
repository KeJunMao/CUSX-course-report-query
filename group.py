import os
from User import User

prefix = input("请输入学号前8位：")
if len(prefix) != 8:
    print("请输入正确的学号前8位")
    os.exit(1)

count = int(input("请输入班级人数：")) + 1

all_user = []
ignore_password_check = False

for i in range(1, count):
    username = f"{prefix}{i:2d}".replace(" ", '0')
    password = username
    if not ignore_password_check:
        flag = input(f"请确认学号密码({username,password})：")
        if flag == '--ignore' or flag == '-i':
            ignore_password_check = True
        elif flag != '':
            password = flag

    user = User(username, password)
    print(f"正在登录{username,password}，请稍等...")
    user.login()
    source = user.getSource()
    total = user.getTotal(source)
    all_user.append({
        "name": user.name if user.name else user.username,
        "source": source,
        "total": total,
        "avg": total / len(source) if len(source) > 0 else 1
    })

all_user.sort(key=lambda x: x['total'], reverse=True)
print("---------------------------")
for idx, u in enumerate(all_user):
    print(f"{u['name']} - 总成绩: {u['total']} 平均成绩: {u['avg']:.2f} 第 {idx+1} 名")
    for s in u['source']:
        print(f"\t {s['名称']}: {s['成绩']}")
    print("---------------------------")
