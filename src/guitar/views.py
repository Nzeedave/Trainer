from django.shortcuts import render, redirect
from django.http import HttpResponse
from guitar.forms import ExerciseDataForm, RoutineDataForm, RoutineItemForm, CategoryForm
from guitar.forms import ExerciseForm, RoutineItemForm_Exercise
from guitar.models import Exercise, ExerciseData, Category, Routine, RoutineItem
from django.db.models.sql.where import NothingNode

def select_exercise(request):
    
    exercise_list = Exercise.objects.all()
    context_dict = {'exercises': exercise_list}
    
    
    return render(request, 'guitar/select_exercise.html', context_dict)


def select_routine(request):
    routine_list = Routine.objects.all()
    context_dict = {'routines': routine_list}
    address = 'guitar/select_routine.html'
    
    return render(request, address, context_dict)
    
def exercise(request, exercise_id, data_id = None):

    exercise = Exercise.objects.get(id = exercise_id)
    context_dict = {}
    address = 'guitar/exercising.html'
    if exercising_util(request, exercise, context_dict):
        return select_exercise(request)
    return render(request, address, context_dict)

def exercising_util(request, exercise, context_dict = {}):
    # Returns True if an Entry is saved -> open next page
    # Returns False if Not -> do nothing

    if request.method == 'POST':
        
        form = ExerciseDataForm(request.POST, ex = exercise.id)
        
        if form.is_valid():
            
            ex_data = form.save(commit=False)
            ex_data.exercise = exercise

            ex_data.save()
            print("Old record:" + str(exercise.record))
            exercise.record = max(int(exercise.record), int(ex_data.count))
            print("New record: " + str(exercise.record))
            if ex_data.time > 0:
                exercise.save()
                print("Saving")
            
            return True
    
    else: 
        form = ExerciseDataForm(ex = exercise.id)
    
    context_dict['exercise_desc'] = exercise.desc_long
    context_dict['form'] = form
    context_dict['request_path'] = str(request.path)
    
    return False


def routine_exercise(request, routine_slug, item_id):
    
    context_dict = {}
    
    try:
        i = int(item_id) - 1
        routine = Routine.objects.get(slug = routine_slug)
        context_dict['routine_count'] = routine.count()
        context_dict['routine_items'] = routine.get_items()
        context_dict['routine_slug'] = routine_slug
                
        if not routine.check_id(i):
            return redirect('show_routine', routine_slug)
            
        exercise = routine.get_items()[i].exercise
        context_dict['current_routine'] = exercise           
                 
        if i > 0: 
            context_dict['previous_id'] = i
        if i < routine.count() - 1:
            context_dict['next_id'] = i + 2
        
        if exercising_util(request, exercise, context_dict):  
             
            next_id = int(item_id) + 1
            if(routine.check_id(next_id - 1)):
                return redirect('routine_exercise', routine_slug, next_id)
            else:
                return redirect('routine_finish', routine_slug)
        
        
        context_dict['exercise_id'] = exercise.id
        context_dict['item_id'] = item_id
        context_dict['i'] = i
                    
    except Routine.DoesNotExist:
        pass
    
    address = 'guitar/routine_item.html'
    return render(request, address, context_dict)

def show_routine(request, routine_slug):
    
    context_dict = {}                

    try:
        routine = Routine.objects.get(slug = routine_slug)
        context_dict['routine_slug'] = routine.slug
        context_dict['routine'] = routine
        
        exercise_items = RoutineItem.objects.filter(routine = routine)
        context_dict['items'] = exercise_items
        
    except Routine.DoesNotExist:
        pass
    address = 'guitar/show_routine.html'
    return render(request, address, context_dict )

def test(request,):
    
    exercises = Exercise.objects.all()
    items = RoutineItem.objects.all()
    form = RoutineItemForm_Exercise
    
    if request.method == 'POST':
        print(request.POST)
        form = RoutineItemForm_Exercise( request.POST)
        if form.is_valid():
            print("Counts as valid")
            
            routine_item = RoutineItem.objects.get_or_create( routine = Routine.objects.get( slug = 'standard'),
                                                              order = 1)[0]
            routine_item.exercise = form.save(commit = False).exercise
            
            print("    Routine: " + routine_item.routine.slug)
            print("    Order: " + str(routine_item.order))
            print("    Exercise: " + routine_item.exercise.desc )
            print("Is valid")
            routine_item.save(force_update =True)
            return redirect(request.path)
    
    context_dict = { 
                    'exercises': exercises, 
                    'form': form,
                    'items': items,
                }
    
    address = 'guitar/test.html'
    
    return render(request, address, context_dict)

def routine_abort(request, routine_slug):
    return redirect('show_routine', routine_slug)

def routine_finish(request, routine_slug):
    print('Finished')
    return redirect('show_routine', routine_slug)

def routine_edit(request,routine_slug):
    context_dict= {}

    
    try:
        routine = Routine.objects.get(slug = routine_slug)
        context_dict['routine'] = routine
        context_dict['routine_items'] = routine.get_items()
    except Routine.DoesNotExist:
        pass
    
    address = 'guitar/edit_routine.html'
    return render(request, address, context_dict)
    
def routine_item_edit(request, routine_slug, routine_item_id=None):
    
    context_dict = {
            'routine_slug': routine_slug,
            'routine_item_id': routine_item_id,
            }
    
    routine= Routine.objects.get(slug = routine_slug)
    context_dict['current'] =  routine.get_items()[int(routine_item_id) - 1]
    form = RoutineItemForm( instance =  routine.get_items()[int(routine_item_id) - 1] )
    context_dict['form'] = form
    context_dict['routine_items']=routine.get_items()
    address = 'guitar/edit_routine_item.html'
    return render(request, address, context_dict)


def create_category(request):
    context_dict = {}
    address = "guitar/create_category.html"
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():

            form.save()
                
            return list_categories(request)
        
        else: 
            context_dict['form'] = form
            return render(request, address, context_dict)
    
    context_dict['form'] = CategoryForm()
    return render(request, address, context_dict)

def list_categories(request):
    context_dict = { 
            'table_header': Category.table_header(),
            'dataset': Category.objects.all()
            }
    
    address = 'guitar/standard_table.html'
    return render(request, address, context_dict)

def create_exercise(request):
    address = "guitar/create_exercise.html"
    context_dict = {}
    
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return list_exercises(request)
        
    else:
        form = ExerciseForm()  
        
    context_dict['form'] = form
           
            
    return render(request, address, context_dict)

def list_exercises(request):
    context_dict = { 
            'table_header': Exercise.table_header(),
            'dataset': Exercise.objects.all(),
            }
    
    address = 'guitar/standard_table.html'
    return render(request, address, context_dict)

# This creates a new RoutineItem 

def replace_routine_item(request, routine_slug, position):
    
    address = ""
    context_dict = {}
    
    return render(request. address, context_dict)

def insert_routine_item(request, routine_slug, position):
    # Creates 
    
    routine_item = RoutineItem()
    address = ""
    context_dict = {}
    
    
    
    try:
        
        if request.method == 'POST':
            routine = Routine.objects.get( slug = routine_slug)
            routine.cleanup_order()
            routine.insert(position)
            
            routine_item.routine = routine
            routine_item.order = position
    except Routine.DoesNotExist:
        pass
            
    return render(request. address, context_dict)
