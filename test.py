from celery import Celery

app = Celery("app", broker = "redis://127.0.0.1:6379")

@app.task
def add(x,y):
    return x+y