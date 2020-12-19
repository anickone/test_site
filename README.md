Тестовое задание

Создать Django-проект:

создать модель Product c полями:
● name - наименование
● description - описание продукта
● uuid - уникальный идентификатор
● created - дата создания
● updated - дата обновления
● logo - картинка
● rotate_duration - дробное

1. создать api-points(CRUD) для модели Product.
2. доступ к Product Details c использованием <uuid>. (пример /products/<uuid>/)
3. список продуктов должен содержать пагинацию на 10 элементов.
4. при загрузке файла logo, необходимо повернуть картинку на 180 градусов и
сохранить, так же необходимо сохранить длительность операции поворота в эту же Модель Product (rotate_duration) в секундах.
5. Необходимо реализовать возможность изменения Продукта только один раз(т.е. повторный запрос на изменение поля description, например, вернет соответствующее сообщение об ошибке)
6. добавить фильтр на апи-поинт списка продуктов, чтобы посмотреть какие из продуктов уже были модифицированы, а какие не были ( пример /products/?modified=true)

Так же:
1. Разместить проект в любом GIT-репозитории с доступом для: max@3dlook.me - Максим Алексеев
2. Обеспечить документирование проекта в README.MD
3. Использовать виртуальное окружения, предпочтительно c помощью pipenv
4. Использовать миграции
5. Следовать PEP8
6. Написать юнит тесты для всего, что считаете нужным
7. Сделать два варианта настроек: для разработки и для прода
8. Базовый язык - английский (в т.ч. для комментариев и строковых констант)
9. Обеспечить должное логирование основных процессов.



## Описание:
Проект развернут [здесь](http://anickone.pythonanywhere.com/) .

К модели Product добавлены поля: владелец(owner) и модификация(modified).

Список всех продуктов: [products/](http://anickone.pythonanywhere.com/products/) .

Список модифицированых продуктов: [products/?modified=true](http://anickone.pythonanywhere.com/products/?modified=true) .

Список не модифицированых продуктов: [products/?modified=false](http://anickone.pythonanywhere.com/products/?modified=false) .

Добавлено 3 settings.py:
    production_settings.py - секретный, добавлен в .gitignore
    development_settings.py - секретный, добавлен в .gitignore
    example_settings.py - для open source

выбираются указанием DJANGO_MODE в .env

echo "export DJANGO_MODE=development" > .env

users: admin, demo. password: цунамипароль в анг. раскадке.

## Requirements
    Python 3.8.0
    Django 2.2.17
    Django Rest Framework 3.12.2

## Install
```
pip install pipenv
pipenv shell
git clone https://github.com/anickone/test_site.git
cd test_site
pipenv install
python manage.py migrate
python manage.py makemigrations products
python manage.py migrate products
python manage.py runserver
```
[Open in browser http://127.0.0.1:8000/](http://127.0.0.1:8000/)
