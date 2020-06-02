# KanCloud_Downloader

## 简介

基于python3.7

用于一键下载看云上面的Markdown文件，并且会自动根据目录结构，生成子文件夹

会默认在该py脚本当前目录生成下载文件

## 依赖

```cmd
$pip install -r requirements.txt
```

## 使用方法

```cmd
$python kc_download.py -u [target_url]
eg:
$python kc_download.py -u https://www.kancloud.cn/alex_wsc/android/401651
[+]Start KanCloud Downloader
[+]Target Article: Android知识技能必备
[+]Downloading...
[+]DOwnload Success!
```

## TODO

- 自定义指定目录生成文件
- 一键合成文件包括优化目录显示