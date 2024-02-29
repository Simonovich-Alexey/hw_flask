# Приложение на Flask

### REST API для списка задач

run database:
```bash
docker-compose --env-file .env_example up db
```
run tests:

```bash
docker-compose --env-file .env_example up tests
```

run app:
```bash
docker-compose --env-file .env_example up app
```

### Сборка Docker-образа
Для сборки Docker-образа используйте следующую команду:

```bash
docker image build -t stocks-products:latest .
```
Эта команда создаст Docker-образ с именем `stocks-products` и тегом `latest`, используя `Dockerfile` из текущего каталога.

### Запуск Docker-контейнера:

После того как образ собран, вы можете запустить контейнер Docker с помощью следующей команды:

```bash
docker run -d -p 5000:6060 stocks-products:latest
```

Эта команда запустит контейнер в фоновом режиме и пробросит порт 6060 из контейнера на порт 5000 хоста.

После этого вы сможете открыть веб-приложение в браузере по адресу `http://localhost:5000/api/v1/`