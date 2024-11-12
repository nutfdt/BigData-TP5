FROM --platform=linux/amd64 debian:buster

# Mise à jour des packages
RUN apt-get update && apt-get upgrade -y

# Installation de Java
RUN apt-get install -y default-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Installation de SSH
RUN apt-get install -y openssh-client openssh-server

# Installation de wget
RUN apt-get install -y wget

# Installation de Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz && \
    tar -xzf hadoop-3.4.1.tar.gz && \
    mv hadoop-3.4.1 /usr/local/hadoop && \
    rm hadoop-3.4.1.tar.gz

# Configuration de Hadoop
ENV HADOOP_HOME=/usr/local/hadoop
ENV HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Ajout de fichiers de configuration
ADD config/* $HADOOP_CONF_DIR/

# Installation de Spark
RUN wget https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz && \
    tar -xzf spark-3.5.3-bin-hadoop3.tgz && \
    mv spark-3.5.3-bin-hadoop3 /usr/local/spark && \
    rm spark-3.5.3-bin-hadoop3.tgz

# Configuration de Spark
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# Configuration SSH
RUN mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Génération de la clé SSH et partage entre les conteneurs
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

# Ajouter le script d'entrée
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

USER root

EXPOSE 22 9000 8042 8041 8040 8088 8042 4040 8888 8080 19888 7077