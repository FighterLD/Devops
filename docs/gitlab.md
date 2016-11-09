#开源版本系统Gitlab部署文档
[TOC]
[开源版本控制系统Gitlab官方安装文档](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/install/installation.md)
##1. 安装软件包及依赖库

###1.1 安装前准备
```
# run as root! 		  	用root用户运行
apt-get update -y  	 	#更新系统安装源
apt-get upgrade -y  		#更新已安装的软件包
apt-get install sudo -y 	#安装sudo，后续会用到
```
###1.2 安装系统必要的软件包
```
sudo apt-get install -y build-essential zlib1g-dev libyaml-dev libssl-dev libgdbm-dev libreadline-dev libncurses5-dev libffi-dev curl openssh-server redis-server checkinstall libxml2-dev libxslt-dev libcurl4-openssl-dev libicu-dev logrotate python-docutils pkg-config cmake nodejs
```
如果你要用Kerberos来验证用户，需要另外安装libkrb5-dev:
```
sudo apt-get install libkrb5-dev
```
###1.3 安装最新版git和邮件服务
```
# 安装Git
sudo apt-get install -y git-core
# 检查git的版本,确保git版本不小于1.7.10
git --version
```
如果系统包里的git版本过旧，可以删除系统自带的，然后用源码编译最新的git。
```
# 删除git
sudo apt-get remove git-core
# 安装依赖
sudo apt-get install -y libcurl4-openssl-dev libexpat1-dev gettext libz-dev libssl-dev build-essential
# 下载并编译源码
cd /tmp
curl -L --progress https://www.kernel.org/pub/software/scm/git/git-2.4.3.tar.gz | tar xz
cd git-2.4.3/
./configure
make prefix=/usr/local all
# 安装到/usr/local/bin目录
sudo make prefix=/usr/local install
# 当编辑config/gitlab.yml(step 5),修改git路径为/usr/local/bin/git
```
注意:为了让Gitlab拥有发送通知邮件的功能,你需要安装一个邮件服务.在Debian系统上默认自带一个exim4的附件,但是Ubuntu上并没有附带这个.Ubuntu上可以安装Postfix来发送邮件.
```
sudo apt-get install -y postfix
```
然后选择Internet Site回车后再确认下主机名。

##2. Ruby环境安装
###2.1 安装Ruby环境
在Gitlab生产环境使用Ruby版本管理工具RVM，rbenv或者chruby常常会带来很多疑难杂症。
比如Gitlab-shell版本管理器调用OpenSSH的功能以防止越过ssh对仓库进行pull和push操作。
而前面提到的三个版本管理器不支持这样的功能,所以强烈建议大家按照下面的方式来安装Ruby。
如果系统上存在旧的Ruby1.8，先删除掉:
```
sudo apt-get remove ruby1.8
```
下载Ruby源码,编译安装:
```
mkdir /tmp/ruby && cd /tmp/ruby
# 这里替换官方文档的下载地址为ruby.taobao.com提供的镜像地址
curl -O --progress http://mirrors.ustc.edu.cn/ruby/2.2/ruby-2.2.2.tar.gz
tar xzf ruby-2.2.2.tar.gz
cd ruby-2.2.2
./configure --disable-install-rdoc
make
sudo make install
```
###2.2 修改Gem安装源
国内使用Ruby的Gem和Bundler必须要做的事情:
```
# 修改gem安装源为淘宝源
$ sudo gem sources --add https://gems.ruby-china.org/ --remove https://rubygems.org/
$ sudo  gem sources -l
*** CURRENT SOURCES ***

https://gems.ruby-china.org/
```
###2.3 安装Bundler Gem:
```
sudo gem install bundler --no-ri --no-rdoc
# 修改bundler的源为淘宝源,执行这一步前先添加git用户,参照本文第4条""创建系统用户"
sudo -u git -H bundle config mirror.https://rubygems.org https://gems.ruby-china.org/
```
##3. Go编辑器安装
从Gitlab8.0开始，Git的HTTP请求由gitlab-git-http-server来处理。需要Go编译器来安装gitlab-git-http-server。
下面一系列的指令都是针对64位的Linux系统。也可以在GoLang官方网站下载其他平台的Go编译器。
```
mkdir /tmp/go && cd /tmp/go
curl -O --progress http://www.golangtc.com/static/go/go1.5.1/go1.5.1.linux-amd64.tar.gz
echo '46eecd290d8803887dec718c691cc243f2175fe0  go1.5.1.linux-amd64.tar.gz' | shasum -c - && \
    sudo tar -C /usr/local -xzf go1.5.1.linux-amd64.tar.gz
sudo ln -sf /usr/local/go/bin/{go,godoc,gofmt} /usr/local/bin/
rm go1.5.1.linux-amd64.tar.gz
```
##4. 系统用户创建
为GitLab创建一个名为git的用户:
```
sudo adduser --disabled-login --gecos 'GitLab' git
```
##5. 数据库安装
Gitlab官方建议用PostgreSQL数据库。如果喜欢用Mysql请前往Gitlab使用Mysql数据库的安装说明。
注意:Gitlab使用的部分扩展插件需要PostgreSQL版本至少为9.1。
###5.1 安装PostgreSQL数据库软件包(PostgreSQL和MySQL数据库二选一)
```
# 安装PostgreSQL数据库软件包
sudo apt-get install -y postgresql postgresql-client libpq-dev

# 使用系统用户postgres登录到PostgreSQL,目标数据库为template1
sudo -u postgres psql -d template1

# 为Gitlab创建一个用户
# 不要输入 'template1=#'，这是PostgreSQL的提示符
template1=# CREATE USER git CREATEDB;

# 创建Gitlab生产环境数据库并赋予git用户属主权限
template1=# CREATE DATABASE gitlabhq_production OWNER git;

# 退出数据库会话
template1=# \q

# 用git用户测试下是否能登录刚才创建的数据库
sudo -u git -H psql -d gitlabhq_production

# 退出数据库会话
gitlabhq_production> \q
```
###5.2 安装MySQL数据库软件包
```
# 安装MySQL数据库软件包
sudo apt-get install -y mysql-server mysql-client libmysqlclient-dev

# 确认MySQL 在 5.5.14 版本以上
mysql --version

# 初始化 MySQL 设置
sudo mysql_secure_installation

# 设置 MySQL root 账号密码

mysqladmin -u root -p password 'gitlab123'

# 登录 MySQL
mysql -u root -p

# 用root密码登录

# 创建gitlab账号及对本地授权，设置密码
mysql> CREATE USER 'git'@'localhost' IDENTIFIED BY '$password';

# 确认可以使用 InnoDB engine，后续需要用到
# If this fails, check your MySQL config files (e.g. `/etc/mysql/*.cnf`, `/etc/mysql/conf.d/*`) for the setting "innodb = off"
mysql> SET storage_engine=INNODB;

#创建 GitLab 数据库
mysql> CREATE DATABASE IF NOT EXISTS `gitlabhq_production` DEFAULT CHARACTER SET `utf8` COLLATE `utf8_unicode_ci`;

# 授予数据库的用户GitLab必要的权限
mysql> GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, LOCK TABLES ON `gitlabhq_production`.* TO 'git'@'localhost';

# 退出数据库
mysql> \q

# 尝试连接到新的数据库的新用户
sudo -u git -H mysql -u git -p -D gitlabhq_production

# 键入密码，您与早期替换 $password

# 会出现 'mysql>' prompt

# Quit the database session
mysql> \q

```
##6. Redis环境安装
GitLab 至少需要Redis 2.8，如果使用的是Debian8或Ubuntu14.04及以上，那么可以简单地安装Redis 2.8搭配：
###6.1 安装Redis
```
sudo apt-get install redis-server
```
###6.2 设置Socket及TCP端口监听
```
# 配置redis使用socket来监听
sudo cp /etc/redis/redis.conf /etc/redis/redis.conf.orig

# 把'post'设置为0以禁止监听TCP端口
sed 's/^port .*/port 0/' /etc/redis/redis.conf.orig | sudo tee /etc/redis/redis.conf
# Enable Redis socket for default Debian / Ubuntu path
echo 'unixsocket /var/run/redis/redis.sock' | sudo tee -a /etc/redis/redis.conf
```
###6.3 Redis用户组授权
```
# 给redis用户组的所有成员授权
echo 'unixsocketperm 770' | sudo tee -a /etc/redis/redis.conf
```
###6.4 创建Socket目录
```
# 创建存放socket的目录
mkdir /var/run/redis
sudo chown redis:redis /var/run/redis
sudo chmod 755 /var/run/redis

if [ -d /etc/tmpfiles.d ]; then
  echo 'd  /var/run/redis  0755  redis  redis  10d  -' | sudo tee -a /etc/tmpfiles.d/redis.conf
fi
```
###6.5 替换新的Redis配置文件
```
# 应用新的 redis.conf
sudo service redis-server restart

# 把git用户加入redis组
sudo usermod -aG redis git
```

##7. Gitlab设置
###7.1 Gitlab初始化安装

####7.1.1 安装gitlab的home目录
```
将gitlab安装到git用户的HOME目录
cd /home/git
```
####7.1.2 克隆Gitlab源码
```
# 克隆GIT@OSC上的Gitlab源码
sudo -u git -H git clone https://git.oschina.net/qiai365/gitlab-ce.git -b 8-1-stable gitlab
```
####7.1.3 配置Gitlab
```
# 进入Gitlab安装目录
cd /home/git/gitlab

# 创建Gitlab主配置文件'gitlab.yml'
sudo -u git -H cp config/gitlab.yml.example config/gitlab.yml

# 更新配置文件
sudo -u git -H vim config/gitlab.yml

# 创建 secrets 配置文件
sudo -u git -H cp config/secrets.yml.example config/secrets.yml
sudo -u git -H chmod 0600 config/secrets.yml

# 修改log/和tmp的权限
sudo chown -R git log/
sudo chown -R git tmp/
sudo chmod -R u+rwX,go-w log/
sudo chmod -R u+rwX tmp/

# 修改 tmp/pids/ 和 tmp/sockets/ 的权限
sudo chmod -R u+rwX tmp/pids/
sudo chmod -R u+rwX tmp/sockets/

# 修改public/uploads/ 权限
sudo -u git -H mkdir -p public/uploads
sudo chmod -R u+rwX  public/uploads

# 修改CI编译和存储目录的权限
sudo chmod -R u+rwX builds/

# 创建 Unicorn 配置文件
sudo -u git -H cp config/unicorn.rb.example config/unicorn.rb

# 查询CPU核心数
nproc

# 如果你想搭建一个高负载的Gitlab实例,可启用集群模式.
# 修改'worker_processes'参数,至少要跟cpu核心数一样.
# 举例:为2G RAM的服务器修改workers数量为3
sudo -u git -H vim config/unicorn.rb

# 创建Rack attack 配置文件
sudo -u git -H cp config/initializers/rack_attack.rb.example config/initializers/rack_attack.rb

# Configure Git global settings for git user, used when editing via web editor
sudo -u git -H git config --global core.autocrlf input

# 配置 Redis 选项
sudo -u git -H cp config/resque.yml.example config/resque.yml

# 如果之前修改过redis socket的路径，在这个配置文件里面修改为当前的路径.
sudo -u git -H vim config/resque.yml
```
重要提示: 一定要按照你自己的情况修改gitlab.yml和unicorn.rb

####7.1.4 修改Gitlab 数据库设置
```
# 此命令仅针对PostgreSQl:
sudo -u git cp config/database.yml.postgresql config/database.yml

# 此命令仅针对MySQL:
sudo -u git cp config/database.yml.mysql config/database.yml

# 以下修改针对MySQL和远程PostgreSQL:
# 修改username/password.
# 生产环境只需要修改第一部分即可.
# 修改'secure password' 为你设置的密码
# 密码字段可以使用"双引号" 
sudo -u git -H editor config/database.yml

# PostgreSQL MySQL都适用:
# 修改database.yml的权限,确保git用户可以读取该文件.
sudo -u git -H chmod o-rwx config/database.yml
```
###7.2 Gitlab 内部依赖安装
####7.2.1 安装Gems
Note: 自bundler1.5.2起,你可以使用bundle install -jN(N就是cpu核心数)安装Gems,速度比之前要快大约60%.详细的内容可以点此处查看.不过首先要确保你的bundler版本>=1.5.2(运行bundle -v查看)。
```
# PostgreSQL 环境
sudo -u git -H bundle install --deployment --without development test mysql aws kerberos

# MySQL 环境
sudo -u git -H bundle install --deployment --without development test postgres aws kerberos
```
####7.2.2 安装GitLab Shell 命令行
GitLab Shell是专为GitLab开发的ssh访问和仓库管理的软件。
```
# 运行安装gitlab shell 的任务 (根据自己的redis安装情况修改`REDIS_URL`),这里如果你事先没有clone gitlab-shell的仓库,就会自动clone官方的仓库进行安装:
sudo -u git -H bundle exec rake gitlab:shell:install[v2.6.6] REDIS_URL=unix:/var/run/redis/redis.sock RAILS_ENV=production

# 默认情况下,gitlab-shell的配置是根据Gitlab的配置生产的.
# 你可以运行下面的命令查看和修改gitlab-shell的配置:
sudo -u git -H vim /home/git/gitlab-shell/config.yml
```
确保您的主机可以在机器上通过任何合适的DNS记录或在附加行/ etc / hosts文件（“127.0.0.1主机名”）来解决。如果设置了gitlab背后一个反向代理，这可能是必要的例子。如果主机名无法解析，最后安装检查将失败，并“检查GitLab API访问：失败。 code: 401” and pushing commits will be rejected with “[remote rejected] master -> master (hook declined)”.

####7.2.3 安装gitlab-git-http-server
```
cd /home/git
sudo -u git -H git clone https://gitlab.com/gitlab-org/gitlab-git-http-server.git
cd gitlab-git-http-server
sudo -u git -H git checkout 0.3.0
sudo -u git -H make
```
###7.3 初始化数据库，激活高级特性
```
# 进入Gitlab安装目录

cd /home/git/gitlab

sudo -u git -H bundle exec rake gitlab:setup RAILS_ENV=production

# 输入 'yes' 来创建数据库表.
# 初始化完成后,会显示 'Administrator account created:',这里会输出默认账号和密码

Administrator account created:

login.........root
password......5iveL!fe
```
Note:你也可以设置环境变量GITLAB_ROOT_PASSWORD，这样在初始数据库的时候就会使用你指定的密码,否则就是上面的默认密码。
```
sudo -u git -H bundle exec rake gitlab:setup RAILS_ENV=production GITLAB_ROOT_PASSWORD=yourpassword
```
###7.4 安全设置 secrets.yml

secrets.yml文件为每个会话和安全变量存储密钥.把这个文件备份到别的地方，但是不要和数据库备份放在一块，否则你的数据库备份损坏会导致这个文件丢失。

###7.5 Gitlab 优化设置
####7.5.1 安装Gitlab启动脚本
```
sudo cp lib/support/init.d/gitlab /etc/init.d/gitlab
sudo cp lib/support/init.d/gitlab.default.example /etc/default/gitlab
```
####7.5.2 设置Gitlab为开机自启动
```
sudo update-rc.d gitlab defaults 21
```
####7.5.2 配置Logrotate
```
sudo cp lib/support/logrotate/gitlab /etc/logrotate.d/gitlab
```
####7.5.3 检查应用状态
```
sudo -u git -H bundle exec rake gitlab:env:info RAILS_ENV=production
```
####7.5.4 编译生成资源文件(Assets)
```
sudo -u git -H bundle exec rake assets:precompile RAILS_ENV=production
```
####7.5.5 启动Gitlab实例
```
sudo service gitlab start  #或者下面这种启动方式
sudo /etc/init.d/gitlab restart
```
##8. Nginx设置
Nginx的是GitLab正式支持的Web服务器。如果你不能或不想使用Nginx的作为Web服务器，可以看[官方文档](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/install/installation.md#using-https)

###8.1 安装nginx
```
sudo apt-get install -y nginx
```
###8.2 设置GitLab 的虚拟主机配置文件
```
sudo cp lib/support/nginx/gitlab /etc/nginx/sites-available/gitlab
sudo ln -s /etc/nginx/sites-available/gitlab /etc/nginx/sites-enabled/gitlab

sudo nginx -t
```

如果使用https，则参考[https官方文档](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/install/installation.md#using-https)
```
# 重启
sudo service nginx restart
nginx -t
```
##9. 安装及使用中遇到的问题及解决方法
###9.1 安装需要注意事项
####9.1.1 安装状态查看
注意安装数据库之前一定修改数据库配置文件config/database.yml里的用户名和密码，不要用root用户。使用如下命令查看gitlab安装状态
```
cd ~gitlab/gitlab
sudo -u gitlab -H bundle exec rake gitlab:check RAILS_ENV=production
```
####9.1.2 迁移数据库到MySQL
导出现有数据
```
bundle exec rake db:data:dump RAILS_ENV=production
```
修改数据库配置
```
#修改数据库配置文件config/database.yml
# backup old database settings first
cp config/database.yml config/database.yml.old
cp config/database.yml.mysql config/database.yml
注：修改database.yml中mysql数据库的用户名和密码。
```
创建数据库
```
bundle exec rake db:setup RAILS_ENV=production
```
导入数据
```
bundle exec rake db:data:load RAILS_ENV=production
```
###9.2 git push出错
使用http协议推送比较大的文件时有可能出现如下错误:
```
error: RPC failed; result=22, HTTP code = 413 fatal: The remote end hung up unexpectedly
```
参考[issue#3099](https://github.com/gitlabhq/gitlabhq/issues/3099)里的讨论，需要在/etc/nginx/sites-available/gitlab里修改client_max_body_size的值。
```
# ... 
client_max_body_size 100M; 
# ...
```
使用有可能出现如下错误:
```
# git push origin master

Counting objects: 3, done.

Writing objects: 100% (3/3), 266 bytes | 0 bytes/s, done.

Total 3 (delta 0), reused 0 (delta 0)

remote: GitLab: API is not accessible

To http://gitlab.pinbot.me/likaiguo/test_gitlab.git

 ! [remote rejected] master -> master (pre-receive hook declined)

error: failed to push some refs to 'http://gitlab.pinbot.me/likaiguo/test_gitlab.git'
```
查看gitlab-shell日志发现：
```
tail -f /home/git/gitlab-shell/gitlab-shell.log
...
ERROR -- : API call <POST http://localhost//api/v3/internal/allowed> failed: 404
...
```
解决方法：
```
vim /home/git/gitlab-shell/config.yml  #修改gitlab_url
gitlab_url: http://gitlab.pinbot.me:8040
```

###9.3 修改工程的默认域名
使用默认设置新建的工程，域名都是localhost，修改gitlab/config/gitlab.yml，如下所示，将32行host改为需要的域名。
```
32     host: gitlab.pinbot.me
```
###9.4 迁移到Mysql时无法找到mysql2 adapter
使用命令bundle exec rake db:data:load RAILS_ENV=production初始化Mysql数据库时报以下错误:
```
rake aborted! Please install the mysql2 adapter: `gem install activerecord-mysql2-adapter` (mysql2 is not part of the bundle. Add it to Gemfile.)
```
按照提示安装activerecord-mysql2-adapter后依然报同样的错误。修改gitlab的Gemfile($GitlabRoot/Gemfile)，找到如下一句:
```
gem "mysql2", :group => :mysql
```
将其修改为
```
gem "mysql2", :group => :production
```
若依然无效，添加如下一行即可。
```
gem 'mysql2'
```
###9.5 sshd端口不是22
若sshd的端口不是22，则会遇到如下错误:
```
ssh: connect to host localhost port 22: Connection refused
```
此时，在/home/gitlab/.ssh/config文件中加入如下内容即可。
```
Host localhost Port 12345
```
###9.6 查看文件源码时出现500错误
pygments需要python2.6或python2.7，如果安装了python2.6或python2.7后依然出现该错误，则可能是因为pygments无法找到python2，执行如下命令即可解决，参考Error 500 while trying to see source file。
```
ln -s /usr/bin/python2.6 /usr/bin/python2
```
###9.7 Github 443报错
github443 Connection refused
```
# github443报错：
Connecting to github.com (github.com)|192.30.252.131|:443... failed: Connection refused.
```
解决方法：
```
echo "192.30.253.113 github.com" | sudo tee -a /etc/hosts
192.30.253.113 github.com
```