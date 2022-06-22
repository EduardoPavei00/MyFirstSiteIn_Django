from django import forms

from polls.models import Subject


class SubjectForm(forms.Form):
    subject = forms.CharField(label='subject') #subject_name
    # model = Subject
    # fields = ('subject_text',)


class QuestionForm(forms.Form):
    question = forms.CharField(label='question')
    # choice = forms.CharField(label='choices')

