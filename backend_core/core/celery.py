import os
from celery import Celery

# Thiết lập module settings mặc định cho Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Load config từ settings.py của Django, namespace 'CELERY' có nghĩa là
# các biến config sẽ bắt đầu bằng CELERY_ (ví dụ CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động tìm tasks.py trong các installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')