from django.forms.models import ModelChoiceField

class ExerciseModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.desc_long
    
    
