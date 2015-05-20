from django.db import models
from django.template.defaultfilters import slugify

# Creating my models here
#
# Necessary models:
#   Routine: Has the current routine
#           Will be overwritten with change?
#
#   Exercise:
#         Contains each exercise
#         Requires:     - Name -> Category
#                       - Detailed Information
#                       - time
#                       - target (in general number)
#                       - comment
#                       - link
#        More Advanced features:
#                       - Auto Start of website?



class Routine(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    slug = models.SlugField(unique = True)
        
    def count(self):
        return RoutineItem.objects.filter( routine = self ).count()
    
    def get_items(self):
        return RoutineItem.objects.filter( routine = self).order_by('order')
    
    def check_id(self, i = 0):
        if i < self.count() and i >= 0:
            return True
        return False
     
    
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Routine, self).save(*args, **kwargs)
    

class Category(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    time = models.IntegerField(default = 0)
    target = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    
class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category)
    desc = models.CharField(max_length = 128)
    desc_long = models.CharField(max_length = 512, blank = True)
    comment = models.CharField(max_length = 512, blank = True)
    url = models.URLField(blank = True)
    record = models.IntegerField(default = 0)
    time = models.IntegerField()
    
    def __unicode__(self):
        return self.desc
    def __str__(self):
        return self.desc
        
class RoutineItem(models.Model):
    routine = models.ForeignKey(Routine)
    exercise = models.ForeignKey(Exercise)
    order = models.IntegerField()
    class Meta:
        unique_together = ["routine", "order"]
    
class ExerciseData(models.Model):
    id = models.AutoField(primary_key = True)
    exercise = models.ForeignKey(Exercise)
    comment = models.CharField(max_length = 512, blank=True)
    time = models.IntegerField()
    count = models.IntegerField()
    date = models.DateField()
    
    def __unicode__(self):
        return str(self.date) + ' ' + str(self.exercise) + ' - ' + str(self.id)
    def __str__(self):
        return str(self.date) + ' ' + str(self.exercise) + ' - ' + str(self.id)


    
