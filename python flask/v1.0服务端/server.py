import os
import time
import threading
import os.path
import flask
from flask import send_file
from tkinter import Tk, Entry, Button

app = flask.Flask(__name__)


def _reload():
    global forbidden, common, ppage
    forbidden = eval(open("forbidden.json", encoding="UTF-8").read())
    common = eval(open("common/data/common.json", encoding="UTF-8").read())

    print("重载完成。")


_reload()

def page4():
    return send_file("404/index.html")

def create_window():
    global w
    w = Tk()
    w.title("Flask GUI")
    e = Entry(w, font=["Consolas", 10, ""])
    e.pack()
    b1 = Button(
        w,
        text="Enter CMD",
        command=lambda: os.system(e.get()),
        font=["Consolas", 10, ""],
    )
    b2 = Button(
        w, text="Enter CPY", command=lambda: exec(e.get()), font=["Consolas", 10, ""]
    )
    b1.pack()
    b2.pack()
    w.mainloop()


@app.route("/")
def nonepage():
    return flask.redirect("/index.html")


@app.route("/<path:page>")
def mainpage(page):
    for i in forbidden:
        if i in page:
            return common["forbidden_tip"]
    if os.path.isdir(page):
        page = page
        page += "/index.html"
    try:
        return flask.send_file(page)
    except FileNotFoundError:
        return page4()


@app.route("/api/getError/<string:errcode>")
def gepage(errcode):
    ecj = eval(open("errorcode.json", encoding="UTF-8").read())
    return ecj[errcode]


def onserver():
    global w
    time.sleep(0.5)
    os.system("cls")
    print("欢迎使用 ©DAIQITAO-v1.0 服务端。")
    print("服务端已准备就绪！\n开始记录日志：\n")

    threading.Thread(target=create_window).start()

    app.run(host="0.0.0.0", port=8080)
    print("服务端已停止运行。\n")
    if 'w' in globals():
        w.destroy()


if __name__ == "__main__":
    threading.Thread(target=onserver).start()