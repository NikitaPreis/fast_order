# Fast Order

### Описание

«Fast Order» — это веб-приложение для управления заказами в кафе. Приложение позволяет добавлять, удалять, искать, изменять и отображать заказы. Подготовлена админ-зона проекта: администратор может создавать категории позиций в меню (Например: Напитки, Горячее) и позиции в меню, связанные с категориями. Также подготовлено API для работы с заказами.

### Стек технологий:

* Python (3.12.7)
* Django
* Django REST framework
* PostgreSQL
* Docker


### Как развернуть проект:

Клонировать репозиторий:
```
git clone git@github.com:NikitaPreis/fast_order.git
cd fast_order

```

Создать и активировать виртуальное окружение, установить зависимости:
```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

Установить переменные окружения в файле .env:
```
# Переменные окружения для работы с БД (Docker Compose, PostgreSQL)
POSTGRES_DB=fast_order
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
DB_HOST=localhost
DB_PORT=5432

# Секретный ключ приложения
SECRET_KEY=django-insecure-sdx)ip1^-ik@r4+jeos3iwkl27ux7lkis2d&vklfi)sqh-ih7g

# Значение DEBUG
DEBUG = True

```

Запустить БД:
```
docker compose -f docker-compose.yml up
```

Создать и выполнить миграции, создать администратора:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Запустить локальный сервер:
```
python manage.py runserver
```


### Страницы с веб-интерфейсом

**Примечание: создать категории и позиции в меню можно в админ-зоне**

1. Таблица заказов с поиском и пагинацией

* **url**: http://127.0.0.1:8000/
* **Описание**: Страница отображает список заказов с поисковой строкой и пагинацией. Пользователь может выполнить поиск по полям заказа: номер стола, статус *(Например, поисковый запрос «24 Оплачено» выведет в таблице все заказы, у которых номер стола «24» и статус «Оплачено»)*.

2. Создание заказа

* **url**: http://127.0.0.1:8000/create
* **Описание**: Страница отображает форму для создания заказа. Пользователь указывает номер стола, статус заказа и выбирает позиции заказа. После создания заказа пользователь видит ID заказа, статус и общую стоимость позиций.

3. Обновление статуса заказа

* **url**: http://127.0.0.1:8000/{order_id}/update_status/
* **Описание**: Пользователь выбирает статус заказа и отправляет форму. После обновления статуса пользователь видит обновленный статус.

4. Удаление заказа

* **url**: http://127.0.0.1:8000/{order_id}/delete/
* **Описание**: Пользователь проверяет данные заказа (Номер стола, статус) и отправляет форму. После удаления пользователя переадресует на страницу с заказами.

5. Выручка

* **url**: http://127.0.0.1:8000/sales_revenues
* **Описание**: Пользователь вводит в форму 2 даты, ограничивающие период, за который необходимо расчитать выручку. В ответ пользователь получает сумму выручки за указанный период (Учитываются только заказы со статусом «Оплачено»).


### Fast Order API

#### Список доступных эндпоинтов:

1) **Заказы**
* **url**: http://127.0.0.1:8000/orders/
* **Методы**: GET, POST
2) **Заказы (Detail)**
* **url**: http://127.0.0.1:8000/orders/{order_id}
* **Методы**: PATCH, DELETE 
3) **Выручка**
* **url**: http://localhost:8000/api/orders/sales_revenue
* **Методы**: GET

#### Примеры запросов и ответов:


**request samples №1:**
```
Method: GET
URL: http://localhost:8000/api/orders/?search=10,Оплачено
```

**response sample №1:**
```
[
    {
        "id": 5,
        "table_number": 10,
        "items": [
            "Кофе: 100.00 RUB",
            "Пицца: 250.00 RUB"
        ],
        "status": "Оплачено",
        "total_price": "350.00"
    },
    {
        "id": 7,
        "table_number": 10,
        "items": [
            "Кофе: 100.00 RUB"
        ],
        "status": "Оплачено",
        "total_price": "100.00"
    }
]
```

**request sample №2:**
```
Method: POST
URL: http://localhost:8000/api/orders/
```

**payload №2:**

```
{
    "table_number": 4,
    "items": [
        1,
        2
    ]
}
```

**response sample №2:**
```
{
    "id": 10,
    "table_number": 4,
    "items": [
        "Кофе: 100.00 RUB",
        "Пицца: 250.00 RUB"
    ],
    "status": "В ожидании",
    "total_price": "350.00"
}
```

**request sample №3:**
```
Method: PATCH
URL: http://localhost:8000/api/orders/10/
```

**payload №3:**

```
{
    "status": "Оплачено"
}
```

**response sample №3:**
```
{
    "id": 10,
    "table_number": 4,
    "items": [
        "Кофе: 100.00 RUB",
        "Пицца: 250.00 RUB"
    ],
    "status": "Оплачено",
    "total_price": "350.00"
}
```

**request sample №4:**
```
Method: DELETE
URL: http://localhost:8000/api/orders/10/
```

**response sample №4:**
```
{NoReturn}
```

**request sample №5:**
```
Method: GET
URL: http://localhost:8000/api/orders/sales_revenue?from_date=2025-03-31&to_date=2025-04-02
```

**response sample №5:**
```
{
    "from_date": "2025-03-31",
    "to_date": "2025-04-02",
    "sales_revenue": 1400.00
}
```
