from django.urls import path # позволяет выстраивать маршруты
from .views import process_get_view, user_form, handle_file_upload

app_name='requestdataapp' # указывается имя приложения для того что
# бы этот фаил был отдельным пространтсвом имен
urlpatterns = [
    path('get/', process_get_view, name='get-view'),
    path('bio/', user_form, name='user-form'),
    path('upload/', handle_file_upload, name='file-upload'),
]
