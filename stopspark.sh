#!/bin/bash

docker compose exec namenode bash -c "/usr/local/spark/sbin/stop-master.sh"

docker compose exec datanode1 bash -c "/usr/local/spark/sbin/stop-worker.sh"
docker compose exec datanode2 bash -c "/usr/local/spark/sbin/stop-worker.sh"
docker compose exec datanode3 bash -c "/usr/local/spark/sbin/stop-worker.sh"