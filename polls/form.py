from django import forms

from polls.models import Subject


class PostForm(forms.Form):
    subject = forms.CharField(label='subject')
    model = Subject
    fields = ('subject_text',)

