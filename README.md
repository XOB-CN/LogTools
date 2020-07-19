# LogTools
[中文版说明](https://github.com/XOB-CN/LogTools/blob/master/README_CN.md)
## Overview
LogTools is a general log analysis software based on PyQt.  
It can use SQL query to filter out and get what you want log content.  
![MainGUI](https://github.com/XOB-CN/LogTools/raw/master/guide/picture/Main_GUI.png)  

## Running from source code
1. install Python3  
2. install Microsoft Visual C++ 14.0  
   if you don't want to install VisualStudio, you can try install 
   [Microsoft Visual C++ Build Tools](https://www.microsoft.com/en-us/download/details.aspx?id=48159)
3. install PyQt5
    ```commandline
    pip install pyqt5 psutil
    ```
4. Double-click the LogTools.py file
5. if you don't want see cmd console, you can rename LogTools.py to LogTools.pyw

## **Running from precompiled**
If you don't want to running as source code, also you can download binary file and double-click LogTools.exe file  
[Windows x64 download](https://github.com/XOB-CN/LogTools/releases)

## Current state
Basic functions have been finish. now planning to add logs for MicroFocus ITOM products

## Support product
* MicroFocus
  * ITOM
    * OA
    * OBM/OMi
    * MP for Microsoft SQL Server
    * MP for Oracle Database
    * SiteScope