#coding=utf-8

"""
Author: chenruotian
Description: 远程mongodb数据导入到本地mongodb
    (方式:多表,不支持整库.
     原因1：有些表数据量非常大, 导出导入容易出错; 原因2：system.indexes表和system.users表不需要导出, 且导出会报权限错误)
Note: 该fabfile在目标mongodb所在机器上执行
Usage: fab -f fabfile_mongo.py connect_remote_mongohost mongo_dump_restore:username_from='root',password_from='xxx',db_from='recruiting',collection_from='tag',datadir_from='/media/data/mongo/mongodata/',hostuser_from='root',username_local='root',password_local='xxx',db_local='recruiting',collection_local='tag'
"""
from fabric.api import run, local, env, abort, cd


def connect_remote_mongohost(remote_host='10.160.24.216', ssh_port=22):
    """设置远程mongo host and user
    """
    env.hosts = ['%s:%d' % (remote_host, ssh_port)]
    env.user = 'root'

def _remote_mongodump(host='localhost', port=27017, username='', password='', authendb='admin', db='', collection='', out='/media/data/mongo/mongodata/'):
    """远程mongo导出到其本地,或从指定的mongo host导出
    单表导出
    Note: mongo账号需要超级权限

    导出单个表：
    mongodump --host 112.124.23.240 --port 27017 --username root --password pinbot-Letsdoit --authenticationDatabase admin --db recruiting --collection tag --directoryperdb --out /media/data/mongo/mongodata/
    """
    if not db:
        abort('Abort for no db specified.')
    if not collection:
        abort('Abort for no collection specified.')
    run('mkdir -p %s' % out)
    with cd(out):
        mongodump_cmd = 'mongodump --host %s --port %d --username %s --password %s --authenticationDatabase %s --db %s --collection %s --directoryperdb --out %s' % (host, port, username, password, authendb, db, collection, out)
        run(mongodump_cmd)

def _local_scpdata(username, local_datadir, remote_datapath):
    """从mongodb主机上远程拷贝数据文件夹
    scp -r root@10.160.24.216:/media/data/mongo/mongodata/recruiting/tag.* /media/data/mongo/mongodata/recruiting/
    """
    local('mkdir -p %s' % local_datadir)
    host = env.hosts[0].split(':')[0]
    scp_cmd = 'scp -r %s@%s:%s %s' % (username, host, remote_datapath, local_datadir)
    local(scp_cmd)

def _local_mongorestore(host='localhost', port=27017, username='', password='', authendb='admin', db='', collection='', datapath=''):
    """将本地数据导入本地mongodb
    mongorestore -h 112.124.4.196 --port 27017 -u root -p pinbot-hopperclouds-4096-196 --authenticationDatabase admin -d recruiting -c tag --drop /media/data/mongodata/recruiting/tag.bson
    """
    if not db:
        abort('Abort for no db specified.')
    if not collection:
        abort('Abort for no collection specified.')
    if not datapath:
        abort('Abort for no datapath specified.')
    mongorestore_cmd = 'mongorestore -h %s --port %d -u %s -p %s --authenticationDatabase %s -d %s -c %s --drop %s' % (host, port, username, password, authendb, db, collection, datapath)
    local(mongorestore_cmd)

def mongo_dump_restore(username_from='root', password_from='', db_from='', collection_from='', datadir_from='/media/data/mongo/mongodata/',
                       hostuser_from='', datadir_local='/media/data/mongo/mongodata/', username_local='root',
                       password_local='', db_local='', collection_local=''):
    """从远程mongo导出数据到本地mongo
    """
    # remote
    _remote_mongodump(username=username_from, password=password_from, db=db_from, collection=collection_from, out=datadir_from)
    # local
    remote_datapath = '%s/%s/%s.*' % (datadir_from, db_from, collection_from)
    local_datadir = '%s/%s' % (datadir_local, db_local)
    _local_scpdata(hostuser_from, local_datadir, remote_datapath)
    # local
    local_datapath = '%s/%s.bson' % (local_datadir, collection_from)
    _local_mongorestore(username=username_local, password=password_local, db=db_local, collection=collection_local, datapath=local_datapath)