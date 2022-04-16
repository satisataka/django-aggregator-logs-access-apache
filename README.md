# Django Aggregator Apache Access Logs

__ВНИМАНИЕ!!! приложение полноценно работает тольно на LINUX, тк использует [cron](https://ru.wikipedia.org/wiki/Cron)__

Это приложение разработано в рамках тестового задания

Формат логов должен быть: _"%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""_, в соотвествии c [Apache Access Log (Combined Log Format)](https://httpd.apache.org/docs/2.4/logs.html)


## Задание

    Используя django, реализовать приложение, которое является агрегатором данных из access логов apache с сохранением в БД.
    Разбор файлов должен выполняться по cron'у .

    В приложении реализовать такие функции:
    - авторизация (пользователи в БД)
    - просмотр данных сохраненных в БД (группировка по IP, по дате, выборка по промежутку дат)
    - API для получения данных в виде JSON (смысл тот же: получение данных по временному промежутку, возможность группировать/фильтровать по IP)
    - конфигурация через файл настроек (где лежат логи, маска файлов, и все, что Вам потребуется для настройки приложения)

## Установка

- Создание виртуальной среды и клонирование репозитория

      $ mkdir aggregator_logs
      $ cd aggregator_logs
      $ python3 -m venv .env
      $ source .env/bin/activate
      (.env) $ python -m pip install -r requirements.txt
      (.env) $ git clone https://github.com/satisataka/django-aggregator-logs-access-apache.git .

## Настройка setting.py

- __DATABASES__ - настройте в соотвествии с настройками вашей базы данных.
- __PARSER_LOG_PATH__ - укажите путь и маску ваших логов например: "home/user/logs/*.log"
  - __По умолчанию:__ указывает на файл "/test_logs/apache_logs", который находится внутри проекта.
  - __Внимание:__ система запоминает лог-файлы по их полному пути, если вы перенесете или переименуете файл, система будет считать, что это новый файл.
  - __Внимание:__ система запоминает последнюю позицию указателя и последнюю сохраненную строку лог-файла. Каждый раз когда система открывает знакомый файл. Она сверяет последнюю строку в бд, и последнюю строку в лог-файле на которую указывает указатель, если эти строки не совпадают, файл будет читаться сначала.
- __PARSER_LOG_CREATED_SINGLE_QUERY__ - количество логов которые будут одновремеено записываться в базу данных.
  - __По умолчанию:__ 100
  - __Если установить 0:__ логи будут по одному записываться в базу данных (не рекомендовано).
  - __Если установить -1 (любой отрицательное число):__ сначала все логи запишутся в память, а потом в бд (не рекомендовано: опасно переполнением памяти).
  
- __CRONJOBS__ - также можете настроить, в соответсвии [django-cron](https://django-cron.readthedocs.io/en/latest/installation.html).
  - __По умолчанию:__ "'*/5 * * * *', 'log_access_apache.utils.parser_log'" - запуск скрипта каждые 5 мин.

## Запуск проекта
- Для начала, сделаем миграции:

      (.env) $ python manage.py migration

- Проверим скрипт парсера логов, запустим его вручную:

      (.env) $ python manage.py shell
      >>> from log_access_apache.utils import parser_log
      >>> parser_log()

      # Если не повилось ошибок, значит всё настроено верно и первые записи уже появились в базе данных.

      >>> exit()

- Создаём пользователя, запускаем __cron__ и сам проект:

      (.env) $python manage.py createsuperuser
      Username: admin
      Password: admin
      Password (again): admin
      Superuser created successfully.
      (.env) $ python manage.py crontab add
      (.env) $ python manage.py runserver

## Авторизация, просмотр данных и фильтрация (Django Views)

  - открываем в браузере: http://127.0.0.1:8000/
  - авторизуемся
  - Доступные фильтры:
    - по IP адресу
    - По промежутку дат
    - По промежутку времени

## Авторизация, просмотр данных и фильтрация (Django REST Api)

### Get Api Token

#### Request
    http post http://127.0.0.1:8000/api/api-token-auth/ username=admin password=admin
#### Response
    HTTP/1.1 200 OK
    Allow: POST, OPTIONS
    Content-Length: 52
    Content-Type: application/json
    Date: Fri, 15 Apr 2022 16:18:17 GMT
    Referrer-Policy: same-origin
    Server: WSGIServer/0.2 CPython/3.10.4
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY

    {
        "token": "9e5be409054237d8e40dcc1352957dbdd0605758"
    }

### Get All Logs
Выводится по 100шт на страницу, так же доступна пагинация и ссылки на каждый отдельный лог

#### Request
    http http://127.0.0.1:8000/api/logs-list/ 'Authorization: Token 9e5be409054237d8e40dcc1352957dbdd0605758'

#### Response
    HTTP/1.1 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Length: 38678
    Content-Type: application/json
    Date: Fri, 15 Apr 2022 16:26:13 GMT
    Referrer-Policy: same-origin
    Server: WSGIServer/0.2 CPython/3.10.4
    Vary: Accept
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY

    {
        "count": 10025,
        "next": "http://127.0.0.1:8000/api/logs-list/?page=2",
        "previous": null,
        "results": [
            {
                "bytes": 1015,
                "date": "2015-05-17T13:05:00+03:00",
                "host": "66.249.73.185",
                "logname": null,
                "referer": null,
                "request_line": "GET /reset.css HTTP/1.1",
                "status": 200,
                "url": "http://127.0.0.1:8000/api/log/101272/",
                "user": null,
                "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            },

            ...

        ]
    }

### Get Filter Logs
  Отфильтрованные логи

  Выводится по 100шт на страницу, так же доступна пагинация и ссылки на каждый отдельный лог

- Доступные фильтры (С примерами):
  - IP адрес
    - host=209.85.238.199
  - Промежуток дат {год}-{месяц}-{день}:
    - date_min=2015-05-18
    - date_max=2015-05-19
  - Промежуток времени {часы}:{минуты}:{секунды}:
    - time_min=07:00:00
    - time_max=08:00:00

    #### Request

        http 'http://127.0.0.1:8000/api/logs-list/?host=209.85.238.199&date_min=2015-05-18&date_max=2015-05-19&time_min=07:00:00&time_max=08:00:00' 'Authorization: Token 9e5be409054237d8e40dcc1352957dbdd0605758'

    #### Response

        HTTP/1.1 200 OK
        Allow: GET, HEAD, OPTIONS
        Content-Length: 1069
        Content-Type: application/json
        Date: Fri, 15 Apr 2022 19:55:49 GMT
        Referrer-Policy: same-origin
        Server: WSGIServer/0.2 CPython/3.10.4
        Vary: Accept
        X-Content-Type-Options: nosniff
        X-Frame-Options: DENY

        {
            "count": 3,
            "next": null,
            "previous": null,
            "results": [
                {
                    "bytes": 32352,
                    "date": "2015-05-18T07:05:08+03:00",
                    "host": "209.85.238.199",
                    "logname": null,
                    "referer": null,
                    "request_line": "GET /?flav=atom HTTP/1.1",
                    "status": 200,
                    "url": "http://127.0.0.1:8000/api/log/103375/",
                    "user": null,
                    "user_agent": "Feedfetcher-Google; (+http://www.google.com/feedfetcher.html; 16 subscribers; feed-id=3389821348893992437)"
                },
                {
                    "bytes": 1370,
                    "date": "2015-05-18T07:05:22+03:00",
                    "host": "209.85.238.199",
                    "logname": null,
                    "referer": null,
                    "request_line": "GET /test.xml HTTP/1.1",
                    "status": 200,
                    "url": "http://127.0.0.1:8000/api/log/103404/",
                    "user": null,
                    "user_agent": "Feedfetcher-Google; (+http://www.google.com/feedfetcher.html; 1 subscribers; feed-id=11390274670024826467)"
                },
                {
                    "bytes": 29941,
                    "date": "2015-05-18T07:05:24+03:00",
                    "host": "209.85.238.199",
                    "logname": null,
                    "referer": null,
                    "request_line": "GET /?flav=rss20 HTTP/1.1",
                    "status": 200,
                    "url": "http://127.0.0.1:8000/api/log/103382/",
                    "user": null,
                    "user_agent": "Feedfetcher-Google; (+http://www.google.com/feedfetcher.html; 22 subscribers; feed-id=8321906634162087507)"
                }
            ]
        }

