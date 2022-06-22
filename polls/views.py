from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from polls.form import SubjectForm, QuestionForm

from polls.models import Question, Choice, Subject


def list_subjects(request):
    form = SubjectForm()
    latest_subject_list = Subject.objects.order_by('-pub_date')[:5]
    context = {'latest_subject_list': latest_subject_list,
               'form': form}
    return render(request, 'polls/list_subjects.html', context, )


def add_subject_form(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            post_subject = form.cleaned_data['subject']
            new_post = Subject(subject_text=post_subject)
            new_post.save()
            return redirect('list_subjects')
    elif request.method == 'GET':
        form = SubjectForm()
        return render(request, 'polls/add_subject_form.html', {'form': form})


def deleteSubject(request, subject_id):
    item = Subject.objects.get(id=subject_id)
    item.delete()
    return redirect('list_subjects')


def changeSubjectName(request, subject_id):
    print("ID: {}".format(subject_id))
    data = request.POST
    print("====== request: {}".format(data))

    form = SubjectForm(data)
    if form.is_valid():
        new_subject_name = form.cleaned_data['subject']
        print("========== form subject: {}".format(new_subject_name))
        subject = Subject.objects.get(id=subject_id)
        subject.subject_text = new_subject_name
        subject.save()
        return redirect('list_subjects')
    else:
        print("ERROR !!!")
        return redirect('add_subject_form')


def question_list_by_subject(request, subject_id):
    latest_question_list = Question.objects.filter(subject_id=subject_id)
    context = {'latest_question_list': latest_question_list,
                'subject_id': subject_id}
    print("---->", context)
    return render(request, 'polls/question_list_by_subject.html', context)


def vote_choice_view(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/vote_choice_view.html', {'question': question})


def add_question_form(request, subject_id):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # post_choice = form.cleaned_data['choice']
            post_question = form.cleaned_data['question']
            subject = Subject.objects.get(id=subject_id)
            new_post = Question(question_text=post_question, subject=subject)
            new_post.save()
            context = {'subject_id': subject_id}
            # return redirect('question_list_by_subject')

            return render(request=request, template_name='polls/question_list_by_subject.html', context=context)
    elif request.method == 'GET':
        context = {
            'form': QuestionForm(),
            'subject_id': subject_id
        }
        return render(request=request, template_name='polls/add_question_form.html', context=context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/vote_choice_view.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
