"""Установщик зависимостей для работы фреймворка MFP"""
from os import path, system

if sys.platform == 'Windows':
    p = 'pip'
else:
    p = 'pip3'
system(f'{p} install requirements.tx')