from distutils.core import setup
setup(
    name = "bzmath",
    version = "1.0",
    description = '第一个测试模块',
    author = 'gaoqi',
    author_email='837434727@qq.com',
    py_modules = ['bzmath.demo1', 'bzmath.demo2'] #需要发行的模块

)
#python setup.py sdist
#python setup.py install
#最终安装环境D:\src\Python Files\modeling_hol2\venv\Lib\site-packages\bzmath

#对外发布 python setup.py sdist upload