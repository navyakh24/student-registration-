from django import forms
from.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__' # This is used to specify the fields that we want to include in the form. We can also exclude fields by using the exclude attribute instead of fields.