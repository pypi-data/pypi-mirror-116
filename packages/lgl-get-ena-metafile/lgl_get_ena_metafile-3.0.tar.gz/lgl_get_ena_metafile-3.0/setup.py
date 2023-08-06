# -*- coding: utf-8 -*-
 
"""
Author     : Liugeliang
Description: get_pubmed_ren
"""
 
import setuptools
 
 
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
 
 
setuptools.setup(
    name='lgl_get_ena_metafile',  # 模块名称
    version="3.0",  # 当前版本
    author="liugeliang",  # 作者
    author_email="sx_liugeliang@163.com",  # 作者邮箱
    description="ENA数据库高通量数据元数据(.txt)批量下载器",  # 模块简介
    long_description = long_description, #模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=['selenium'],
    python_requires='>=3.6',
)