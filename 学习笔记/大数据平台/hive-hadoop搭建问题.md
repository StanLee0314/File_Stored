# 1. metastore 要去mysql里面创建
cd $HIVE_HOME/scripts/metastore/upgrade/mysql/
< Login into MySQL >
mysql> drop database IF EXISTS hive;
mysql> create database hive;
mysql> use hive;
mysql> source hive-schema-3.1.0.mysql.sql;
https://stackoverflow.com/questions/42209875/hive-2-1-1-metaexceptionmessageversion-information-not-found-in-metastore
# 2.schematool --dbType mysql --initSchema
Error: Table 'CTLGS' already exists (state=42S01,code=1050)org.apache.hadoop.hive.metastore.HiveMetaException: Schema initialization FAILED! Metastore state would be inconsistent !!
sql 里面把metadata表删掉
hive --service metastore
# 3.
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
https://repo1.maven.org/maven2/org/slf4j/slf4j-nop/1.7.9/
下一个nop放在/
jar:file:/usr/local/hadoop/share/hadoop/common/lib/slf4j-nop-1.7.9.jar!
# 4.
org.apache.hadoop.hive.metastore.HiveMetaException: Failed to load driver
Underlying cause: java.lang.ClassNotFoundException : com.mysql.jdbc.Driver
下载mysql-connector-java-commercial-5.1.7-bin.jar 放在hive/lib里面
# 5.
java.lang.NoSuchMethodError: com.google.common.base.Preconditions.checkArgument
$ rm /opt/shared/apache-hive-3.1.2-bin/lib/guava-19.0.jar
$ cp /opt/shared/hadoop-3.2.1/share/hadoop/hdfs/lib/guava-27.0-jre.jar /opt/shared/apache-hive-3.1.2-bin/lib/
#6.
problem: FAILED: SemanticException Cannot find class 'org.elasticsearch.hadoop.hive.ESStorageHandler'
I solved the problem after adding elasticsearch-hadoop-2.3.0.jar and elasticsearch-hadoop-hive-2.3.0.jar files in $HIVE_HOME/lib folder.
