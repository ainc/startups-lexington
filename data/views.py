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
                curr_stage = get_current_stage(company=obj)
                current_stage_list.append(curr_stage.stage.title)
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
        # try:
        #     current_stage = CompanyStageReport.objects.filter(company=self.company).latest('date_updated')
        # except ObjectDoesNotExist:
        #     current_stage = "No report"

        context['current_stage'] = get_current_stage(self.company)

        return context

    

class CompanyGrowthList(ListView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def get_current_stage(company):
    try:
        current_stage = CompanyStageReport.objects.filter(company=company).latest('date_updated')
    except ObjectDoesNotExist:
        current_stage = "No Report"

    return current_stage

def chart_data(request):
    stage_reports = CompanyStageReport.objects.all()
    companies = Company.objects.all()

    company_stages = []
    for c in companies:
        company_stages.append(get_current_stage(c))

    print(company_stages)

    stage_counts = {}

    for s in company_stages:
        print(s)
        if s.stage.id not in stage_counts:
            stage_counts[s.stage.id] = {
                'name': s.stage.title,
                'y': 0
            }
        stage_counts[s.stage.id]['y'] += 1
        

    print(stage_counts)
    print(list(map(lambda row: {'name': stage_counts[row]['name'], 'y': stage_counts[row]['y']}, stage_counts)))


    # stage_nums = {}
    # test = []
    # for s in range(len(dataset)):
    #     test.append({'name': dataset[s].company.name, 'y': dataset[s].stage.get_stage_number()})
    #     stage_nums[dataset[s].company.name] = dataset[s].stage.get_stage_number()
    
    # print(test)

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Stage Reports'},
        'series': [{
            'name': 'Companies',
            'colorByPoint': True,
            'data': list(map(lambda row: {'name': stage_counts[row]['name'], 'y': stage_counts[row]['y']}, stage_counts))
            # 'data': list(map(lambda row: {'name': row.stage.get_stage_number(), 'y': 0}, dataset))
        }]
    }

    return JsonResponse(chart)
