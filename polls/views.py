from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from polls.form import SubjectForm

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

            return redirect('polls:list_subjects')
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


def quest(request, subject_id):
    latest_question_list = Question.objects.filter(subject_id=subject_id)
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/quest.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
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
