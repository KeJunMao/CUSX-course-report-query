from User import User
import pyperclip

force_update = False

while True:
    text = ""
    inputvalue = input("请输入学号和密码：").split()
    if len(inputvalue) == 0:
        continue
    if len(inputvalue) == 1:
        username = inputvalue[0]
        password = username
    elif len(inputvalue) == 2:
        username, password = inputvalue
        if password == '--force':
            force_update = True
            password = username
    elif len(inputvalue) == 3:
        username, password, force_flag = inputvalue
        if force_flag == '--force':
            force_update = True
            password = password
    if username == "q":
        break
    if len(username) != 10:
        print("Invalid username")
        continue
    user = User(username, password, True, force_update)
    source = user.do()
    if not user.isLogin:
        continue
    total = user.getTotal(source)
    text += f"{user.username} - 总成绩: {total:.2f} 平均成绩: {total / len(source) if len(source) > 0 else 1:.2f}\n"
    # text += f"{user.name} - 总成绩: {total:.2f} 平均成绩: {total / len(source) if len(source) > 0 else 1:.2f}\n"
    for s in source:
        text += f"\t {s['名称']}: {s['成绩']}\n"
    text += "\n有时候发不出消息，收到回复下，另外空间说说第一条，大学生创业！扫一下！拜托了这对我真的很重要！"
    print(text)
    pyperclip.copy(text)
    force_update = False
