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
    
    def cleanup_order(self):
        i = 1
        for item in self.get_items():
            item.order = i;
            i = i+1
            item.save()
    
    def insert(self, position):
        for item in RoutineItem.objects.filter( routine = self).filter( order__gte = position).order_by('order').reverse():
            item.order = item.order + 1;
            item.save()
    
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
    
    @staticmethod
    def table_header():
        return[
                "Name",
                "Time",
                "Target"
            ]
    
    def table_data(self):
        return [
                [self.name, "name"],
                [self.time, 'time'],
                [self.target, "target"]
            ]
    
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
    
    @staticmethod
    def table_header():
        return [
                "Category",
                "Description",
                "Comment",
                "Url",
                "# Completed",
                "Last Done"
            ]
    
    def table_tags(self):
        return [
                "category",
                "description",
                "comment",
                "url",
                "count",
                "last"
            ]
    
    def table_data(self):
        if self.url != '':
            link_tag = '<a href="' + self.url + '"> Link </a>'
        else: 
            link_tag = ''
        return [ 
                [self.category, "category"],
                [self.desc_long, "desc_long"],
                [self.comment, "comment"],
                [link_tag, "link"],
                [self.count_times(), "count"],
                [self.last_time(), "last"]
                ]
    def count_times(self):
        return ExerciseData.objects.filter(exercise = self).count()
    
    def last_time(self):
        if self.count_times() > 0:
            return ExerciseData.objects.filter(exercise = self).order_by('date').reverse()[0]
        return 0
    
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


    
    
