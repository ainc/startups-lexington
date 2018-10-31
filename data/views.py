from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Company, Founder
from django.shortcuts import get_object_or_404

class CompanyList(ListView):
    model = Company
    context_object_name = "companies"

class CompanyDetail(DetailView):
    model = Company
    context_object_name = "company"
    slug_field = 'company_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        context['founders'] = Founder.objects.filter(company=self.company)

        return context
