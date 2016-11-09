#!/usr/bin/env python
#coding:utf-8
'''
Created on 2016年8月28日

@author: liudong

主要实现本地文件打包,上传,校验,解压等功能

'''

from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user='bigdata'
env.hosts=['192.168.0.214','192.168.0.216']
env.password='POILKJ,mn'


@task
@runs_once
def tar_task():            #本地打包函数,runs_once 代表只限执行一次
    with lcd("/Users/liudong/github"):
        local("tar -zcf IDC.tar.gz IDC")

@task
def put_task():            #上传文件任务函数
    run("mkdir -p /data/github")
    with cd("/data/github"):
        with settings(warn_only=True):         #put上传出现异常时继续执行,而非终止任务
            #将本地IDC.tar.gz拷贝到远程机器
            result = put("/Users/liudong/github/IDC.tar.gz","/data/github/IDC.tar.gz")
        if result.filed and not confirm("put file failed, Continue[Y/N]?"):
            abort("Aborting file put task!")   #出现异常时,确认用户是否继续,(Y继续)
@task
def check_task():          #校验文件任务函数
    with settings(warn_only=True):
        #本地local命令需要配置capture=True 才能获取返回值
        lmd5=local("md5 /Users/liudong/github/IDC.tar.gz",capture=True).split(' ')[3]
        #MAC系统中md5命令获取文件md5码,注意是第4部分才是md5值,后面下标为3
        rmd5=run("md5sum /data/github/IDC.tar.gz").split(' ')[0]
    if lmd5==rmd5:
        print "OK"
        with cd("/data/github"):
            with run("rm -fr IDC"):
                run("tar -zxf IDC.tar.gz")
    else:
        print "tar file md5 Error"
@task
def go():                 #设置只有go函数对fab命令可见,后面执行时,直接fab -f simple.py go  实现本地本文件打包,上传,校验全程自动化
    tar_task()
    put_task()
    check_task()