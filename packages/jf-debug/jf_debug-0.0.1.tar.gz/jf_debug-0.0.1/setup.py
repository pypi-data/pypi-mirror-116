# coding=utf-8

import setuptools


setuptools.setup(
    name="jf_debug",
    version="0.0.1",
    author="DePanda", 
    author_email="957454525@qq.com",
    description="debug过程中辅助修饰方法",
    long_description=open('README.rst').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ImDePanDa/pyrelease",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7", 
)