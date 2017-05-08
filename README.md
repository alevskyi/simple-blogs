### Abstract:
This is a blog service which consists of posts created by registered users.
No registration required for browsing posts and commenting.
However, in order to post a new article user must be authenticated.
For navigation resource has a search form which takes a regex as input and performing matches by post theme, text, or author.
Search results can be narrowed by specifying a date range, sorted by date or amount of comments, and divided by pages (```POSTS_PER_PAGE``` variable in settings, by default 2 posts per page).

### Screenshots:
Main page
![main](https://cloud.githubusercontent.com/assets/27825950/25802817/c1e64cec-33fc-11e7-9803-7c2c477a7143.jpg)
Specific post
![detailed](https://cloud.githubusercontent.com/assets/27825950/25802835/d3885544-33fc-11e7-88c8-2065ae9cc54b.jpg)

### How to run:
Execute ```python manage.py runserver``` in project root, server will start on ```localhost:8000```
