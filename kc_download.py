#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File   : download.py
@Author : DEADF1SH_CAT
@Date   : 2020/06/01 15:03

Description:
    用于一键下载看云上面的markdown文件，并根据目录结构自动生成文件夹
Usage:
    $python kc_download.py -u https://www.kancloud.cn/alex_wsc/android/401651
'''

import os
import sys
import re
import json
import requests
import argparse
import platform
from bs4 import BeautifulSoup

class KanCloud():
    
    def __init__(self,url):
        self.url = url
        self.base_url = parse_url(self.url)
        self.data = self.get_data(self.url)
        self.flag = self.get_os()
        self.create()

    @staticmethod
    def get_os():
        if platform.system() == 'Windows':
            return '\\'
        elif platform.system() == 'Darwin' or platform.system() == 'Linux':
            return '/'

    def get_summary(self,data):
        return self.data['summary']

    @staticmethod
    def get_data(url):
        data = requests.get(url).text
        result = parse_html(data)

        return result
    
    def create(self):
        print("[+]Start KanCloud Downloader")
        print("[+]Target Article: " + self.data['config']['title'])
        base_path = get_path()
        mk_dir = base_path + self.flag + self.data['config']['title']
        make_path(mk_dir)
        print("[+]Downloading...")
        for table in self.data['summary']:
            self.isArt(table,mk_dir)
        print("[+]DOwnload Success!")

    def isArt(self,table,mk_dir):
        try:
            file_name = mk_dir + self.flag + table['name']
            make_file(file_name,self.get_content(table['id']))
            if table['articles']:
                art_path = mk_dir + self.flag + table['title']
                make_path(art_path)
                for art in table['articles']:
                    file_path = art_path + self.flag + art['name']
                    content = self.get_content(art['id'])
                    make_file(file_path,content)
                    self.isArt(art,art_path)
        except KeyError:
            pass

    def get_content(self,id):
        url = self.base_url + str(id)
        data = self.get_data(url)
        
        return data['article']['content']

def parse_url(url):
    base_url = re.findall('^.*\/',url)
    
    return base_url[0]

def parse_html(html_data):
    soup = BeautifulSoup(html_data,'lxml')
    data = json.loads(soup.find_all("script",type="application/payload+json")[0].string)
    
    return data

def get_path():
    dir_path = os.getcwd()
    
    return dir_path

def make_path(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def make_file(path,content):
    isExists = os.path.exists(path)
    if not isExists:
        with open(path,'w+',encoding="utf-8") as f:
            f.write(content)
            f.close()
            return True
    else:
        return False

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='KanCloud Downloader',add_help=True)
    parser.add_argument('-u','--url',default=None,help='目标URL',type=str)
    args = parser.parse_args()

    if args.url:
        try:
            kc = KanCloud(args.url)
        except:
            print("Args error! Please check the target url!")
            exit()