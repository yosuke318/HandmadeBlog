# HandmadeBlog

``````
docker compose build
``````

```
docker compose up -d
```

```
docker exec -it blog_backend bash
```

#### 初回の場合migrateコマンドを実行
```
python manage.py migrate
```


```
python manage.py runserver 0.0.0.0:8000
```

### DB migrate後、以下のコマンドで起動

```
docker compose up -d
```

### localhost:8000にアクセス
<img src="blog_initail.png">