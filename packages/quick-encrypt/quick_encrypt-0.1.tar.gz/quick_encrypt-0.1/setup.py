# -*- coding=utf-8 -*-
from os import path
from codecs import open
from setuptools import setup, find_packages


basedir = path.abspath(path.dirname(__file__))

with open(path.join(basedir, 'README.md'), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='quick_encrypt',
    version='0.1',
    url='https://github.com/luxp4588/quick_encrypt.git',
    license='MIT',
    author="python-xp",
    author_email="luxp4588@126.com",
    description="用于快速实现AES加密功能，包含文本加密，数组或者字典类型加密方法",
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',

    zip_safe=False,
    include_package_data=True,
    install_requires=['pycryptodome'],
    keywords='AES ENCRYPT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)