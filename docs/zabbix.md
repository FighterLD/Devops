#Zabbix监控部署
[TOC]
##1. 服务端安装

###1.1 下载zabbix 服务端 安装包
```
#  mkdir /data && cd /data
# wget http://repo.zabbix.com/zabbix/3.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_3.0-1+trusty_all.deb
# dpkg -i zabbix-release_3.0-1+trusty_all.deb
# apt-get update
```

###1.2 安装所需依赖插件（mysql+web）
```
# apt-get install zabbix-server-mysql zabbix-frontend-php
```

###1.3 mysql数据库初始化及创建zabbix所需账号
```
# groupadd zabbix
# useradd -r -s /sbin/nologin -g zabbix zabbix

# mysqladmin -uroot password ‘pinbot123'
#  mysql -uroot -p ‘pinbot123'（登陆数据库）
mysql>create database zabbix character set utf8 collate utf8_bin;
mysql>grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';
mysql>flush privileges;

注：-S /data/mysql/data/mysql.sock 是指定mysql.sock文件路径
```

###1.4 修改web端 PHP配置文件
```
#  vim /etc/php5/apache2/php.ini
date.timezone = Asia/Shanghai
max_execution_time = 300
post_max_size = 32M
max_input_time=300
memory_limit = 128M
mbstring.func_overload = off
always_populate_raw_post_data = -1

# cp -r /usr/share/zabbix /var/www/html/zabbix

注：拷贝操作是web界面能访问的关键
```

###1.5 导入zabbix所需数据库
```
# cd /usr/share/doc/zabbix-server-mysql
# zcat create.sql.gz | mysql -uroot -p’pinbot123’
```

###1.6 服务端配置
```
# vim /etc/zabbix/zabbix_server.conf
DBName=zabbix 数据库名称
DBUser=zabbix 数据库用户
DBPassword=zabbix 数据库密码
ListenIP=localhost #数据库IP地址，一般为默认
AlertScriptsPath=/usr/lib/zabbix/alertscripts    #运行脚本存放路径
```

###1.7 服务端启动
```
# /etc/init.d/zabbix-server start
```

##2. 客户端安装
###2.1 客户端安装包下载
```
# apt-get install zabbix-agent
```

###2.2 客户端配置
```
注意：zabbix_agentd.conf 是客户端的配置文件，这里配置的目的是对自身进行监控，此处的192.168.0.192是服务端的IP

# vim /etc/zabbix/zabbix_agentd.conf
Server=192.168.0.192        # 监控服务器的IP
ListenPort=10050            # 监听的端口
StartAgents=1               # 启动的客户端进程
ServerActive=192.168.0.192：10051  # 主动模式下的监控服务器IP（主动模式必须）
/tmp/zabbix_agentd.log                       #修改日志路径
UnsafeUserParameters=1                    #默认是不启用自定义脚本功能的，需开启
Hostname=zabbix.com         #监控服务器的名称，大小写敏感（主动模式必须），邮件报警时需要用到
```

###2.3 客户端启动
```
# /etc/init.d/zabbix-agent start
```

###2.4 加入开机自启动
```
# cp /usr/sbin/zabbix_server /etc/rc.d/init.d/zabbix_server
# cp /usr/sbin/zabbix_agentd /etc/rc.d/init.d/zabbix_agentd
# chmod +x # /etc/rc.d/init.d/zabbix_server
# chmod +x # /etc/rc.d/init.d/zabbix_agentd
```

##3. web端访问zabbix
访问地址：[http://192.168.0.192/zabbix](http://192.168.0.192/zabbix) #http://服务器地址或域名/zabbix  
默认用户名：admin  默认密码：zabbix
