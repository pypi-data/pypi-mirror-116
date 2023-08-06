from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.0'
DESCRIPTION = 'Just a Simple PushBullet Wrapper for Organisational use'
LONG_DESCRIPTION = 'Just a Simple PushBullet Wrapper for Organisational use, Still under development.'

# Setting up
setup(
    name="pbskrishna",
    version=VERSION,
    author=" abhinanddreddrive (Red Drive)",
    author_email="<abhi.at.gaming@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pushbullet.py','pyodbc','requests','pyautogui'],
    keywords=['python', 'hello','krishna','garments'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)