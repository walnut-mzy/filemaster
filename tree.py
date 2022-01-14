import base64
import os
import sqlite3
import hashlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox,QFileDialog,QFrame
from treelib import Tree
from PyQt5.QtGui import QIcon
import sys,os
import time
import datetime
import PyQt5
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
num=1
count=0
class fileTREE:
    def __init__(self,root=None):
        self.tree=Tree()
        if root==None:
            raise Exception("建立一个项目必须有根节点")
        else:
            self.tree.create_node(root,root)
    def append(self,node,parent_node_name):
        """
        :param node: 文件名
        :return: true,false
        """
        try:
            self.tree.add_node(node,parent_node_name)
            return True
        except Exception as e:
            print("出现意外错误")
            raise  e

    def delete(self,node):
        """
        :param node:文件名
        :return:s
        """
        self.tree.remove_node(node)
    def show(self):
        """打印树"""
        print(self.tree)
    def return_tree(self):
        return self.tree
    def delete_clear(self,node):
        """
        完全删除一个文件
               :param node:文件名
               :return:
               """
        node1=node
        str1 = str(node)
        print(str1)
        print(self.find_child(node1))
        # while self.find_praents(node) != None:
        #     node = self.find_praents(node).tag
        #     str1 = node + "/" + str1
        if self.find_child(node1)!=[]:
            str1=os.getcwd().replace("\\","/")+str1[1:]
            print(str1)
            os.removedirs(str1)
        else:
            str1 = os.getcwd().replace("\\", "/") + str1[1:]
            print(str1)
            os.remove(str1)
        self.tree.remove_node(node)
        return True
    def open(self,node):
        """
        :param node: 文件名
        :return: 读出结果
        """
        if self.find_child(node)!=[]:
            raise Exception("该文件是一个目录不能读取")
        str1=str(node)
        while self.find_praents(node)!=None:
            node=self.find_praents(node).tag
            str1=node+"/"+str1
        with open(str1,"r",encoding="utf-8") as fp:
            return  fp.read()
    def xianxu_sort(self):
        """
        先序遍历
        :return:
        """
        return [self.tree[node].tag for node in self.tree.expand_tree(mode=Tree.DEPTH, sorting=False)]

    def cengxu_sort(self):
        """
        层序遍历
        :return:
        """
        return [self.tree[node].tag for node in self.tree.expand_tree(mode=Tree.WIDTH, sorting=False)]
    def zhongxu_sort(self):
        """
        中序遍历
        :return:
        """
        return [self.tree[node].tag for node in self.tree.expand_tree(mode=Tree.DEPTH, sorting=False)]
    def houxu_sort(self):
        """
        后序遍历
        :return:
        """
        return [self.tree[node].tag for node in self.tree.expand_tree(mode=Tree.WIDTH, sorting=False,reverse=False)]
    def find_praents(self,node):
        """
        找到父亲节点
        :return:
        """
        return self.tree.parent(node)
    def find_child(self,node):
        """
        :param node:
        :return: 找到子节点
        """
        return self.tree.children(node)
    def sort_by_size(self,node):
        """
        以该节点为父节点对没给文件的大小进行排序
        :param node:
        :return:
        """
        if self.find_child(node)==None:
            raise Exception("文件不能被排序")
        str1 = str(node)
        node1=node
        while self.find_praents(node) != None:
            node = self.find_praents(node).tag
            str1 = node + "/" + str1
        dic1=dict(zip(["./"+i for i in os.listdir(str1)],[os.path.getsize(i) for i in os.listdir(str1)]))
        print(dic1)
        dic1=sorted(dic1.items(),key=lambda  x:x[1],reverse=False)
        return str(dic1)
        # parents_node1=self.find_praents(node1)
        # self.delete(node1)
        # self.append(node1,parents_node1)
        # [self.append(i,node1) for i in dic1.keys()]
    #使用冒泡排序进行
    def bubble_sort(self,nums):
        for i in range(len(nums) - 1):
            for j in range(len(nums) - i - 1):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
        return nums
    #使用快速排序
    def quick_sort(self,nums: list, left: int, right: int) -> None:
        if left < right:
            i = left
            j = right
            # 取第一个元素为枢轴量
            pivot = nums[left]
            while i != j:
                # 交替扫描和交换
                # 从右往左找到第一个比枢轴量小的元素，交换位置
                while j > i and nums[j] > pivot:
                    j -= 1
                if j > i:
                    # 如果找到了，进行元素交换
                    nums[i] = nums[j]
                    i += 1
                # 从左往右找到第一个比枢轴量大的元素，交换位置
                while i < j and nums[i] < pivot:
                    i += 1
                if i < j:
                    nums[j] = nums[i]
                    j -= 1
            # 至此完成一趟快速排序，枢轴量的位置已经确定好了，就在i位置上（i和j)值相等
            nums[i] = pivot
            # 以i为枢轴进行子序列元素交换
            self.quick_sort(nums, left, i - 1)
            self.quick_sort(nums, i + 1, right)
    #使用归并排序
    def merge(self,a, b):
        c = []
        h = j = 0
        while j < len(a) and h < len(b):
            if a[j] < b[h]:
                c.append(a[j])
                j += 1
            else:
                c.append(b[h])
                h += 1

        if j == len(a):
            for i in b[h:]:
                c.append(i)
        else:
            for i in a[j:]:
                c.append(i)

        return c

    def merge_sort(self,lists):
        if len(lists) <= 1:
            return lists
        middle = len(lists) // 2
        left = self.merge_sort(lists[:middle])
        right = self.erge_sort(lists[middle:])
        return self.merge(left, right)
    def create_by_path(self,path):
        """
        :param path: 文件路径 注：这个是根据文件路径打开文件的
        :return:
        """
        list1 = [path]
        while True:
            list0 = []
            for k in list1:
                for i in os.listdir(k):
                    self.tree.create_node(k + "/" + i, k + "/" + i, parent=k)
                    # print(i)
                    if os.path.isdir(k + "/" + i):
                        # print(i)
                        list0.append(k + "/" + i)
                    print(list0)
            list1 = list0
            if list1 == []:
                break


class login:
    def __init__(self,password,login,who):
        self.password=password
        self.loginword=login
        self.who=who
    def check(self,who,login1,password1):
        """
        返回是否登录成功
        :param login1:
        :param password1:
        :return:  true or false
        """
        if self.password==password1 and self.loginword==login1:
            return True
    def check_admin(self,login1,password1,who):
        # conn=sqlite3.connect("file.db")
        # curosr=conn.cursor()
        # #执行sql语句
        # #curosr.execute("create table user(id varchar(20),password varchar(20))")
        # curosr.execute("insert into user (id, password) values ('admin','mzy12345' )")
        # conn.commit()
        # curosr.execute("select * from user where id=" + login1 + " and " + "password=" + password1)
        # values=curosr.fetchall()
        #m.update(b"admin admin mzy12345")
        # conn=sqlite3.connect("file.db")
        # curosr=conn.cursor()
        # #执行sql语句
        # #curosr.execute("create table user(id varchar(20),password varchar(20))")
        # curosr.execute("insert into user (id, password) values ('admin','mzy12345' )")
        # conn.commit()
        # curosr.execute("select * from user where id=" + login1 + " and " + "password=" + password1)
        # values=curosr.fetchall()
        # print(values)
        # m.update(b"admin admin mzy12345")
        import hashlib
        m = hashlib.md5()
        with open("admin.db", "r", encoding="utf-8") as fp:
            str1 = fp.read()
            list1 = str1.split("\n")
            print(who + "/" + login1 + "/" + password1)
            m.update((who + "/" + login1 + "/" + password1).encode(encoding='UTF-8'))
            print(list1)
            print(m.hexdigest())
            if m.hexdigest() in list1:
                return True
            else:
                return False





class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(290, 216)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(90, 150, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(70, 60, 151, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 100, 151, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 60, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 72, 15))
        self.label_3.setObjectName("label_3")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(70, 20, 151, 21))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("文件管理系统")
        Form.setWindowIcon(QIcon("filemaster.png"))
        self.pushButton.setText(_translate("Form", "login"))
        self.label.setText(_translate("Form", "账号"))
        self.label_2.setText(_translate("Form", "密码"))
        self.label_3.setText(_translate("Form", "身份"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Form", "admin"))
        item = self.listWidget.item(1)
        item.setText(_translate("Form", "usr"))
        self.listWidget.setSortingEnabled(__sortingEnabled)


class Ui_Form1(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(140, 40, 251, 261))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 40, 91, 261))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(170, 10, 41, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(230, 10, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(290, 10, 41, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(340, 10, 41, 16))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("文件管理系统")
        Form.setWindowIcon(QIcon("filemaster.png"))
        self.label.setText(_translate("Form", "fileTree"))
        self.label_2.setText(_translate("Form", "copy"))
        self.label_3.setText(_translate("Form", "copy"))
        self.label_4.setText(_translate("Form", "copy"))
        self.label_5.setText(_translate("Form", "copy"))
class Ui_Form2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(968, 618)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(0, 20, 371, 601))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(400, 70, 561, 551))
        self.textEdit.setObjectName("textEdit")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(400, 0, 561, 71))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("文件管理系统")
        Form.setWindowIcon(QIcon("filemaster.png"))
        self.pushButton.setText(_translate("Form", "open"))
        self.pushButton_2.setText(_translate("Form", "del"))
        self.pushButton_3.setText(_translate("Form", "save"))
        self.pushButton_4.setText(_translate("Form", "show"))
class Ui_Form3(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(657, 445)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 661, 451))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("文件管理系统")
        Form.setWindowIcon(QIcon("filemaster.png"))
class mywindow3(QWidget, Ui_Form3):  # 这个地方要注意Ui_MainWindow
    def __init__(self,text,parent=None):
        super(mywindow3, self).__init__(parent)
        self.setupUi(self)
        self.textEdit.setText(text)

class mywindow1(QWidget, Ui_Form2):  # 这个地方要注意Ui_MainWindow
    def __init__(self,count,parent=None):
        super(mywindow1, self).__init__(parent)
        self.setupUi(self)
        self.tree=fileTREE(".")
        self.tree.create_by_path(".")
        self.slot_init()
        self.pushButton.setIcon(QIcon("file.png"))
        self.pushButton_2.setIcon(QIcon("del.png"))
        self.pushButton_3.setIcon(QIcon("save.png"))
        self.pushButton_4.setIcon(QIcon("show.png"))
        self.count=count
#(str(tree.return_tree()))
        self.plainTextEdit_2.setPlainText((str(self.tree.return_tree())))
        #self.plainTextEdit_2.setEnabled(False)
        self.file1=None
        #self.textEdit_2.setText(str(tree.return_tree()))
        self.mainwindows=mywindow3("层序排序："+str(self.tree.cengxu_sort())+"\n\n\n后序排序:"+str(self.tree.houxu_sort())+"\n\n\n中序排序:"+str(self.tree.zhongxu_sort())+"\n\n\n前序排序"+str(self.tree.xianxu_sort())
                          +"\n\n\n以大小排列:\n冒泡排序"+str(self.tree.sort_by_size("."))+"\n\n\n快速排序"+str(self.tree.sort_by_size("."))+"\n\n\n归并排序:"+str(self.tree.sort_by_size("."))          )
        #self.pushButton_4.clicked.connect(self.show)
    def slot_init(self):
        # self.pushButton.clicked.connect(self.selectall)
        self.pushButton.clicked.connect(self.file)
        self.pushButton_2.clicked.connect(self.delete)

        self.pushButton_3.clicked.connect(self.save)
        self.pushButton_4.clicked.connect(self.show1)
    def delete1(self):
        QMessageBox.warning(self,"warning","非管理员不能删除")
    def save1(self):
        QMessageBox.warning(self,"warning","非管理员不能修改")
    def file(self):

        self.textEdit.clear()
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        self.file1=fileName
        with open("file.log", "a+") as fp:
            fp.write(str(datetime.datetime.now())+"执行打开操作  "+"filename:"+str(fileName)+ "\n")
        try:
            with open(fileName,"r",encoding="utf-8") as fp:
                self.textEdit.setText(fp.read())
        except Exception as e:
            QMessageBox.warning(self,"warm",str(e))

    def delete(self):
        if self.count==1:
            QMessageBox.warning(self, "warning", "非管理员不能删除")
            return
        self.textEdit.clear()
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        print(fileName)
        with open("file.log", "a+") as fp:
            fp.write(str(datetime.datetime.now())+" 执行删除操作  "+"filename:"+str(fileName)+ "\n")
        try:
            self.plainTextEdit_2.clear()
            self.plainTextEdit_2.setPlainText(str(self.tree.return_tree()))
            self.tree.delete_clear("./"+os.path.relpath(fileName, os.getcwd()).replace("\\","/"))
            QMessageBox.about(self,"warning","删除成功")
          # self.tree.delete_clear()
        except Exception as e:
            QMessageBox.warning(self, "warm", str(e))

    def save(self):
        if self.count==1:
            QMessageBox.warning(self, "warning", "非管理员不能修改")
            return
        if self.file1==None:
            QMessageBox.about(self,"about","没有打开文件")
            return
        try:
            with open("file.log", "a+") as fp:
                fp.write(str(datetime.datetime.now()) + " 执行保存操作  " + "filename:" + str(self.file1) + "\n")
            with open(self.file1,"a",encoding="utf-8") as fp:
                fp.write(self.textEdit.toPlainText())
                QMessageBox.about(self,"about","已保存")
        except Exception as e:
            QMessageBox.warning(self,"warning",str(e))
    def show1(self):
        print("hello")
        with open("file.log", "a+") as fp:
            fp.write(str(datetime.datetime.now()) + " 执行展示操作  " + "\n")
        self.mainwindows.show()

class mywindow(QWidget, Ui_Form):  # 这个地方要注意Ui_MainWindow
    def __init__(self,parent=None):
        super(mywindow, self).__init__(parent)
        self.setupUi(self)
        #self.slot_init()
        self.pushButton.clicked.connect(self.check)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.mainwindow=None
        self.count=0
    def slot_init(self):
        #self.pushButton.clicked.connect(self.selectall)
        self.pushButton.clicked.connect(self.check)
    def check(self):
        flag=None
        login1=self.lineEdit.text()
        password=self.lineEdit_2.text()
        admin=self.listWidget.selectedItems()
        print(login1)
        print(password)
        try:
            admin=admin.pop().text()
        except:
            admin="admin"
        if admin=="usr":
            print("#*9")
            self.count=1
       # my=login(login1,password,admin.pop().text())
        try:

            ma = hashlib.md5()
            with open("admin.db", "r", encoding="utf-8") as fp:
                str1 = fp.read()
                list1 = str1.split("\n")
                print((admin + "/" + login1 + "/" + password))
                ma.update((admin + "/" + login1 + "/" + password).encode())
                print(list1)
                print(ma.hexdigest())
                if ma.hexdigest() in list1:
                    flag=True
                else:
                    flag=False
            if flag:
                print("hello")
                reply4 = QMessageBox.about(self,"about", "密码正确")
                num=0
                self.hide()
                #self.show()
                self.open_main_window()

            else:
                reply4 = QMessageBox.about(self, "about", "密码错误")
        except Exception as e:
            with open("file.log","a+") as fp:
                fp.write(e)

    def open_main_window(self):
        self.mainwindow=mywindow1(self.count)
        self.mainwindow.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w=mywindow()
    w.show()
    sys.exit(app.exec_())
# if __name__ == '__main__':
#
#     tree=fileTREE(".")
#     tree.create_by_path(".")
#     tree.show()
