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
# 6.
problem: FAILED: SemanticException Cannot find class 'org.elasticsearch.hadoop.hive.ESStorageHandler'
I solved the problem after adding elasticsearch-hadoop-2.3.0.jar and elasticsearch-hadoop-hive-2.3.0.jar files in $HIVE_HOME/lib folder.
# 7.
problem:FAILED: Execution Error, return code 1 from org.apache.hadoop.hive.ql.exec.DDLTask. java.lang.RuntimeException:
MetaException(message:java.lang.NoClassDefFoundError org/apache/commons/httpclient/HttpConnectionManager)
I followed the roadmap proposed by Sergio, but used this jar:

https://mvnrepository.com/artifact/commons-httpclient/commons-httpclient/3.1.0.redhat-8 84
# 8. 
problem: FAILED: Execution Error, return code 1 from org.apache.hadoop.hive.ql.exec.DDLTask. org.elasticsearch.hadoop.EsHadoopIllegalArgumentException: Cannot
detect ES version - typically this happens if the network/Elasticsearch cluster is not accessible or when targeting a WAN/Cloud instance without the proper
setting 'es.nodes.wan.only'
solve: 只引一个包 First, make sure that ONLY ONE of those jars are added. The first one there includes all integrations, and the second one includes only the hive 
integration code + the core code. Adding both will trip up internal checks for only one jar on the classpath
# 9.
pro:FAILED: Execution Error, return code 1 from org.apache.hadoop.hive.ql.exec.DDLTask. org/apache/hadoop/hive/serde2/SerDe
您可以添加与您的版本对应的jar add jar HIVE_HOME/lib/hive-hcatalog-core-2.3.2.jar,
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
https://repo1.maven.org/maven2/org/apache/hive/hcatalog/hive-hcatalog-core/3.1.0/
# 10.
pro: Could not find any valid local directory for nmPrivate/container_1595384260109_0006_02_0000011738df49a11.tokens
For more detailed output, check the application tracking page: http://csiv-12:8088/cluster/app/application_1595384260109_0006 
Then click on links to logs of each attempt.. Failing the application.
Please check whether your <HADOOP_HOME>/etc/hadoop/mapred-site.xml contains the below configuration:
<property>
  <name>yarn.app.mapreduce.am.env</name>
  <value>HADOOP_MAPRED_HOME=${full path of your hadoop distribution directory}</value>
</property>
<property>
  <name>mapreduce.map.env</name>
  <value>HADOOP_MAPRED_HOME=${full path of your hadoop distribution directory}</value>
</property>
<property>
  <name>mapreduce.reduce.env</name>
  <value>HADOOP_MAPRED_HOME=${full path of your hadoop distribution directory}</value>
</property>
solution: mapred -site.xml
```
<property>
 22     <name>mapreduce.framework.name</name>
 23     <value>yarn</value>
 24 </property>
 25  <property>
 26         <name>hadoop.tmp.dir</name>
 27         <value>/usr/local/hadoop/data/</value>
 28         <description>hadoop数据存放</description>
 29  </property>
 30  <property>
 31         <name>yarn.app.mapreduce.am.env</name>
 32         <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
 33     </property>
 34     <property>
 35         <name>mapreduce.map.env</name>
 36         <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
 37     </property>
 38     <property>
 39         <name>mapreduce.reduce.env</name>
 40         <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
 41     </property>
```
# 11. 
pro:  java.lang.ClassNotFoundException: org.apache.hive.hcatalog.data.JsonSerDe
```<property>
    <name>hive.aux.jars.path</name>
    <value>file:///usr/local/Cellar/hive–1.2.1/lib/hive-hcatalog-core-1.2.1.jar</value>
  </property>
```
