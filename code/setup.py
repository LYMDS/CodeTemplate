from cx_Freeze import setup, Executable
import sys
import os.path
#from docx import Document
#from tkinter import filedialog

# try:
#     import xml.etree.cElementTree as ET
# except ImportError:
#     import xml.etree.ElementTree as ET
#
# os.environ['TCL_LIBRARY'] = r'C:\D\Python\Python312\tcl\tcl8.6'
# os.environ['TK_LIBRARY'] = r'C:\D\Python\Python312\tcl\tk8.6'
base = 'Win32GUI' if sys.platform=='win32' else None
# includes = [r"queue"]
# include_files = [r"C:\D\Python\Python312\DLLs\tcl86t.dll",
#                  r"C:\D\Python\Python312\DLLs\tk86t.dll"]

# 本地Python打包环境的路径
pythonBaseURL = "C:\\D\\Python\\Python312\\"

build_options = {
    "includes":
         [
             # "flask",
             # "sqlalchemy",
             # "flask_cors",
             # "jinja2",
             # "objtyping",
             # "json",
             # "html",
             # "uuid",
             # "io",
             # "datetime"
         ],
    "packages": [
        "sqlalchemy",
        "requests"
    ],
    "include_files":
        [
            ("Publish", "lib/Publish"),
            (pythonBaseURL + "DLLs\\sqlite3.dll", "lib\\sqlite3.dll")
        ]
}

data_files = []

executables = [
    Executable('main.py', target_name="CodeTemplate.exe", icon="logo.ico")
]

setup(name='CodeTemplate',
      version = '1.0',
      description = '代码模板',
      options={"build_exe": build_options},
      executables = executables,
      data_files=data_files)
