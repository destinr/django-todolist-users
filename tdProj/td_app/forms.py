from django import forms

class TaskForm(forms.Form):
    content = forms.CharField(max_length=100, initial ="Task", label=False)
    priority = forms.CharField(max_length= 1,initial ="Priority",label=False)