from django.urls import path
from .views import save_enquiry, chat_reply

urlpatterns = [
    path("save-enquiry/", save_enquiry),
    path("chat/", chat_reply),
]
