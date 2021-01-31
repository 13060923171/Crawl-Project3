import os
import comtypes.client
import time

def get_file(input_path, output_path):
    # 获取所有文件名的列表
    filename_list = os.listdir(input_path)
    # 获取所有 Word 文件名列表
    wordname_list = [filename for filename in filename_list \
                     if filename.endswith((".doc", ".docx"))]
    for wordname in wordname_list:
        # 分离 Word 文件名称和后缀，转化为 PDF 名称
        pdfname = os.path.splitext(wordname)[0] + ".pdf"
        # 如果当前 Word 文件对应的 PDF 文件存在，则不转化
        if pdfname in filename_list:
            continue
        # 拼接路径和文件名
        wordpath = os.path.join(input_path, wordname)
        pdfpath = os.path.join(output_path, pdfname)
        # 生成器
        yield wordpath, pdfpath

def word2pdf(input_path, output_path):
    word = comtypes.client.CreateObject("Word.Application")
    word.Visible = 0
    for wordpath, pdfpath in get_file(input_path, output_path):
        newpdf = word.Documents.Open(wordpath)
        newpdf.SaveAs(pdfpath, FileFormat=17)
        newpdf.Close()

if __name__ == "__main__":
    # 获取当前运行路径
    path = os.getcwd()
    print('------------正在转换中-------------')
    word2pdf(path + "\input", path + "\output")
    print('-------------转换完毕--------------')
    time.sleep(0.5)
