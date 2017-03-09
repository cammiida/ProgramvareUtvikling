from django import forms

class Questions(forms.Form):
    question=forms.CharField(max_length=500)
    value=forms.IntegerField(default=0)