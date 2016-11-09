 Mysql授权
```
grant all privileges on *.* to root@localhost identified by 'A123!@#b200' with grant option;  #对root用户访问本地授权所有权限，密码为A123!@#b200
grant all privileges on *.* to root@'%' identified by 'A123!@#b200' with grant option;    #对root用户访问所有IP授权所有权限，密码为A123!@#b200
grant select,create,alter on *.* to  pinbot@'%' identified by 'pinbot123' with grant option;   #对pinbot用户授权所有IP查询、创建权限，密码为pinbot123
```

Mysql备份
```
mysqldump -u root -p --all-databases > all-databases.sql   #备份所有库
```
```
Plugin 'FEDERATED' is disabled.
^G/usr/sbin/mysqld: Can't find file: './mysql/plugin.frm' (errno: 13 - Permission denied)
[ERROR] Can't open the mysql.plugin table. Please run mysql_upgrade to create it.
```



```
Can't create test file /data/mysql/server2.lower-test
Can't create test file /data/mysql/server2.lower-test
```

修改mysql默认使用的数据文件路径的权限
```
vim  /etc/apparmor.d/usr.sbin.mysqld
  /var/lib/mysql/ r,
  /var/lib/mysql/** rwk,
  /media/mysql/ r,
  /media/mysql/** rwk,
```
重启apparmor服务
```
  sudo service apparmor restart
```
```
Plugin 'FEDERATED' is disabled.
/usr/local/Cellar/mysql/5.6.15/bin/mysqld: Can't find file: './mysql/plugin.frm' (errno: 13 - Permission denied)
2014-01-31 00:03:03 13223 [ERROR] Can't open the mysql.plugin table. Please run mysql_upgrade to create it.
2014-01-31 00:03:03 13223 [Note] InnoDB: The InnoDB memory heap is disabled
2014-01-31 00:03:03 13223 [Note] InnoDB: Mutexes and rw_locks use GCC atomic builtins
2014-01-31 00:03:03 13223 [Note] InnoDB: Compressed tables use zlib 1.2.3
2014-01-31 00:03:03 13223 [Note] InnoDB: Using CPU crc32 instructions
2014-01-31 00:03:03 13223 [Note] InnoDB: Initializing buffer pool, size = 128.0M
2014-01-31 00:03:03 13223 [Note] InnoDB: Completed initialization of buffer pool
2014-01-31 00:03:03 13223 [ERROR] InnoDB: ./ibdata1 can't be opened in read-write mode
```


从innodb_force_recovery的值1开始尝试，看mysql能否在该修复模式下启动，不要尝试值为4及以上。
在我这里，mysql在值为2时可以启动，这是stop掉数据库，然后备份数据
```
vim /etc/mysql/my.cnf
innodb_force_recovery = 2
```
```
sudo service mysql stop
mysqldump -u root -p --all-databases > all-databases.sql
```
删除掉出错的数据文件
```
mv ib_logfile0 ib_logfile0.bak
mv ib_logfile1 ib_logfile1.bak
mv ibdata1 ibdata1.bak
```
启动mysql，然后从备份文件恢复数据
```
sudo service mysql start
mysql -u root -p < all-databases.sql

因为在修复模式下，在插入数据时报错，也就是说此时是不能写入数据的。所以就关闭掉了修复模式
```
vim /etc/mysql/my.cnf
innodb_force_recovery = 0
```
restart mysql后，再次恢复数据
```
sudo service mysql restart
mysql -u root -p < all-databases.sql
```
```
Mysql初始化服务器
```
mysql_install_db - u mysql  or  mysql_upgrade -u
```
```
rm -rf /var/lib/mysql
mysql_install_db --user=mysql --no-defaults --datadir=/var/lib/mysql
sudo chown -R mysql:mysql /var/lib/mysql
sudo chmod 755 /var/lib/mysql
```