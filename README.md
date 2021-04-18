# Better MAL Credits

[bettermalcredits.moe](https://bettermalcredits.moe)

Website that let's you browse, sort and filter credits of anime creators.
```
MAL - My Anime List. A IMDb style website for anime (japanese animation)
```

## Technologies used
- backend - python
  - website itself using Flask framework
  - handling database operations by ORM - SQLAlchemy
  - Celery Task Que for asynchronous operations of downloading and updating pages
  - information on pages taken from My Anime List website via Jikan, it's unofficial API
- no frontend frameworks
  - few javascript files for implemening table sorting and filtering, dynamic searching.
  - no html/css libraries like bootstrap, visual and layout is created using css files.

## Main stack
- nginx -> uwsgi -> flask app
- MySQL database
- Celery worker

## Hosting
Website is hosted on a VPS with Debian 10 installed. Everything was set up manually.
Production version is updated using GitHub.
