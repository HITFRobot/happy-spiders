# -*- coding:utf-8 -*-  
__author__ = 'conghuai'
import re


def clean_text(text):
    text = re.sub('\s', '', text)
