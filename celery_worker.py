from app import create_app, celery

#跟wsgi一樣都要放在外面，給他啟動服務器
app = create_app(celery=celery)