from django import forms
from guitar.models import Exercise, ExerciseData, Routine
import datetime

class ExerciseDataForm(forms.ModelForm):
    ex = Exercise()
    
    def __init__(self,*args,**kwargs):
        str_ex = kwargs.pop('ex')
        super(ExerciseDataForm,self).__init__(*args,**kwargs)
        if str_ex != "":
            ex = Exercise.objects.get(id = int(str_ex))
            self.fields['comment'] = forms.CharField(max_length = 512, required = False, initial = ex.comment)
            self.fields['time'] = forms.IntegerField(initial = ex.time)
            self.fields['count'] = forms.IntegerField(initial = ex.record)
            self.fields['date'] = forms.DateField( initial = datetime.date.today())

    class Meta:
        model = ExerciseData
        exclude = ('exercise',)
      
class RoutineDataForm(forms.ModelForm):
    name = forms.CharField()
    class Meta:
        model = Routine
        fields = ('name',)
        