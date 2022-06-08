
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from polls.forms import PostForm


from polls.models import Question, Choice, Subject


def index(request):
    latest_subject_list = Subject.objects.order_by('-pub_date')[:5]
    context = {'latest_subject_list': latest_subject_list}
    return render(request, 'polls/index.html', context, )


def post_new(request):
    form = PostForm()
    return render(request, 'polls/index.html', {'form': form})


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
