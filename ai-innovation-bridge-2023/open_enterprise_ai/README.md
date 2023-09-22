### Instructions for splitting Gaudi-2 into 8 Docker containers

First, let's match the device ID to the module ID
```bash
hl-smi -Q index,module_id -f csv
```
We should get an output like:
```bash
index, module_id
3, 2
2, 4
0, 6
7, 1
4, 5
1, 7
5, 3
6, 0
```

Update the docker-compose.yml file with the associated `index` to `module_id`. Feel free to update the tokens and port numbers according to what ports you would like to use. 

With the `Dockerfile` and the `docker-compose.yml` files in the same directory, we can run the docker compose in the background:
```bash
docker compose up -d
```

Each of the docker containers should be pointing at one of the Gaudi 2 instances with Jupyter running. 
