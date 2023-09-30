from django import forms
from .models import Question, Answer, Tag


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "body", "tags"]



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].widget = forms.Textarea(attrs={"rows": 5})


class SearchForm(forms.Form):
    query = forms.CharField()


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
