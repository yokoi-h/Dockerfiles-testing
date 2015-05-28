## books app
### build
```bash
docker build -t java-testing .
```

### run
- run a single container
```
docker run -d -p 10001:8080 --name stu01 java-testing
```

- run containers
```shell
./setup.sh start | sh
```

### stop
- stop a single container
```shell
docker stop stu01
docker rm stu01
```

- stop containers
```shell
./setup.sh stop | sh
```
