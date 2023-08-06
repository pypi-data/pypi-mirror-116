# -*-coding:utf-8-*-
import setuptools

setuptools.setup(
    name='finformula',
    version='0.0.2',
    author='Ding',
    author_email='dingxuechun@hotmail.com',
    description='Testing installation of Package',
    url='https://git03.hundsun.com/AIQA/aiqa-ie/tree/dev/finformula',
    license='MIT',
    packages=['finformula'],
    install_requires=
    ['numpy==1.16.6', 'pandas==1.1.5',
     'scipy==1.5.4', 'pymssql==2.1.4',
     'sqlalchemy==1.3.18'
     ],
)

