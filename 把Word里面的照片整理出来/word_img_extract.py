import itertools
import os
import shutil
from pathlib import Path
from zipfile import ZipFile

from PIL import Image
from win32com import client as wc  # 导入模块

def word_img_extract(doc_path, temp_dir="temp"):
    if os.path.exists(f"{doc_path}/{temp_dir}"):
        shutil.rmtree(f"{doc_path}/{temp_dir}")
    os.mkdir(f"{doc_path}/{temp_dir}")

    word = wc.Dispatch("Word.Application")  # 打开word应用程序
    try:
        files = list(Path(doc_path).glob("*.doc"))
        if len(files) == 0:
            raise Exception("当前目录中没有word文档")
        for i, filename in enumerate(files, 1):
            file = str(filename)
            dest_name = str(filename.parent / f"{temp_dir}" / str(filename.name)) + "x"
            # print(file, dest_name)
            doc = word.Documents.Open(file)  # 打开word文件
            doc.SaveAs(dest_name, 12)  # 另存为后缀为".docx"的文件，其中参数12指docx文件
            yield "word doc格式转docx格式：", i * 1000 // len(files)
    finally:
        word.Quit()

    if os.path.exists(f"{doc_path}/{temp_dir}/imgs"):
        shutil.rmtree(f"{doc_path}/{temp_dir}/imgs")
    os.makedirs(f"{doc_path}/{temp_dir}/imgs")

    i = 1
    files = list(itertools.chain(Path(doc_path).glob("*.docx"), (Path(doc_path) / temp_dir).glob("*.docx")))
    for j, filename in enumerate(files, 1):
        # print(filename)
        with ZipFile(filename) as zip_file:
            for names in zip_file.namelist():
                if names.startswith("word/media/image"):
                    zip_file.extract(names, doc_path)
                    os.rename(f"{doc_path}/{names}",
                              f"{doc_path}/{temp_dir}/imgs/{i}{names[names.find('.'):]}")
                    # print("\t", names, f"{i}{names[names.find('.'):]}")
                    i += 1
        yield "word提取图片：", j * 1000 // len(files)
    shutil.rmtree(f"{doc_path}/word")

    if not os.path.exists(f"{doc_path}/imgs"):
        os.mkdir(f"{doc_path}/imgs")

    files = list(Path(f"{doc_path}/{temp_dir}/imgs").glob("*"))
    for i, filename in enumerate(files, 1):
        file = str(filename)
        with Image.open(file) as im:
            im.convert('RGB').save(
                f"{doc_path}/imgs/{filename.name[:filename.name.find('.')]}.jpg", 'jpeg')
        yield "图片转换为jpg格式：", i * 1000 // len(files)


if __name__ == '__main__':
    doc_path = r"E:\tmp\答疑整理"
    for msg, i in word_img_extract(doc_path):
        print(f"\r {msg}{i}", end="")