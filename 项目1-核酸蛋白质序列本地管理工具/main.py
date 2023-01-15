# Python大作业——核酸/蛋白序列本地管理工具
# 作者：华中农业大学 生物信息学2002 张玉 2020317210208
# 2022-12-26

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from urllib.request import urlopen
import re
from time import sleep

def main_page():
    """
    主界面配置
    """
    window = Tk()
    # 外框配置
    window.title("主页")
    window.geometry("800x600")
    window.iconbitmap("icon.ico")
    # 图片
    main_img = PhotoImage(file="背景.gif")
    img_lab = Label(window, image=main_img).pack(side="top")
    # 标题文字
    main_text = Label(window,
        text="核酸/蛋白序列本地管理工具",
        font=("微软雅黑", 20, "bold"),
        borderwidth=10)
    main_text.pack(fill=X)
    # 按钮控件
    b1 = Button(window,
        text="本地序列库查询",
        font=("宋体", 15, "bold"),
        bg="#DDEBE9",
        command=seq_db)
    b2 = Button(window,
        text="从NCBI下载序列",
        font=("宋体", 15, "bold"),
        bg="#3C8883",
        command=crawl_page)
    b3 = Button(window,
        text="退出",
        font=("宋体", 15, "bold"),
        bg="#415F90",
        command=window.quit)
    b1.pack()
    b2.pack()
    b3.pack()
    # 提交运行
    window.mainloop()

def seq_db():
    """
    序列库界面
    """
    # 初始化窗口
    tb = Tk()
    tb.title("数据库")
    tb.geometry("800x600")
    tb.iconbitmap("icon.ico")
    # 表格设置
    table_frame = Frame(tb)
    table_frame.pack()
    columns = ['类型', '注册号', '名称', '长度', '来源']
    table = ttk.Treeview(
        master=tb,
        height=30,
        columns=columns,
        show="headings"
    )
    table.heading(column='类型', text='类型')
    table.heading(column='注册号', text='注册号')
    table.heading(column='名称', text='名称')
    table.heading(column='长度', text='长度')
    table.heading(column='来源', text='来源')
    table.column('类型', width=150, anchor=S)
    table.column('注册号', width=150, anchor=S)
    table.column('名称', width=150, anchor=S)
    table.column('长度', width=150, anchor=S)
    table.column('来源', width=150, anchor=S)
    # 初始载入本地文件
    load_file(table)
    # 顶部工具栏
    main_menu = Menu(tb)
    main_menu.add_command(label="添加新序列", command=lambda:insert(table))
    main_menu.add_command(label="删除序列", command=lambda:delete(table))
    main_menu.add_command(label="下载目标序列", command=download)
    main_menu.add_command(label="清空数据库", command=lambda:del_all(table))
    tb.config (menu=main_menu)
    # 布局
    table.pack(fill=BOTH, expand=True)

def load_file(table):
    """
    从本地文件中读取序列并插入表格
    """
    file = open("table.txt", "rt")
    data = file.readlines()
    if data != []:
        for i in data:
            sub = i.strip().split("\t")
            table.insert('', END,
                values=(sub[0], sub[1], sub[2], sub[3], sub[4]))
    file.close()

def insert(table):
    """
    插入一条新记录
    """
    # 创建窗体
    ins = Tk()
    ins.title("插入一条新记录")
    ins.geometry("250x200")
    ins.iconbitmap("icon.ico")
    # 创建标签对象
    label1 = Label(ins, text="类型: ").grid(row=0)
    label2 = Label(ins, text="注册号: ").grid(row=1)
    label3 = Label(ins, text="名称: ").grid(row=2)
    label4 = Label(ins, text="长度: ").grid(row=3)
    label5 = Label(ins, text="来源: ").grid(row=4)
    label6 = Label(ins, text="序列: ").grid(row=5)
    # 创建输入控件对象
    entry1 = Entry(ins)
    entry2 = Entry(ins)
    entry3 = Entry(ins)
    entry4 = Entry(ins)
    entry5 = Entry(ins)
    entry6 = Entry(ins)
    entry1.grid(row=0, column=1)
    entry2.grid(row=1, column=1)
    entry3.grid(row=2, column=1)
    entry4.grid(row=3, column=1)
    entry5.grid(row=4, column=1)
    entry6.grid(row=5, column=1)
    # 按钮对象
    button = Button(ins, text="插入",
      font=("微软雅黑", 10, "bold"),
      command=lambda:update(entry1.get(), entry2.get(), entry3.get(),
          entry4.get(), entry5.get(), entry6.get(), table, ins))
    button.grid(row=6, column=1)
    
def update(e1, e2, e3, e4, e5, e6, table, win):
    """
    更新本地文件
    """
    # 写入表格文件
    file = open("table.txt", "a")
    file.write("%s\t%s\t%s\t%s\t%s\n"%(e1, e2, e3, e4, e5))
    file.close()
    # 写入序列文件
    file = open("seq.txt", "a")
    seq = ''
    for i in e6:
        if i != "\n":
            seq += i.strip()
    file.write("%s\t%s\t%s\n"%(e1, e2, seq))
    file.close()
    # 删除显示的内容并重新加载
    for item in table.get_children():
        table.delete(item)
    load_file(table)
    # 弹出信息并摧毁窗口
    messagebox.showinfo(title="提示", message="添加成功!")
    win.destroy()

def delete(table):
    """
    删除指定的数据
    """
    # 创建窗体
    dele = Tk()
    dele.title("删除记录")
    dele.geometry("230x100")
    dele.iconbitmap("icon.ico")
    # 创建标签对象
    label = Label(dele, text="请输入要删除的序列注册号: ").grid(row=0)
    label2 = Label(dele, text="(如果有多条,请务必以英文','间隔!!!)").grid(row=2)
    # 创建输入控件对象
    entry = Entry(dele)
    entry.grid(row=1, column=0)
    # 按钮对象
    button = Button(dele, text="删除",
      font=("微软雅黑", 10, "bold"),
      command=lambda:update2(entry.get(), table, dele))
    button.grid(row=3, column=0)

def update2(e, table, win):
    """
    因删除重写文件
    """
    # 重写表格文件
    del_line = e.split(",")
    count = 0
    with open("table.txt", "rt") as f:
        lines = f.readlines()
    with open("table.txt","wt") as f_w:
        for line in lines:
            mark = 0
            for i in del_line:
                if i in line.split("\t"):
                    count += 1
                    mark = 1
                    continue
            if mark == 0:
                f_w.write(line)
    # 重写序列文件
    with open("seq.txt", "rt") as f:
        lines = f.readlines()
    with open("seq.txt","wt") as f_w:
        for line in lines:
            mark = 0
            for i in del_line:
                if i in line.split("\t"):
                    mark = 1
                    continue
            if mark == 0:
                f_w.write(line)
    # 删除并重新加载
    for item in table.get_children():
        table.delete(item)
    load_file(table)
    # 弹出信息并摧毁窗口
    if count == len(del_line):
        messagebox.showinfo(title="提示", message="全部删除成功!")
    elif count < len(del_line) and count > 0:
        messagebox.showinfo(title="提示", message="只删除了%s条!"%count)
    elif count == 0:
        messagebox.showinfo(title="提示", message="没有找到数据!")
    win.destroy()

def download():
    """
    下载本地数据库中指定的序列
    """
    # 创建窗体
    dl = Tk()
    dl.title("下载序列")
    dl.geometry("500x150")
    dl.iconbitmap("icon.ico")
    # 创建标签对象
    label = Label(dl, text="请输入要下载的序列注册号: ").grid(row=0, sticky=W)
    label2 = Label(dl, text="(如果有多条,请务必以英文','间隔!!!)").grid(row=2, column=1, sticky=W)
    label3 = Label(dl, text="下载路径: ").grid(row=3, sticky=W)
    # 路径变量
    path = StringVar()
    # 创建输入控件对象
    entry = Entry(dl)
    entry2 = Entry(dl, textvariable=path)
    entry.grid(row=1, column=1)
    entry2.grid(row=3, column=1)
    # 按钮对象
    button = Button(dl, text="选择路径",
      font=("微软雅黑", 10, "bold"),
      command=lambda:open_file_name(entry2))
    button.grid(row=3, column=2, sticky=W)
    button2 = Button(dl, text="下载",
      font=("微软雅黑", 10, "bold"),
      command=lambda:download_all(entry.get(), entry2.get(), dl))
    button2.grid(row=4, column=1)

def open_file_name(entry):
    """
    返回获取的文件路径
    """
    entry.insert(0, filedialog.askopenfilename())

def download_all(number, file_path, win):
    """
    按指定路径下载需要的序列    
    """
    acc_num = number.split(",")
    name_list = []
    seq_list = []
    # 从表格文件中获取名字
    lines = open("table.txt", "rt").readlines()
    for i in acc_num:
        for line in lines:
            if i in line.split("\t"):
                name_list.append(line.split("\t")[2])
                break
    # 从序列文件中获取序列
    lines = open("seq.txt", "rt").readlines()
    for i in acc_num:
        for line in lines:
            if i in line.split("\t"):
                seq_list.append(line.split("\t")[2])
                break
    # 写入目标文件
    file = open(file_path, 'wt')
    for i in range(len(name_list)):
        file.write("> %s %s\n"%(acc_num[i], name_list[i]))
        file.write("%s\n"%seq_list[i].strip())
    messagebox.showinfo(title="提示", message="下载成功!")
    win.destroy()

def del_all(table):
    """
    清空全部数据
    """
    for item in table.get_children():
        table.delete(item)
    with open("table.txt",'a+',encoding='utf-8') as f:
        f.truncate(0)
    with open("seq.txt",'a+',encoding='utf-8') as f:
        f.truncate(0)

def crawl_page():
    """
    从NCBI上爬取想要的序列页面
    """
    cr = Tk()
    cr.title("NCBI抓取")
    cr.geometry("400x300")
    cr.iconbitmap("icon.ico")
    # 请求库选择
    label1 = Label(cr, text="请求库: ").grid(row=0, sticky=W)
    entry1 = Entry(cr)
    entry1.insert(0, "填入 nuccore 或 protein")
    entry1.grid(row=0, column=1)
    # 序列号输入
    label2 = Label(cr, text="序列号(以','间隔): ").grid(row=1, sticky=W)
    entry2 = Entry(cr)
    entry2.grid(row=1, column=1)
    # 是否存储到本地库中
    label3 = Label(cr, text="是否将结果存储到库: ").grid(row=2, sticky=W)
    entry3 = Entry(cr)
    entry3.insert(0, "填入 是 或 否")
    entry3.grid(row=2, column=1)
    # 是否输出到某文件
    label4 = Label(cr, text="是否将结果存储到本地文件: ").grid(row=3, sticky=W)
    entry4 = Entry(cr)
    entry4.insert(0, "填入 是 或 否")
    entry4.grid(row=3, column=1)
    # 获取路径
    entry5 = Entry(cr)
    entry5.grid(row=4, column=1)
    button = Button(cr, text="选择路径",
      font=("微软雅黑", 10, "bold"),
      command=lambda:open_file_name(entry5))
    button.grid(row=4, column=0, sticky=W)
    # 提交运行
    button2 = Button(cr, text="抓取",
      font=("微软雅黑", 10, "bold"),
      command=lambda:crawl(entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), cr))
    button2.grid(row=5, column=1, sticky=W)

def crawl(repo, accession, store, download, path=None, win=None):
    """
    爬取NCBI相应内容
    """
    file1 = open("table.txt", "a")
    file2 = open("seq.txt", "a")
    if path != '':
        file3 = open(path, "a")
    for i in accession.split(","):
        print("正在爬取%s主页信息..."%i)
        ## 爬取主页
        # 一级请求，获得uid号
        url = "https://www.ncbi.nlm.nih.gov/" + repo + "/" + i
        f = urlopen(url)
        temp = f.read().decode("utf-8")
        f.close()
        find_uid = re.compile(r'ncbi_uid=(.*?)&')
        res = re.search(find_uid, temp).group()
        uid = res.split("=")[1].split("&")[0]
        # 同级请求fasta，获得phid号
        url = "https://www.ncbi.nlm.nih.gov/" + repo + "/" + i + "?report=fasta"
        f = urlopen(url)
        temp = f.read().decode("utf-8")
        f.close()
        find_phid = re.compile(r'ncbi_phid=(.*?)" /')
        res = re.search(find_phid, temp).group()
        phid = res.split("=")[1].split("\"")[0]
        sleep(5)    # 礼貌访问
        # 二级请求
        url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id="+uid
        f = urlopen(url)
        result = f.read().decode("utf-8")
        f.close()
        # 根据请求库不同进行存储
        name = re.findall(r'DEFINITION(.*?)\nACCESSION', result)[0].strip()
        source = re.findall(r'SOURCE(.*?)\n  ORGANISM', result)[0].strip()
        if repo == "nuccore":
            seq_type = "Nucleotide"
            length = re.findall(r'%s(.*?) bp'%i, result)[0].strip()
        elif repo == "protein":
            seq_type = "Protein"
            length = re.findall(r'%s(.*?) aa'%i, result)[0].strip()
        # 根据需要进行本地库存储
        if store == "是":
            file1.write("%s\t%s\t%s\t%s\t%s\n"%(seq_type, i, name, length, source))
        print("%s主页信息已爬取,准备爬取FASTA信息..."%i)
        sleep(5)    # 礼貌访问
        ## 爬取FASTA序列
        # 三级请求，获取FASTA页面
        url = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=%s&db=%s&report=fasta&extrafeat=null&conwithfeat=on&hide-cdd=on&retmode=html&ncbi_phid=%s&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000"%(uid, repo, phid)
        f = urlopen(url)
        result = f.read().decode("utf-8")
        f.close()
        # 依情况存储
        if store == "是":
            # 获取一行序列
            seq = ''
            raw = result.split("\n")[1:]
            for i in raw:
                seq += i
            # 存储
            file2.write("%s\t%s\t%s\n"%(seq_type, i, seq))
        if download == "是":
            file3.write(result)
        print("已完成爬取%s!请等待下一轮爬取..."%i)
        sleep(5)    # 礼貌访问，等待下一轮请求
    file1.close()
    file2.close()
    if path != '':
        file3.close()
    messagebox.showinfo(title="提示", message="爬取完成!")
    win.destroy()

# 运行
main_page()