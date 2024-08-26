### Начальные найстроки

.env:

```
DJANGO_SECRET=123456
YOOKASSA_SHOP_ID=
YOOKASSA_SECRET_KEY=
YOOKASSA_RETURN_URL=
ALLOWED_HOSTS=1.2.3.4,mysite.com
```

### Установить зависимости

```
pip install -r requirements.txt 
```

### Загрузить ингредиенты

```
python manage.py loaddata ingredients.json
```
