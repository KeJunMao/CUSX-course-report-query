from User import User
import pyperclip

while True:
    text = ""
    inputvalue = input("请输入学号和密码：").split()
    if len(inputvalue) == 2:
        username, password = inputvalue
    else:
        username = inputvalue[0]
        password = username
    if username == "q":
        break
    print(f"正在登录{username,password}，请稍等...")
    user = User(username, password, False)
    user.login()
    source = user.getSource()
    if not user.isLogin:
        continue
    total = user.getTotal(source)
    text += f"{user.name} - 总成绩: {total} 平均成绩: {total / len(source) if len(source) > 0 else 1:.2f}\n"
    for s in source:
        text += f"\t {s['名称']}: {s['成绩']}\n"
    text += "\n不用谢我，如果可以的话，空间说说第一条，大学生创业！扫一下或者转发一下都可以鸭！拜托了这对我真的很重要！"
    print(text)
    pyperclip.copy(text)
