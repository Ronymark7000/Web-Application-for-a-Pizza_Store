from django.shortcuts import render
from django.forms import formset_factory
from .models import Pizza

from .forms import PizzaForm, MultiplePizzaForms

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    mulitple_form = MultiplePizzaForms()
    if request.method == 'POST':
        #for immage accept garna lie
        filled_form = PizzaForm(request.POST)
        #request.FILES
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = 'Thank you for your order of {} {} and {} pizza' .format(filled_form.cleaned_data['size'], filled_form.cleaned_data['topping1'], filled_form.cleaned_data['topping2'])
            filled_form = PizzaForm()
        else:
            created_pizza_pk = None
            note = "Pizza Order has failed"
        return render(request, 'pizza/order.html', {'created_pizza_pk': created_pizza_pk, 'pizzaform':filled_form, 'note':note, 'multiple_form': mulitple_form})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform':form, 'multiple_form':mulitple_form})

#form set ko part ...not totally understood
def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForms(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = 'Pizzas have been ordered'
        else:
            note = 'Order was not created. Please order again' 
        return render(request, 'pizza/pizzas.html', {'note':note, 'formset':formset})
    else:
        return render(request, 'pizza/pizzas.html', {'formset':formset})
    
def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = 'Order has been pdated'
            return render(request, 'pizza/edit_order.html', {'note':note, 'pizzaform':form, 'pizza':pizza},)
    return render(request, 'pizza/edit_order.html', {'pizzaform':form, 'pizza':pizza},)

        

