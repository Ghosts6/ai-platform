from django.urls import path
from .views import ContactMessageView, ChatHistoryView, ChatSessionView, LastChatSessionView

urlpatterns = [
    path('contact/', ContactMessageView.as_view(), name='contact_message'),
    path('chat/history/', ChatHistoryView.as_view(), name='chat_history'),
    path('chat/session/<int:session_id>/', ChatSessionView.as_view(), name='chat_session'),
    path('chat/last/', LastChatSessionView.as_view(), name='last_chat_session'),
]
