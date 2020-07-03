# LogTools
[English](https://github.com/XOB-CN/LogTools)
## **软件概述**
LogTools 是一个基于 PyQt5 的通用日志分析软件.  
该软件可以使用 SQL 语句来过滤您想要的日志内容.  
![MainGUI](https://github.com/XOB-CN/LogTools/raw/master/guide/picture/Main_GUI.png)  

## **源码运行**
1. 安装 Python3  
2. 安装 Microsoft Visual C++ 14.0  
   如果不想安装 VisualStudio, 可以尝试安装 
   [Microsoft Visual C++ Build Tools](https://www.microsoft.com/en-us/download/details.aspx?id=48159)
3. 安装 PyQt5, 可以使用 pip 命令来安装
    ```commandline
    pip install pyqt5 psutil
    ```
4. 双击文件中的 LogTools.py 文件来运行软件
5. 如果您不想在运行中看到 cmd 的 console 界面, 可以将 LogTools.py 重命名为 LogTools.pyw

## **编译运行**
如果不想使用源码方式来运行, 也可以选择直接运行编译后的 LogTools.exe 程序文件  
[Windows x64 下载链接](https://github.com/XOB-CN/LogTools/releases)

## **项目状态**
基本功能已经完成, 目前计划添加 MicroFocus ITOM 产品的日志

## **支持产品**
* MicroFocus
  * ITOM
    * OA
    * OBM/OMi
    * MP for Microsoft SQL Server
    * SiteScope