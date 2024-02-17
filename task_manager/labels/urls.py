from django.urls import path
from task_manager.labels import views


app_name = 'marked'


urlpatterns = [
	path('', views.LabelsView.as_view(), name='labels_index'),
	path('create/', views.LabelCreateView.as_view(), name='create label'),
	path('<int:pk>/update/', views.LabelUpdateView.as_view(), name='update label'),
	path('<int:pk>/delete/', views.LabelDeleteView.as_view(), name='delete label'),

]