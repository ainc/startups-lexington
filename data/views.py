from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Company, Founder, CompanyStageReport, MasterStage
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
import json
import copy


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

def get_previous_company_report(report):
    # return None if new company
    try:
        prev_report = CompanyStageReport.objects.filter(date_updated__date__lt=report.date_updated.date(), company=report.company).latest('date_updated')
    except ObjectDoesNotExist:
        prev_report = None
    return prev_report

def stage_history(request):
    master_stages = MasterStage.objects.all().order_by('value')
    stage_reports = CompanyStageReport.objects.all()
    
    stage_history = {} # generate number of companies per stage for each new date
    stage_history['keys'] = [stage.title for stage in master_stages]
    stage_history['dates'] = {}
    for report in stage_reports:

        report_date = report.date_updated.date().strftime('%m/%d/%Y')

        # if the report is on a new date, create a new entry in stage_history
        if report_date not in stage_history['dates']:
            # if not the first date
            if stage_history['dates']:
                # load the previous date's companies per stage into to the new date
                stage_history['dates'][report_date] = copy.deepcopy(stage_history['dates'][list(stage_history['dates'])[-1]])
            # add first date
            else: 
                stage_history['dates'][report_date] = {}

        # add counts from current report to current date entry
        for stage in master_stages:
            # if the master stage does not exist in the current date add it
            if stage.title not in stage_history['dates'][report_date]:
                stage_history['dates'][report_date][stage.title] = 0 
            # if the master stage is the stage of the current report, increase its count in the current date
            if stage.title == report.stage.title:
                stage_history['dates'][report_date][stage.title] += 1
        
        # subtract previous stage counts for pre-existing companies
        prev_report = get_previous_company_report(report)
        if prev_report:
            stage_history['dates'][report_date][prev_report.stage.title] -= 1

    return JsonResponse(stage_history)


def get_current_stage(company):
    try:
        current_stage = CompanyStageReport.objects.filter(company=company).latest('date_updated')
    except ObjectDoesNotExist:
        current_stage = "No Report"
    return current_stage

def stage_summary(request):
    master_stages = MasterStage.objects.all().order_by('value')
    companies = Company.objects.all()
    
    # list of latest stages
    latest_stages = []
    for c in companies:
        latest_stages.append(get_current_stage(c))

    # generate empty stage counts dict
    stage_counts = {}
    for m in master_stages:
        stage_counts[m.title] = {
            'y' : 0
        }

    # add current stage counts
    for s in latest_stages:
        stage_counts[s.stage.title]['y'] += 1

    return JsonResponse(stage_counts)

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

    # print(list(map(lambda row: {'year': all_yearly_stages[row], 'y': all_yearly_stages[row]}, all_yearly_stages)))

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
