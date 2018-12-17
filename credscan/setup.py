"""
Defines how pip should install this module
"""

from setuptools import setup


setup(
    name='pylint-cred-scanner',
    description='Naively scans python code for credentials',
    author='Sean Usher',
    author_email='seusher@microsoft.com',
    version='0.10',
    download_url='https://github.com/seushermsft/CSEBoulder',
    install_requires=[
        'pylint',
    ],
    packages=[
        '',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ]
)
