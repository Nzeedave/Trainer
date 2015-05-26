from django import forms
from guitar.models import Exercise, ExerciseData, Routine, RoutineItem, Category
import datetime
from guitar.fields import ExerciseModelChoiceField

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
        
class RoutineItemForm(forms.ModelForm):
    exercise = ExerciseModelChoiceField( Exercise.objects.all())
    routine = forms.ModelChoiceField( Routine.objects.all())
    order = forms.IntegerField()
    
    class Meta:
        model = RoutineItem
        fields= ('exercise', 'routine', 'order')
        
    
class CategoryForm(forms.ModelForm):
    name = forms.CharField
    time = forms.IntegerField(initial = 0)
    target = forms.IntegerField(initial = 0)
    
    class Meta:
        model = Category
        fields = ('name', 'time', 'target')
        
class ExerciseForm(forms.ModelForm):
    
    category = forms.ModelChoiceField( Category.objects.all() )
    desc = forms.CharField( max_length = 128)
    desc_long = forms.CharField( max_length = 512,  required = False)
    comment = forms.Textarea( )
    url = forms.URLField( required = False)
    record = forms.IntegerField( initial = 0)
    time = forms.IntegerField()
    
    class Meta:
        model = Exercise
        exclude = ('id',)
        