from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.list_subjects, name='list_subjects'),
    path('add_subject/', views.add_subject_form, name='add_subject'),

    path('<int:subject_id>/delete', views.deleteSubject, name='deleteSubject'),
    path('<int:subject_id>/edit', views.changeSubjectName, name='changeSubjectName'),
    path('<int:subject_id>/', views.quest, name='quest'),
    path('question/<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

]