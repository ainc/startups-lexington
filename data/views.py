from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Company, Founder, CompanyStageReport
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import HttpResponse, JsonResponse

class CompanyList(ListView):
    model = Company
    context_object_name = "companies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_stage_list = []
        for obj in self.object_list:
            if obj.company_stage_report.all():
                current_stage_list.append(obj.company_stage_report.all()[0].stage.title)
            else:
                current_stage_list.append("No report")
        company_list = zip(self.object_list, current_stage_list)
        context['company_list'] = company_list

        context['chart_data'] = chart_data(self)
        
        return context

class CompanyDetail(DetailView):
    model = Company
    context_object_name = "company"
    slug_field = 'company_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.company = get_object_or_404(Company, pk=self.kwargs['pk'])
        context['founders'] = Founder.objects.filter(company=self.company)
        context['stages'] = CompanyStageReport.objects.filter(company=self.company)
        try:
            current_stage = CompanyStageReport.objects.filter(company=self.company).latest('date_updated')
        except ObjectDoesNotExist:
            current_stage = "No report"

        context['current_stage'] = current_stage

        return context

    

class CompanyGrowthList(ListView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def chart_data(request):
    dataset = CompanyStageReport.objects.all().order_by('stage')

    stage_nums = []
    for s in range(len(dataset)):
        stage_nums.append(dataset[s].stage.get_stage_number())

    print(stage_nums)

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Stage Reports'},
        'series': [{
            'name': 'Stage #',
            'data': list(map(lambda row: {'name': stage_nums[row], 'y': 2}, dataset))
        }]
    }

    return JsonResponse(chart)
