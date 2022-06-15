from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    #add Subject
    path('form/', views.form, name='form'),
    #delete Subject
    path('<int:subject_id>', views.deleteSubject, name='deleteSubject'),
    #edit subject
    path('<int:subject_id>', views.editSubjectPopup, name='editSubjectPopup'),

    path('<int:subject_id>/', views.quest, name='quest'),
    path('question/<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

]