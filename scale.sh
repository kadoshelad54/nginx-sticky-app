#!/bin/bash

REPLICAS=${1:-5}

docker compose up -d --scale app=$REPLICAS
docker compose restart nginx
docker compose ps