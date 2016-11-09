# 集群部署

1. 集群地址：[https://github.com/elastic/elasticsearch](https://github.com/elastic/elasticsearch)
2. Fork到自己的项目中，得到项目地址为：[https://github.com/FighterLD/elasticsearch](https://github.com/FighterLD/elasticsearch)
3. clone代码到需要部署的Linux服务器
```
#--depth 1 表示取最近一次修改的项目
git clone --depth 1 https://github.com/FighterLD/elasticsearch.git
```

4. elasticsearch配置信息
```
mv elasticsearch-rtf-2.2.0 elasticsearch-rtf
cd elasticsearch-rtf
vim config/elasticsearch.yml
#集群显示名 配置前需空一格
 cluster.name: pinbot-220   #pinbot-220
 network.bind_host: "0.0.0.0"
 network.publish_host: "192.168.0.222"   #设置对外访问的IP
 discovery.zen.ping.multicast.enabled: false    #设置禁止广播查找同网段集群
 discovery.zen.ping.unicast.hosts: ["192.168.0.220", "192.168.0.224"]  #设置集群中其他节点IP
```

5. supervisor守护进程配置
```
#添加supervisor启动信息
vim supervisor.elasticsearch.conf
[program:elasticsearch]
command=/home/bigdata/github/elasticsearch-rtf/bin/elasticsearch -Dnetwork.host=0.0.0.0
directory=/home/bigdata/github/elasticsearch-rtf
user=bigdata
;environment=JAVA_OPTS="-Xmx64m -Xms32m",ES_MIN_MEM=32m,ES_MAX_MEM=64m
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/data/supervisor/elasticsearch/logs/supervisor.out.log
stderr_logfile=/data/supervisor/elasticsearch/logs/supervisor.out.err
```

6. 日志目录创建
 ```
mkdir -p /data/supervisor/elasticsearch/logs
```

7. 启动Supervisor进程并拉起集群
```
supervisord -c /home/bigdata/github/elasticsearch-rtf/supervisor.elasticsearch.conf
```

8. 同步集群到其他节点
```
sudo scp -r /home/bigdata/github/elasticsearch-rtf bigdata@192.168.0.220:~/github/
sudo scp -r /home/bigdata/github/elasticsearch-rtf bigdata@192.168.0.224:~/github/
注：同步后需要：
1、修改elasticsearch配置信息中的 network.publish_host: "192.168.0.222"   #设置对外访问的IP
2、启动Supervisor进程并拉起集群
```

9. 给集群加上Git源
```
git remote add origin https://github.com/wwwa/elasticsearch-rtf.git --fetch
```

10. 集群后台管理
[http://192.168.0.222:9200/_plugin/rtf/](http://192.168.0.222:9200/_plugin/rtf/)



