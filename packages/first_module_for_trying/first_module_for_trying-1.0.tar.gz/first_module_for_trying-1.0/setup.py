from distutils.core import setup

setup(
    name='first_module_for_trying',            # 对外我们的模块名
    version='1.0',                  # 版本号
    description='第一次尝试上传模块',    # 描述
    author='wennan',                    # 作者
    author_email='xiangwennan@163.com',     # 作者邮箱
    py_modules=['first_module_for_trying.Salary_copy']       # 要发布的模块
)

