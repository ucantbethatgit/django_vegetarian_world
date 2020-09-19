from django.shortcuts import render

# Create your views here.

from catalog.models import Vegetable, Farmer, VegetableInstance, Family

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_vegetables = Vegetable.objects.all().count()
    num_instances = VegetableInstance.objects.all().count()
    
    # Available vegetables (status = 'a')
    num_instances_available = VegetableInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_farmers = Farmer.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    
    context = {
        'num_vegetables': num_vegetables,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_farmers': num_farmers,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class VegetableListView(generic.ListView):
    model = Vegetable

class VegetableDetailView(generic.DetailView):
    model = Vegetable

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedVegetablesByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing vegetables on loan to current user."""
    model = VegetableInstance
    template_name ='catalog/vegetableinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return VegetableInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('exp_date')

import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewVegetableForm

@permission_required('catalog.can_mark_returned')
def renew_vegetable_agrarian(request, pk):
    """View function for renewing a specific VegetableInstance by agrarian."""
    vegetable_instance = get_object_or_404(VegetableInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewVegetableForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model exp_date field)
            vegetable_instance.exp_date = form.cleaned_data['renewal_date']
            vegetable_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewVegetableForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'vegetable_instance': vegetable_instance,
    }

    return render(request, 'catalog/vegetable_renew_agrarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Farmer

class FarmerCreate(CreateView):
    model = Farmer
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class FarmerUpdate(UpdateView):
    model = Farmer
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class FarmerDelete(DeleteView):
    model = Farmer
    success_url = reverse_lazy('farmers')
