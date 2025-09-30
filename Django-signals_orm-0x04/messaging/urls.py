from messaging_app.messaging_app.urls import urlpatterns
from .views import DeleteUserView
from django.urls import path

urlpatterns = [
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
]