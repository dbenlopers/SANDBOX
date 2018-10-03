#!/bin/sh
docker run -d -p 8081:8081 -v /etc/passwd:/etc/passwd -v /home/nexus-repo:/nexus-data -p 5000:5000 --restart=always --name nexus ge/nexus
