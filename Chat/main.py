from imp import reload
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js


import asyncio


chat_msjs = []
online_users = set()


max_messages_count = 100

async def main():
    global chat_msjs

    put_markdown("## Добро пожаловать в чат!")


    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input("Войти в чат!", required=True, placeholder="Ваше имя", validate=lambda n: "Такое имя уже используется!" if n in online_users or n == '' else None)
    online_users.add(nickname)

    chat_msjs.append(('', f"'{nickname}' присоединился к чату!"))
    msg_box.append(put_markdown(f"'{nickname}' присоединился к чату!"))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("Новое сообщение!", [input(placeholder="Текст сообщения", name="msg"), actions(name="cmd", buttons=["Отправить", {'label':"Выйти из чата!", 'type':'cancel'}])], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m["msg"] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"'{nickname}': {data['msg']}"))
        chat_msjs.append((nickname, data['msg']))

    #выход из чата
    refresh_task.close()

    online_users.remove(nickname)
    toast("Вы покинули чат!")
    msg_box.append(put_markdown(f"Пользователь '{nickname}' покинул чат!"))
    chat_msjs.append((f"Пользователь '{nickname}' покинул чат!"))

    put_buttons(["Зайти снова!"], onclick=lambda btn: run_js('window.location.reload'))


async def refresh_msg(nickname, msg_box):
    global chat_msjs
    last_idx = len(chat_msjs)

    while True:
        await asyncio.sleep(1)

        for m in chat_msjs[last_idx:]:
            if m[0] != nickname:
                msg_box.append(put_markdown(f"'{m[0]}': {m[1]}"))
        
        #remove expired
        if len(chat_msjs) > max_messages_count:
            chat_msjs = chat_msjs[len(chat_msjs) // 2:]

        last_idx = len(chat_msjs)


if __name__ == "__main__":
    start_server(main, debug=True, port=8000, cdn=False)