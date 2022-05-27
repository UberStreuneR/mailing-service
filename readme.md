## Реализовано

- Все задачи из основного блока, вся логика
- docker-compose.yml для сборки проекта
- Swagger документация по адресу /docs/

## Недочеты

- POST запрос с помощью requests возвращает статус 400, в то время как аналогичный запрос через Postman проходит успешно
- Из-за чего у всех объектов модели Message статус 'E', означающий ошибку

## Запуск проекта

- Клонировать в локальный репозиторий
- $ docker-compose up

## Использование

- Создать тестового клиента (POST localhost:8000/clients/)

```sh
{
    "number": "79009009090",
    "operator_code": "900",
    "tag": "mytag"
}
```

- Создать тестовую рассылку (POST localhost:8000/mailings/)

```sh
{
    "start_time": "2022-05-27 00:00:00",
    "end_time": "2022-05-28 00:00:00",
    "message": "Hello everybody",
    "filter_operator_code": "900",
    "filter_tag": "mytag"
}
```

- Убедиться, что сообщения были отправлены (GET localhost:8000/messages/).
- Просмотреть детали рассылок (GET localhost:8000/mailings/)
