### Сборка образа

```
docker build ./ --tag=test_dj_docker2

```

### Запуск контейнера

```
docker run --name my_hw1.2_stocks -d -p 8000:8000 test_dj_docker2
```