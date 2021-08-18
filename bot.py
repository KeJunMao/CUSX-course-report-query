import asyncio
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import At, Plain, Image, Quote, Source
from graia.application.session import Session
from graia.application.message.chain import MessageChain
from graia.application.group import Group, Member
from User import User
from graia.application.friend import Friend
from gen_png import gen_png
from dotenv import load_dotenv
import os
load_dotenv()

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",
        authKey=os.getenv('BOT_KEY'),
        account=os.getenv('BOT_QQ'),
        websocket=True
    )
)


@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    if message.asDisplay().startswith("/") and group.id == 976500620:
        text = ""
        force_update = False
        input_value = message.asDisplay().split('/')[1].split()
        user_png = None
        if len(input_value) == 1:
            username = input_value[0]
            password = username
        elif len(input_value) == 2:
            username, password = input_value
            if password == '--force':
                force_update = True
                password = username
        elif len(input_value) == 3:
            username, password, force_flag = input_value
            if force_flag == '--force':
                force_update = True
                password = password
        if len(username) != 10:
            text = "无效学号"
        else:
            user = User(username, password, True, force_update)
            source = user.do()
            if not user.isLogin:
                text = '密码错误'
            else:
                png = gen_png(user, course=source)
                user_png = Image.fromUnsafeBytes(png)
                if len(source) == 0:
                    text = "暂无成绩"
        element = [At(member.id), Plain(text)]
        if user_png is not None:
            element[1] = user_png
        await app.sendGroupMessage(group, MessageChain.create(element))
    elif message.asDisplay().startswith("/"):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain("为了不打扰大家正常聊天，特意建了群查成绩 976500620")
        ]))

app.launch_blocking()
