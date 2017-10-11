sudo apt-get install ssh
sudo apt-get install rsync

sudo apt install openssh-client
sudo apt install openssh-server

sudo adduser tim
sudo adduser tim sudo

# Copy ssh key
sudo mkdir /home/tim/.ssh
sudo cp /home/ubuntu/.ssh/authorized_keys /home/tim/.ssh/authorized_keys
sudo chown tim -R /home/tim/.ssh
sudo chmod 700 /home/tim/.ssh
sudo chmod 600 /home/tim/.ssh/authorized_keys

# Switch user
su tim

eval `ssh-agent -s`
ssh localhost
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer

mkdir downloads
cd downloads
pwd
wget http://www-us.apache.org/dist/hadoop/common/hadoop-2.7.4/hadoop-2.7.4.tar.gz
tar xvzf hadoop-2.7.4.tar.gz
sudo mkdir -p /usr/local/hadoop
cd hadoop-2.7.4/
sudo mv * /usr/local/hadoop

cd ~
sudo nano .bashrc

export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export PATH=$PATH:$JAVA_HOME/bin

export HADOOP_HOME=/usr/local/hadoop
export HIVE_HOME=/home/tim/downloads/apache-hive-2.3.0-bin

export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin
export PATH=$PATH:$HIVE_HOME/bin

export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
export HADOOP_LOG_DIR=/home/tim/logs

export SPARK_HOME=/home/tim/downloads/spark-2.2.0-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME/bin


export HIVE_HOME=/usr/local/apache-hive-2.1.0-bin
export HIVE_CONF_DIR=/usr/local/apache-hive-2.1.0-bin/conf
export PATH=$HIVE_HOME/bin:$PATH
export CLASSPATH=$CLASSPATH:/usr/local/hadoop/lib/*:.
export CLASSPATH=$CLASSPATH:/usr/local/apache-hive-2.1.0-bin/lib/*:.



source ~/.bashrc

mkdir logs
mkdir tmp


sudo chown -R tim /usr/local/hadoop/

hadoop-env.sh
-------------
export JAVA_HOME=/usr/lib/jvm/java-8-oracle

core-site.xml
-------------
<configuration>
<property>
 <name>hadoop.tmp.dir</name>
   <value>/home/thanooj/tmp</value>
   <description>A base for other temporary directories.</description>
</property>
 <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>

mapred-site.xml
---------------
<configuration>
<property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>


hdfs-site.xml
-------------
<configuration>
<property>
        <name>dfs.replication</name>
        <value>1</value>
</property>
<property>
   <name>dfs.namenode.name.dir</name>
   <value>file:/home/thanooj/hadoop_store/hdfs/namenode</value>
 </property>
 <property>
   <name>dfs.datanode.data.dir</name>
   <value>file:/home/thanooj/hadoop_store/hdfs/datanode</value>
 </property>
</configuration>

yarn-site.xml
-------------
<configuration>
<property>
      <name>yarn.nodemanager.aux-services</name>
      <value>mapreduce_shuffle</value>
   </property>
</configuration>


thanooj@ubuntu:~$ cd /home/thanooj/hadoop_store/hdfs/
thanooj@ubuntu:~/hadoop_store/hdfs$ ls -ltr
total 8
drwx------ 3 thanooj thanooj 4096 Aug  7 13:34 datanode
drwxrwxr-x 3 thanooj thanooj 4096 Aug  7 13:35 namenode
thanooj@ubuntu:~/hadoop_store/hdfs$ rm -rf datanode
thanooj@ubuntu:~/hadoop_store/hdfs$ rm -rf namenode
thanooj@ubuntu:~/hadoop_store/hdfs$ hdfs namenode -format
.....

thanooj@ubuntu:~/hadoop_store/hdfs$ start-all.sh
This script is Deprecated. Instead use start-dfs.sh and start-yarn.sh
Starting namenodes on [localhost]
localhost: starting namenode, logging to /usr/local/hadoop/logs/hadoop-thanooj-namenode-ubuntu.out
localhost: starting datanode, logging to /usr/local/hadoop/logs/hadoop-thanooj-datanode-ubuntu.out
Starting secondary namenodes [0.0.0.0]
0.0.0.0: starting secondarynamenode, logging to /usr/local/hadoop/logs/hadoop-thanooj-secondarynamenode-ubuntu.out
starting yarn daemons
starting resourcemanager, logging to /usr/local/hadoop/logs/yarn-thanooj-resourcemanager-ubuntu.out
localhost: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-thanooj-nodemanager-ubuntu.out
thanooj@ubuntu:~/hadoop_store/hdfs$ jps
18737 DataNode
18626 NameNode
19094 ResourceManager
19208 NodeManager
19240 Jps
18940 SecondaryNameNode
thanooj@ubuntu:~/hadoop_store/hdfs$

thanooj@ubuntu:~/hadoop_store/hdfs$ hdfs dfs -mkdir -p /user/hive/warehouse
thanooj@ubuntu:~/hadoop_store/hdfs$ hdfs dfs -mkdir /tmp
thanooj@ubuntu:~/hadoop_store/hdfs$ hdfs dfs -chmod g+w /user/hive/warehouse
thanooj@ubuntu:~/hadoop_store/hdfs$ hdfs dfs -chmod g+w /tmp
thanooj@ubuntu:~/hadoop_store/hdfs$


###################################hive-site.xml###################################################
<property>
<name>javax.jdo.option.ConnectionURL</name>
<value>jdbc:derby:;databaseName=/home/thanooj/downloads/apache-hive-2.3.0-bin/metastore_db;create=true</value>
</property>
<property>
<name>hive.metastore.warehouse.dir</name>
<value>/user/hive/warehouse</value>
<description>location of default database for the warehouse</description>
</property>
<property>
<name>hive.metastore.uris</name>
<value/>
<description>Thrift URI for the remote metastore. Used by metastore client to connect to remote metastore.</description>
</property>
<property>
<name>javax.jdo.option.ConnectionDriverName</name>
<value>org.apache.derby.jdbc.EmbeddedDriver</value>
<description>Driver class name for a JDBC metastore</description>
</property>
<property>
<name>javax.jdo.PersistenceManagerFactoryClass</name>
<value>org.datanucleus.api.jdo.JDOPersistenceManagerFactory</value>
<description>class implementing the jdo persistence</description>
</property>




vim conf/hive-env.sh


########################hive-env.sh############################################
# The heap size of the jvm stared by hive shell script can be controlled via:
#
export HADOOP_HEAPSIZE=512
#
# Larger heap size may be required when running queries over large number of files or partitions.
# By default hive shell scripts use a heap size of 256 (MB).  Larger heap size would also be
# appropriate for hive server (hwi etc).


# Set HADOOP_HOME to point to a specific hadoop install directory
export HADOOP_HOME=/usr/local/hadoop

# Hive Configuration Directory can be controlled by:
export HIVE_CONF_DIR=/home/thanooj/downloads/apache-hive-2.3.0-bin/conf

# Folder containing extra ibraries required for hive compilation/execution can be controlled by:
export HIVE_AUX_JARS_PATH=/home/thanooj/downloads/apache-hive-2.3.0-bin/lib/*.jar



thanooj@ubuntu:~/downloads/apache-hive-2.3.0-bin/conf$ source ~/.bashrc
thanooj@ubuntu:~/downloads/apache-hive-2.3.0-bin/conf$ schematool -initSchema -dbType derby
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/home/thanooj/downloads/apache-hive-2.3.0-bin/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/local/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
Metastore connection URL:        jdbc:derby:;databaseName=metastore_db;create=true
Metastore Connection Driver :    org.apache.derby.jdbc.EmbeddedDriver
Metastore connection User:       APP
Starting metastore schema initialization to 2.3.0
Initialization script hive-schema-2.3.0.derby.sql
Initialization script completed
schemaTool completed
thanooj@ubuntu:~/downloads/apache-hive-2.3.0-bin/conf$ hive
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/home/thanooj/downloads/apache-hive-2.3.0-bin/lib/log4j-slf4j-impl-2.6.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/local/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]

Logging initialized using configuration in jar:file:/home/thanooj/downloads/apache-hive-2.3.0-bin/lib/hive-common-2.3.0.jar!/hive-log4j2.properties Async: true
Hive-on-MR is deprecated in Hive 2 and may not be available in the future versions. Consider using a different execution engine (i.e. spark, tez) or using Hive 1.X releases.
hive> show databases;
OK
default
Time taken: 15.312 seconds, Fetched: 1 row(s)
hive> exit;
thanooj@ubuntu:~/downloads/apache-hive-2.3.0-bin/conf$




thanooj@ubuntu:~$ sudo apt-get install scala
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  libhawtjni-runtime-java libjansi-java libjansi-native-java libjline2-java scala-library scala-parser-combinators scala-xml
Suggested packages:
  scala-doc
The following NEW packages will be installed:
  libhawtjni-runtime-java libjansi-java libjansi-native-java libjline2-java scala scala-library scala-parser-combinators scala-xml
0 upgraded, 8 newly installed, 0 to remove and 10 not upgraded.
Need to get 23.6 MB of archives.
After this operation, 28.1 MB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 libhawtjni-runtime-java all 1.10-1 [54.0 kB]
Get:2 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 libjansi-native-java all 1.0-4 [35.3 kB]
Get:3 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 libjansi-java all 1.4-3 [57.4 kB]
Get:4 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 libjline2-java all 2.11-4 [107 kB]
Get:5 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 scala-library all 2.11.6-6 [9,239 kB]
Get:6 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 scala-parser-combinators all 1.0.3-3 [355 kB]
Get:7 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 scala-xml all 1.0.3-3 [601 kB]
Get:8 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 scala all 2.11.6-6 [13.1 MB]
Fetched 23.6 MB in 2min 23s (164 kB/s)
Selecting previously unselected package libhawtjni-runtime-java.
(Reading database ... 88696 files and directories currently installed.)
Preparing to unpack .../libhawtjni-runtime-java_1.10-1_all.deb ...
Unpacking libhawtjni-runtime-java (1.10-1) ...
Selecting previously unselected package libjansi-native-java.
Preparing to unpack .../libjansi-native-java_1.0-4_all.deb ...
Unpacking libjansi-native-java (1.0-4) ...
Selecting previously unselected package libjansi-java.
Preparing to unpack .../libjansi-java_1.4-3_all.deb ...
Unpacking libjansi-java (1.4-3) ...
Selecting previously unselected package libjline2-java.
Preparing to unpack .../libjline2-java_2.11-4_all.deb ...
Unpacking libjline2-java (2.11-4) ...
Selecting previously unselected package scala-library.
Preparing to unpack .../scala-library_2.11.6-6_all.deb ...
Unpacking scala-library (2.11.6-6) ...
Selecting previously unselected package scala-parser-combinators.
Preparing to unpack .../scala-parser-combinators_1.0.3-3_all.deb ...
Unpacking scala-parser-combinators (1.0.3-3) ...
Selecting previously unselected package scala-xml.
Preparing to unpack .../scala-xml_1.0.3-3_all.deb ...
Unpacking scala-xml (1.0.3-3) ...
Selecting previously unselected package scala.
Preparing to unpack .../scala_2.11.6-6_all.deb ...
Unpacking scala (2.11.6-6) ...
Setting up libhawtjni-runtime-java (1.10-1) ...
Setting up libjansi-native-java (1.0-4) ...
Setting up libjansi-java (1.4-3) ...
Setting up libjline2-java (2.11-4) ...
Setting up scala-library (2.11.6-6) ...
Setting up scala-parser-combinators (1.0.3-3) ...
Setting up scala-xml (1.0.3-3) ...
Setting up scala (2.11.6-6) ...
update-alternatives: using /usr/share/scala-2.11/bin/scala to provide /usr/bin/scala (scala) in auto mode
thanooj@ubuntu:~/downloads/apache-hive-2.3.0-bin/conf$ scala
Welcome to Scala version 2.11.6 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_144).
Type in expressions to have them evaluated.
Type :help for more information.

scala> exit

thanooj@ubuntu:~/downloads/apache-hive-2.3.0-bin/conf$ scala -version
Scala code runner version 2.11.6 -- Copyright 2002-2013, LAMP/EPFL
thanooj@ubuntu:~/downloads/apache-hive-2.3.0-bin/conf$ scala
Welcome to Scala version 2.11.6 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_144).
Type in expressions to have them evaluated.
Type :help for more information.

scala> println("Hello World")
Hello World

scala> :q
thanooj@ubuntu:~/downloads/apache-hive-2.3.0-bin/conf$


thanooj@ubuntu:~/downloads/spark-2.2.0-bin-hadoop2.7/conf$ ls -ltr
-rw-r--r-- 1 thanooj thanooj 2025 Jun 30 16:09 log4j.properties
.....
-rwxr-xr-x 1 thanooj thanooj 3856 Aug 15 11:31 spark-env.sh
drwxrwxr-x 5 thanooj thanooj 4096 Aug 15 11:39 metastore_db
-rw-rw-r-- 1 thanooj thanooj  775 Aug 15 11:39 derby.log
thanooj@ubuntu:~/downloads/spark-2.2.0-bin-hadoop2.7/conf$


# Set the default spark-shell log level to WARN. When running the spark-shell, the
# log level for this class is used to overwrite the root logger's log level, so that
# the user can have different defaults for the shell and regular Spark apps.
log4j.logger.org.apache.spark.repl.Main=INFO


##################################spark-env.sh##############################
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export SPARK_CONF_DIR=/home/thanooj/downloads/spark-2.2.0-bin-hadoop2.7/conf
export SPARK_LOCAL_IP=127.0.0.1



thanooj@ubuntu:~$ spark-shell
17/08/15 11:50:03 INFO SignalUtils: Registered signal handler for INT
17/08/15 11:50:25 INFO SparkContext: Running Spark version 2.2.0
17/08/15 11:50:26 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/08/15 11:50:27 INFO SparkContext: Submitted application: Spark shell
17/08/15 11:50:27 INFO SecurityManager: Changing view acls to: thanooj
17/08/15 11:50:27 INFO SecurityManager: Changing modify acls to: thanooj
17/08/15 11:50:27 INFO SecurityManager: Changing view acls groups to:
17/08/15 11:50:27 INFO SecurityManager: Changing modify acls groups to:
17/08/15 11:50:27 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users  with view permissions: Set(thanooj); groups with view permissions: Set(); users  with modify permissions: Set(thanooj); groups with modify permissions: Set()
17/08/15 11:50:28 INFO Utils: Successfully started service 'sparkDriver' on port 35370.
17/08/15 11:50:28 INFO SparkEnv: Registering MapOutputTracker
17/08/15 11:50:28 INFO SparkEnv: Registering BlockManagerMaster
17/08/15 11:50:28 INFO BlockManagerMasterEndpoint: Using org.apache.spark.storage.DefaultTopologyMapper for getting topology information
17/08/15 11:50:28 INFO BlockManagerMasterEndpoint: BlockManagerMasterEndpoint up
17/08/15 11:50:28 INFO DiskBlockManager: Created local directory at /tmp/blockmgr-f72cecf8-d8a9-475b-bd68-fa5f4ca8aaaa
17/08/15 11:50:28 INFO MemoryStore: MemoryStore started with capacity 413.9 MB
17/08/15 11:50:29 INFO SparkEnv: Registering OutputCommitCoordinator
17/08/15 11:50:29 INFO Utils: Successfully started service 'SparkUI' on port 4040.
17/08/15 11:50:29 INFO SparkUI: Bound SparkUI to 127.0.0.1, and started at http://127.0.0.1:4040
17/08/15 11:50:30 INFO Executor: Starting executor ID driver on host localhost
17/08/15 11:50:30 INFO Executor: Using REPL class URI: spark://127.0.0.1:35370/classes
17/08/15 11:50:30 INFO Utils: Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 40615.
17/08/15 11:50:30 INFO NettyBlockTransferService: Server created on 127.0.0.1:40615
17/08/15 11:50:30 INFO BlockManager: Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
17/08/15 11:50:30 INFO BlockManagerMaster: Registering BlockManager BlockManagerId(driver, 127.0.0.1, 40615, None)
17/08/15 11:50:30 INFO BlockManagerMasterEndpoint: Registering block manager 127.0.0.1:40615 with 413.9 MB RAM, BlockManagerId(driver, 127.0.0.1, 40615, None)
17/08/15 11:50:30 INFO BlockManagerMaster: Registered BlockManager BlockManagerId(driver, 127.0.0.1, 40615, None)
17/08/15 11:50:30 INFO BlockManager: Initialized BlockManager: BlockManagerId(driver, 127.0.0.1, 40615, None)
17/08/15 11:50:31 INFO SharedState: Setting hive.metastore.warehouse.dir ('null') to the value of spark.sql.warehouse.dir ('file:/home/thanooj/downloads/spark-2.2.0-bin-hadoop2.7/conf/spark-warehouse').
17/08/15 11:50:31 INFO SharedState: Warehouse path is 'file:/home/thanooj/downloads/spark-2.2.0-bin-hadoop2.7/conf/spark-warehouse'.
17/08/15 11:50:33 INFO HiveUtils: Initializing HiveMetastoreConnection version 1.2.1 using Spark classes.
17/08/15 11:50:35 INFO HiveMetaStore: 0: Opening raw store with implemenation class:org.apache.hadoop.hive.metastore.ObjectStore
17/08/15 11:50:35 INFO ObjectStore: ObjectStore, initialize called
17/08/15 11:50:36 INFO Persistence: Property hive.metastore.integral.jdo.pushdown unknown - will be ignored
17/08/15 11:50:36 INFO Persistence: Property datanucleus.cache.level2 unknown - will be ignored
17/08/15 11:50:40 INFO ObjectStore: Setting MetaStore object pin classes with hive.metastore.cache.pinobjtypes="Table,StorageDescriptor,SerDeInfo,Partition,Database,Type,FieldSchema,Order"
17/08/15 11:50:43 INFO Datastore: The class "org.apache.hadoop.hive.metastore.model.MFieldSchema" is tagged as "embedded-only" so does not have its own datastore table.
17/08/15 11:50:43 INFO Datastore: The class "org.apache.hadoop.hive.metastore.model.MOrder" is tagged as "embedded-only" so does not have its own datastore table.
17/08/15 11:50:44 INFO Datastore: The class "org.apache.hadoop.hive.metastore.model.MFieldSchema" is tagged as "embedded-only" so does not have its own datastore table.
17/08/15 11:50:44 INFO Datastore: The class "org.apache.hadoop.hive.metastore.model.MOrder" is tagged as "embedded-only" so does not have its own datastore table.
17/08/15 11:50:45 INFO Query: Reading in results for query "org.datanucleus.store.rdbms.query.SQLQuery@0" since the connection used is closing
17/08/15 11:50:45 INFO MetaStoreDirectSql: Using direct SQL, underlying DB is DERBY
17/08/15 11:50:45 INFO ObjectStore: Initialized ObjectStore
17/08/15 11:50:46 INFO HiveMetaStore: Added admin role in metastore
17/08/15 11:50:46 INFO HiveMetaStore: Added public role in metastore
17/08/15 11:50:46 INFO HiveMetaStore: No user is added in admin role, since config is empty
17/08/15 11:50:46 INFO HiveMetaStore: 0: get_all_databases
17/08/15 11:50:46 INFO audit: ugi=thanooj       ip=unknown-ip-addr      cmd=get_all_databases
17/08/15 11:50:47 INFO HiveMetaStore: 0: get_functions: db=default pat=*
17/08/15 11:50:47 INFO audit: ugi=thanooj       ip=unknown-ip-addr      cmd=get_functions: db=default pat=*
17/08/15 11:50:47 INFO Datastore: The class "org.apache.hadoop.hive.metastore.model.MResourceUri" is tagged as "embedded-only" so does not have its own datastore table.
17/08/15 11:50:48 INFO SessionState: Created local directory: /tmp/b1eb22d8-5842-4418-81b3-7c6cfd3a8d5a_resources
17/08/15 11:50:48 INFO SessionState: Created HDFS directory: /tmp/hive/thanooj/b1eb22d8-5842-4418-81b3-7c6cfd3a8d5a
17/08/15 11:50:48 INFO SessionState: Created local directory: /tmp/thanooj/b1eb22d8-5842-4418-81b3-7c6cfd3a8d5a
17/08/15 11:50:48 INFO SessionState: Created HDFS directory: /tmp/hive/thanooj/b1eb22d8-5842-4418-81b3-7c6cfd3a8d5a/_tmp_space.db
17/08/15 11:50:48 INFO HiveClientImpl: Warehouse location for Hive client (version 1.2.1) is file:/home/thanooj/downloads/spark-2.2.0-bin-hadoop2.7/conf/spark-warehouse
17/08/15 11:50:49 INFO HiveMetaStore: 0: get_database: default
17/08/15 11:50:49 INFO audit: ugi=thanooj       ip=unknown-ip-addr      cmd=get_database: default
17/08/15 11:50:49 INFO HiveMetaStore: 0: get_database: global_temp
17/08/15 11:50:49 INFO audit: ugi=thanooj       ip=unknown-ip-addr      cmd=get_database: global_temp
17/08/15 11:50:49 WARN ObjectStore: Failed to get database global_temp, returning NoSuchObjectException
17/08/15 11:50:49 INFO SessionState: Created local directory: /tmp/1a29fec0-d3c0-4b15-8400-252a0c3ce726_resources
17/08/15 11:50:49 INFO SessionState: Created HDFS directory: /tmp/hive/thanooj/1a29fec0-d3c0-4b15-8400-252a0c3ce726
17/08/15 11:50:49 INFO SessionState: Created local directory: /tmp/thanooj/1a29fec0-d3c0-4b15-8400-252a0c3ce726
17/08/15 11:50:49 INFO SessionState: Created HDFS directory: /tmp/hive/thanooj/1a29fec0-d3c0-4b15-8400-252a0c3ce726/_tmp_space.db
17/08/15 11:50:49 INFO HiveClientImpl: Warehouse location for Hive client (version 1.2.1) is file:/home/thanooj/downloads/spark-2.2.0-bin-hadoop2.7/conf/spark-warehouse
17/08/15 11:50:50 INFO StateStoreCoordinatorRef: Registered StateStoreCoordinator endpoint
17/08/15 11:50:50 INFO Main: Created Spark session with Hive support
Spark context Web UI available at http://127.0.0.1:4040
Spark context available as 'sc' (master = local[*], app id = local-1502823029976).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.2.0
      /_/

Using Scala version 2.11.8 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_144)
Type in expressions to have them evaluated.
Type :help for more information.

scala> sc
res0: org.apache.spark.SparkContext = org.apache.spark.SparkContext@76b6bad3

scala> :q
17/08/15 11:53:39 INFO SparkUI: Stopped Spark web UI at http://127.0.0.1:4040
17/08/15 11:53:39 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!
17/08/15 11:53:39 INFO MemoryStore: MemoryStore cleared
17/08/15 11:53:39 INFO BlockManager: BlockManager stopped
17/08/15 11:53:39 INFO BlockManagerMaster: BlockManagerMaster stopped
17/08/15 11:53:39 INFO OutputCommitCoordinator$OutputCommitCoordinatorEndpoint: OutputCommitCoordinator stopped!
17/08/15 11:53:39 INFO SparkContext: Successfully stopped SparkContext
17/08/15 11:53:39 INFO ShutdownHookManager: Shutdown hook called
17/08/15 11:53:39 INFO ShutdownHookManager: Deleting directory /tmp/spark-e3619a09-8fdf-4f8f-bd80-7263ee308140/repl-dc70615e-7859-4158-9762-261d6bee81e1
17/08/15 11:53:39 INFO ShutdownHookManager: Deleting directory /tmp/spark-e3619a09-8fdf-4f8f-bd80-7263ee308140
thanooj@ubuntu:~$


################################### HBase #######################################################
/home/thanooj/downloads/hbase-1.3.1
/home/thanooj/downloads/hbase-1.3.1/hbasestorage


################################ hbase-site.xml ##########################
<configuration>
   //Here you have to set the path where you want HBase to store its files.
   <property>
      <name>hbase.rootdir</name>
      <value>/home/thanooj/downloads/hbase-1.3.1/hbasestorage</value>
   </property>
   <property>
    <name>hbase.zookeeper.quorum</name>
    <value>localhost</value>
    <description>The directory shared by RegionServers.</description>
  </property>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
    <description>The mode the cluster will be in. Possible values are
      false: standalone and pseudo-distributed setups with managed Zookeeper
      true: fully-distributed with unmanaged Zookeeper Quorum (see hbase-env.sh)
    </description>
  </property>
   //Here you have to set the path where you want HBase to store its built in zookeeper  files.
   <property>
      <name>hbase.zookeeper.property.dataDir</name>
      <value>/home/thanooj/downloads/hbase-1.3.1/hbasestorage/zookeeper</value>
   </property>
</configuration>



########################### hbase-env.sh ####################################
# Tell HBase whether it should manage it's own instance of Zookeeper or not.
export HBASE_MANAGES_ZK=true
HBASE_ROOT_LOGGER=INFO,DRFA
# The reason for changing default to RFA is to avoid the boundary case of filling out disk space as
# DRFA doesn't put any cap on the log size. Please refer to HBase-5655 for more context.
export JAVA_HOME=/usr/lib/jvm/java-8-oracle



thanooj@ubuntu:~$ start-hbase.sh
localhost: starting zookeeper, logging to /home/thanooj/downloads/hbase-1.3.1/bin/../logs/hbase-thanooj-zookeeper-ubuntu.out
starting master, logging to /home/thanooj/downloads/hbase-1.3.1/logs/hbase-thanooj-master-ubuntu.out
starting regionserver, logging to /home/thanooj/downloads/hbase-1.3.1/logs/hbase-thanooj-1-regionserver-ubuntu.out
thanooj@ubuntu:~/hadoop_store/hdfs$ jps
7748 HQuorumPeer
7802 HMaster
7915 HRegionServer
18737 DataNode
18626 NameNode
19094 ResourceManager
19208 NodeManager
19240 Jps
18940 SecondaryNameNode
thanooj@ubuntu:~/hadoop_store/hdfs$ hbase shell
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/home/thanooj/downloads/hbase-1.3.1/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/usr/local/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
HBase Shell; enter 'help<RETURN>' for list of supported commands.
Type "exit<RETURN>" to leave the HBase Shell
Version 1.3.1, r930b9a55528fe45d8edce7af42fef2d35e77677a, Thu Apr  6 19:36:54 PDT 2017

hbase(main):001:0> list
TABLE
0 row(s) in 0.7070 seconds

=> []
hbase(main):002:0> exit
thanooj@ubuntu:~$ stop-hbase.sh
stopping hbase....................
localhost: stopping zookeeper.
thanooj@ubuntu:~/hadoop_store/hdfs$ jps
18737 DataNode
18626 NameNode
19094 ResourceManager
19208 NodeManager
19240 Jps
18940 SecondaryNameNode
thanooj@ubuntu:~/hadoop_store/hdfs$
