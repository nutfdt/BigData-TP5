#!/bin/bash

docker compose exec namenode bash -c "/usr/local/spark/sbin/start-master.sh"

docker compose exec datanode1 bash -c "/usr/local/spark/sbin/start-worker.sh spark://namenode:7077"
docker compose exec datanode2 bash -c "/usr/local/spark/sbin/start-worker.sh spark://namenode:7077"
docker compose exec datanode3 bash -c "/usr/local/spark/sbin/start-worker.sh spark://namenode:7077"