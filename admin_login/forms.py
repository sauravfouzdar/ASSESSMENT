from django.forms import ModelForm
from django import forms
from .models import StudentModel,TestModel,AnswerModel

# Create the form class.
class StudentForm(ModelForm):
    class Meta:
        model = StudentModel
        fields = '__all__'

        
class TestForm(ModelForm):
    class Meta:
        model = TestModel
        exclude = ['test_id','email','grading_id']

class AnswerForm(ModelForm):
    class Meta:
        model = AnswerModel
        #fields = '__all__'
        fields = ['answer_paper']

class ExcelForm(forms.Form):
   # test_id = forms.CharField(max_length=50)
    excel_file = forms.FileField(required=True)

