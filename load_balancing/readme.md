https://medium.com/@nirgn/load-balancing-applications-with-haproxy-and-docker-d719b7c5b231

docker build -t awesome .

docker swarm init
docker stack deploy --compose-file=docker-compose.yml prod
docker service ls