import PySimpleGUI as sg

from word_img_extract import word_img_extract

sg.change_look_and_feel("GreenMono")

layout = [
    [
        sg.Text("请输入word文档所在的目录："),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse('浏览'),
    ], [
        sg.Button('开始抽取', enable_events=True, key="抽取"),
        sg.Text(text_color="red", size=(47, 2), key="error"),
    ], [
        sg.Text("准备：", size=(20, 1), key="-TOUT-"),
        sg.ProgressBar(1000, orientation='h', size=(35, 20), key='progressbar')
    ]
]
window = sg.Window('word文档图片抽取系统', layout)
while True:
    event, values = window.read()
    if event in (None,):
        break  # 相当于关闭界面
    elif event == "抽取":
        if values["-FOLDER-"]:
            window["error"].update("")
            try:
                for msg, i in word_img_extract(values["-FOLDER-"]):
                    window["-TOUT-"].update(msg)
                    window['progressbar'].UpdateBar(i)
                window["-TOUT-"].update('抽取完毕！！！')
            except Exception as e:
                window["error"].update(str(e))
        else:
            sg.popup('请先输入word文档所在的路径！！！')
window.close()