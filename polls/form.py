from django import forms

from polls.models import Subject


class SubjectForm(forms.Form):
    subject = forms.CharField(label='subject') # subject_name
    # model = Subject
    # fields = ('subject_text',)

