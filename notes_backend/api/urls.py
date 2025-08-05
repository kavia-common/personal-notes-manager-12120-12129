from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health, RegisterView, LoginView, LogoutView, NoteViewSet

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='note')

urlpatterns = [
    path('health/', health, name='Health'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
