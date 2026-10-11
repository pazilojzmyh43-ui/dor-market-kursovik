# DoorMarket

Салон дверей. Веб-проект Django для Visual Studio 2019 (шаблон «Веб-проект Django»).

## Как открыть

1. Установить Python 3.7 (в лаборатории) или 3.8–3.10 и Django из `DoorMarket/requirements.txt`:
   `pip install -r DoorMarket/requirements.txt`
2. Открыть `DoorMarket.sln` в Visual Studio 2019.
3. В обозревателе решений: проект `DoorMarket`, среда Python 3.7, запуск — Django (`manage.py runserver`).
4. В каталоге проекта выполнить миграции и заполнение базы, если файла `db.sqlite3` ещё нет:
   - `python manage.py migrate`
   - `python manage.py seed`

## Учётные записи

| Роль | Логин | Пароль |
| --- | --- | --- |
| Администратор | admin | admin123 |
| Клиент | client | client123 |
| Менеджер | manager | manager123 |

Административный раздел Django: `/admin/`.
