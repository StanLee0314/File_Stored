# Cloudera 3.6.1配置问题

1、修改主机名

```
sudo hostnamectl set-hostname foo-1.example.com
```

2、编辑 `/etc/hosts` 文件

```
1.1.1.1  foo-1.example.com  foo-1
2.2.2.2  foo-2.example.com  foo-2
3.3.3.3  foo-3.example.com  foo-3
4.4.4.4  foo-4.example.com  foo-4
1234
```

3、确认每个主机都是固定网络

a. 分别运行 `uname -a`和`hostname`，检查主机名是否一致

b. 运行`/sbin/ifconfig`，注意`eth0`中的`inet addr`的值，例如：

```
eth0      Link encap:Ethernet  HWaddr 00:0C:29:A4:E8:97  
          inet addr:172.29.82.176  Bcast:172.29.87.255  Mask:255.255.248.0
...
123
```

c. 运行`host -v -t A $(hostname)`，检查主机名是否和`hostname`命令输出一致，IP地址是否和`ifconfig`中的输出一致

```
Trying "foo-1.example.com"
...
;; ANSWER SECTION:
foo-1.example.com. 60 IN
A
172.29.82.176
123456
```

## 关闭防火墙

```
sudo systemctl stop ufw
sudo systemctl disable ufw
2） 重启服务
     Ubuntu: $sudo/etc/init.d/networking restart
```

## 设置SELinux模式

Ubuntu默认没有安装selinux-utils，如果没有selinux，可以跳过此步。

如果使用了selinux，请先关闭，安装CDH完成后，再开启。

## 设置时钟同步

cloudera manager需要ntp服务。需要安装。使用ntp做时钟同步的操作在这里不做描述，可以自行查找资料。

另外，Ubuntu内置支持了timedatectl，默认开启了时钟同步。可用来调整服务器时间。

查看

```
timedatectl
1
```

设置时区

```
sudo timedatectl set-timezone "Asia/Shanghai"
1
```

## ssh设置

1、允许root登陆

编辑`/etc/ssh/sshd_config`，找到修改配置 `PermitRootLogin yes`，使用`sudo systemctl restart ssh`重启ssh服务。

2、设置root密码

切换到root：`sudo su`

设置密码：`passwd`

## 搭建CM源

https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/cm_ig_create_local_package_repo.html#internal_package_repo_content

### 设置web服务

```
sudo apt-get install apache2
sudo systemctl start apache2
sudo systemctl enable apache2
123
```

### 下载并发布包仓库

```
sudo mkdir -p /var/www/html/cloudera-repos/cm6
wget https://archive.cloudera.com/cm6/6.3.1/repo-as-tarball/cm6.3.1-ubuntu1804.tar.gz
sudo tar xvfz cm6.3.1-ubuntu1804.tar.gz -C /var/www/html/cloudera-repos/cm6 --strip-components=1
cd /var/www/html/cloudera-repos/cm6
sudo wget https://archive.cloudera.com/cm6/6.3.1/allkeys.asc
sudo chmod -R ugo+rX /var/www/html/cloudera-repos/cm6
123456
```

此处注意版本ubuntu 1604 本次

### 配置并使用内部仓库

创建`/etc/apt/sources.list.d/cloudera-repo.list`文件，编辑内容如下：

```
deb http://<web_server>/cm <codename> <components>
1
```

可以从 `./conf/distributions` 找到 `<codename>` 和 `<components>`。

可以下载官方源文件进行参考：

```
sudo wget https://archive.cloudera.com/cm6/6.3.1/ubuntu1804/apt/cloudera-manager.list
1
```

完整示例如下：

```
# Cloudera Manager 6.3.1
deb [arch=amd64] http://foo-1.example.com/cloudera-repos/cm6 bionic-cm6.3.1 contrib
12
```

导入仓库签名GPG KEY，archive.key在上面本地源的cloudera-repos/cm6目录下:

```
sudo apt-key add archive.key
1
```

更新

```
sudo apt-get update
1
```

## 安装CM

安装jdk（每台机器都要安装）

```
sudo apt-get install openjdk-8-jdk
1
```

安装cm:

```
sudo apt-get install cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server
1
```

安装mariadb:

```
sudo apt-get install mariadb-server
1
```

停止mariadb

```
sudo systemctl stop mariadb
1
```

mariadb (mysql) 配置 /etc/mysql/conf.d/mysql.cnf：

```
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
transaction-isolation = READ-COMMITTED
# Disabling symbolic-links is recommended to prevent assorted security risks;
# to do so, uncomment this line:
symbolic-links = 0
# Settings user and group are ignored when systemd is used.
# If you need to run mysqld under a different user or group,
# customize your systemd unit file for mariadb according to the
# instructions in http://fedoraproject.org/wiki/Systemd

key_buffer = 16M
key_buffer_size = 32M
max_allowed_packet = 32M
thread_stack = 256K
thread_cache_size = 64
query_cache_limit = 8M
query_cache_size = 64M
query_cache_type = 1

max_connections = 550
#expire_logs_days = 10
#max_binlog_size = 100M

#log_bin should be on a disk with enough free space.
#Replace '/var/lib/mysql/mysql_binary_log' with an appropriate path for your
#system and chown the specified folder to the mysql user.
log_bin=/var/lib/mysql/mysql_binary_log

#In later versions of MariaDB, if you enable the binary log and do not set
#a server_id, MariaDB will not start. The server_id must be unique within
#the replicating group.
server_id=1

binlog_format = mixed

read_buffer_size = 2M
read_rnd_buffer_size = 16M
sort_buffer_size = 8M
join_buffer_size = 8M

# InnoDB settings
innodb_file_per_table = 1
innodb_flush_log_at_trx_commit  = 2
innodb_log_buffer_size = 64M
innodb_buffer_pool_size = 4G
innodb_thread_concurrency = 8
innodb_flush_method = O_DIRECT
innodb_log_file_size = 512M

[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354
```

允许远程访问

编辑**/etc/mysql/mariadb.conf.d/50-server.cnf**，

注释掉：`bind-address = 127.0.0.1`

启动mariadb

```
sudo systemctl start mariadb
1
```

设置root密码

```
sudo /usr/bin/mysql_secure_installation
1
```

操作如下：

```
[...]
Enter current password for root (enter for none):
OK, successfully used password, moving on...
[...]
Set root password? [Y/n] Y
New password:
Re-enter new password:
[...]
Remove anonymous users? [Y/n] Y
[...]
Disallow root login remotely? [Y/n] N
[...]
Remove test database and access to it [Y/n] Y
[...]
Reload privilege tables now? [Y/n] Y
[...]
All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!
1234567891011121314151617181920
```

安装MySQL JDBC Driver for MariaDB

```
sudo apt-get install libmysql-java

```

##### mysql链接####

https://docs.cloudera.com/documentation/enterprise/6/latest/topics/cm_ig_mysql.html



里面的socket选项在 var/run/mysql/里面！！

socket相关链接

https://blog.csdn.net/hjf161105/article/details/78850658?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param

lib里面自动创建，继续创建软链接

ln -s /var/lib/mysql/mysql.sock /var/run/mysqld/mysqld.sock

远程登录设置注释、etc/mysql/conf.d/mysql.cnf里面的127.0.0.1



创建数据库

1、进入mriadb

```
sudo mysql -u root -p
1
```

2、建库并授权（以下非全部库）

```
CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON scm.* TO 'scm'@'%' IDENTIFIED BY 'scm';

CREATE DATABASE amon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON amon.* TO 'amon'@'%' IDENTIFIED BY 'amon';

CREATE DATABASE rman DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON rman.* TO 'rman'@'%' IDENTIFIED BY 'rman';

CREATE DATABASE hue DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON hue.* TO 'hue'@'%' IDENTIFIED BY 'hue';

CREATE DATABASE hive DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON hive.* TO 'hive'@'%' IDENTIFIED BY 'hive';

CREATE DATABASE sentry DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON sentry.* TO 'sentry'@'%' IDENTIFIED BY 'sentry';

CREATE DATABASE oozie DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON oozie.* TO 'oozie'@'%' IDENTIFIED BY 'oozie';
1234567891011121314151617181920
```

设置cm数据库

```linux
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql scm scm scm -h localhost
```

```bash
sudo apt-get install mysql-server mysql-client libmysqlclient-dev libmysql-java
#停止mysql
sudo systemctl stop mysql
#删除不需要的文件
sudo rm /var/lib/mysql/ib_logfile0
sudo rm /var/lib/mysql/ib_logfile1
123456
#覆盖mysql配置文件
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
transaction-isolation = READ-COMMITTED
# Disabling symbolic-links is recommended to prevent assorted security risks;
# to do so, uncomment this line:
symbolic-links = 0

key_buffer_size = 32M
max_allowed_packet = 32M
thread_stack = 256K
thread_cache_size = 64
query_cache_limit = 8M
query_cache_size = 64M
query_cache_type = 1

max_connections = 550
#expire_logs_days = 10
#max_binlog_size = 100M

#log_bin should be on a disk with enough free space.
#Replace '/var/lib/mysql/mysql_binary_log' with an appropriate path for your
#system and chown the specified folder to the mysql user.
log_bin=/var/lib/mysql/mysql_binary_log

#In later versions of MySQL, if you enable the binary log and do not set
#a server_id, MySQL will not start. The server_id must be unique within
#the replicating group.
server_id=1

binlog_format = mixed

read_buffer_size = 2M
read_rnd_buffer_size = 16M
sort_buffer_size = 8M
join_buffer_size = 8M

# InnoDB settings
innodb_file_per_table = 1
innodb_flush_log_at_trx_commit  = 2
innodb_log_buffer_size = 64M
innodb_buffer_pool_size = 4G
innodb_thread_concurrency = 8
innodb_flush_method = O_DIRECT
innodb_log_file_size = 512M

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

sql_mode=STRICT_ALL_TABLES
1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253
#初始化mysql
sudo mysql_secure_installation
12
#创建数据库并授权
sudo mysql -h27.0.0.1 -uroot -p
12
-- 创建数据库
-- Cloudera Manager Server
CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
-- Activity Monitor
CREATE DATABASE amon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
-- Reports Manager
CREATE DATABASE rman DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
-- Hue
CREATE DATABASE hue DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
-- Hive Metastore Server
CREATE DATABASE hive DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
-- Sentry Server
CREATE DATABASE sentry DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
-- Cloudera Navigator Audit Server
CREATE DATABASE nav DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
-- Cloudera Navigator Metadata Server
CREATE DATABASE navms DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
-- Oozie
CREATE DATABASE oozie DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
 
#创建用户并授权
GRANT ALL ON scm.* TO 'scm'@'%' IDENTIFIED BY 'scm123456';
GRANT ALL ON amon.* TO 'amon'@'%' IDENTIFIED BY 'amon123456';
GRANT ALL ON rman.* TO 'rman'@'%' IDENTIFIED BY 'rman123456';
GRANT ALL ON hue.* TO 'hue'@'%' IDENTIFIED BY 'hue123456';
GRANT ALL ON hive.* TO 'hive'@'%' IDENTIFIED BY 'hive123456';
GRANT ALL ON sentry.* TO 'sentry'@'%' IDENTIFIED BY 'sentry123456';
GRANT ALL ON nav.* TO 'nav'@'%' IDENTIFIED BY 'nav123456';
GRANT ALL ON navms.* TO 'navms'@'%' IDENTIFIED BY 'navms123456';
GRANT ALL ON oozie.* TO 'oozie'@'%' IDENTIFIED BY 'oozie123456';
123456789101112131415161718192021222324252627282930
```

## step5 设置Cloudera Manager数据库

```bash
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql scm scm scm123456
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql amon amon amon123456
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql rman rman rman123456
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql hue hue hue123456
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql hive hive hive123456
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql sentry sentry sentry123456
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql nav nav nav123456
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql navms navms navms123456
sudo /opt/cloudera/cm/schema/scm_prepare_database.sh mysql oozie oozie oozie123456
123456789
```

## step6 启动

```bash
#启动cloudera-scm-server
sudo systemctl start cloudera-scm-server
 
#查看启动日志，等待Jetty启动完成
sudo tail -f /var/log/cloudera-scm-server/cloudera-scm-server.log
12345
```

## step 7

浏览器输入http://192.168.1.115:7180/
用户/密码：admin/admin
按照向导搭建集群。
如果搭建集群遇到**Could not find a HOST_MONITORING nozzle from SCM**错误，则/etc/hosts添加**127.0.0.1 localhost**

https://blog.csdn.net/summer089089/article/details/107605831

1.选物理节点用，号分割

2.选repository选定foo1.example.com/cloudera/cm6路径

