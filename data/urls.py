from django.urls import path

from . import views
from data.views import CompanyList, CompanyDetail

urlpatterns = [
    path('', CompanyList.as_view(), name='companies'),
    path('growth', CompanyList.as_view(), name='companies'),
    path('<int:pk>/', CompanyDetail.as_view(), name='company-detail'),
    path('json/stage_summary/', views.stage_summary, name='stage_summary'),
    path('json/yearly_progress/', views.yearly_progress, name='yearly_progress'),
]