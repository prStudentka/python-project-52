from django.urls import path
from task_manager.statuses import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='status_index'),
    path('create/', views.StatusCreateView.as_view(), name='create status'),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name='update status'),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='delete status'),
]
