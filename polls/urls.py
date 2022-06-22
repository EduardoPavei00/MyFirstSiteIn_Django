from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.list_subjects, name='list_subjects'),


    path('add_subject/', views.add_subject_form, name='add_subject'),

    path('<int:subject_id>/delete', views.deleteSubject, name='deleteSubject'),

    path('<int:subject_id>/edit', views.changeSubjectName, name='changeSubjectName'),

    path('<int:subject_id>/add_question', views.add_question_form, name='add_question_form'),

    path('<int:subject_id>/list_questions', views.question_list_by_subject, name='question_list_by_subject'),

    path('<int:question_id>/question', views.vote_choice_view, name='vote_choice_view'),

    path('<int:question_id>/results/', views.results, name='results'),

    path('<int:question_id>/vote/', views.vote, name='vote'),


]