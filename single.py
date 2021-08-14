from User import User
import pyperclip
from ranking import get_rank_info

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
    rank_info = get_rank_info(user.username)
    text += f"{user.username} - 总成绩: {total:.2f} 平均成绩: {total / len(source) if len(source) > 0 else 1:.2f} 排名：{rank_info['ranking']:.0f}/{rank_info['total_users']} \n"
    # text += f"{user.name} - 总成绩: {total:.2f} 平均成绩: {total / len(source) if len(source) > 0 else 1:.2f}\n"
    for s in source:
        text += f"\t {s['名称']}: {s['成绩']}\n"
    text += "\n不用谢我，空间说说拜托扫一下呜呜呜"
    print(text)
    pyperclip.copy(text)
    force_update = False
