from django.urls import path
from task_manager.tasks import views


urlpatterns = [
	path('', views.IndexView.as_view(), name='tasks_index'),
	path('create/', views.TaskCreateView.as_view(), name='create task'),
	path('<int:pk>/update/', views.TaskUpdateView.as_view(), name='update task'),
	path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete task'),
	path('<int:pk>/', views.TaskDetailView.as_view(), name='detail task'),

]