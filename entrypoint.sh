#!/bin/bash

# Formater le Namenode si cela n'a pas été fait
if [ ! -d "/usr/local/hadoop/hadoop_data/hdfs/namenode/current" ]; then
    hdfs namenode -format
fi

# Lancer le service
exec "$@"
