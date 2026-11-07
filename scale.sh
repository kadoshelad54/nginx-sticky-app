#!/bin/bash

docker compose up -d --scale app=5
docker compose restart nginx
docker compose ps