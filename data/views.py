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

        context['stage_summary'] = stage_summary(self)
        # context['yearly_progress'] = yearly_progress(self)
        yearly_progress(self)
        
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

def stage_summary(request):
    stage_reports = CompanyStageReport.objects.all()
    companies = Company.objects.all()

    company_stages = []
    for c in companies:
        company_stages.append(get_current_stage(c))

    stage_counts = {}

    for s in company_stages:
        if s.stage.id not in stage_counts:
            stage_counts[s.stage.id] = {
                'name': s.stage.title,
                'y': 0
            }
        stage_counts[s.stage.id]['y'] += 1

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Stage Reports'},
        'series': [{
            'name': 'Companies',
            'colorByPoint': True,
            # Create list from dict
            'data': list(map(lambda row: {'name': stage_counts[row]['name'], 'y': stage_counts[row]['y']}, stage_counts))
            # 'data': list(map(lambda row: {'name': row.stage.get_stage_number(), 'y': 0}, dataset))
        }]
    }

    return JsonResponse(chart)

def yearly_progress(request):
    stage_reports = CompanyStageReport.objects.all().order_by('date_updated')
    companies = Company.objects.all()

    all_yearly_stages = {}
    for c in companies:
        company_yearly_stages = get_company_yearly_stages(c)
        # print(company_yearly_stages)
        for year, stage_report in company_yearly_stages.items():
            if year in all_yearly_stages:
                all_yearly_stages[year].append(stage_report)
            else:
                all_yearly_stages[year] = [stage_report]
    # print(all_yearly_stages)

    yearly_company_stages = {}

    print(list(map(lambda row: {'year': all_yearly_stages[row], 'y': all_yearly_stages[row]}, all_yearly_stages)))

    # chart = {
    #     'chart': {'type': 'line'},
    #     'title': {'text': 'Yearly Progress'},
    #     'series': [{
    #         'name': 'Stages',
    #         'colorByPoint': True,
    #         # Create list from dict
    #         'data': list(map(lambda row: {'year': all_yearly_stages[row], 'y': all_yearly_stages[row]}, all_yearly_stages))
    #         # 'data': list(map(lambda row: {'name': row.stage.get_stage_number(), 'y': 0}, dataset))
    #     }]
    # }


"""
Query to get unique yearly reports based on a company
param: company
return: dict of unique yearly reports
{year1: <CompanyStageReport>, year2: ...}
"""
def get_company_yearly_stages(company):
    stage_reports = CompanyStageReport.objects.filter(company=company).order_by('date_updated')
    yearly_company_reports = {}
    for s in stage_reports:
        if s.date_updated.year not in yearly_company_reports:
            yearly_company_reports[s.date_updated.year] = s
    return yearly_company_reports

    





