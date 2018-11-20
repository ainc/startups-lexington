from django.db import models
from django.utils import timezone
from datetime import datetime
import Levenshtein

# change true/false to yes/no for forms
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class Company(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateField('date created', auto_now_add=True)
    # stage = models.ForeignKey('Stage', on_delete=models.CASCADE, blank=True, null=True)
    website = models.URLField(blank=True)
    email_address = models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

class CommonStage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    funding = models.IntegerField('Funding', default=0, blank=True, null=True)
    product_stage = models.ForeignKey('ProductStage', on_delete=models.CASCADE, blank=True, null=True)
    has_customers = models.BooleanField(choices=BOOL_CHOICES, blank=True, null=True)
    revenue = models.IntegerField('Revenue', default=0, blank=True, null=True)
    fulltime_employees = models.IntegerField('Fulltime Employees', default=0, blank=True, null=True)

    class Meta:
        abstract = True

class MasterStage(CommonStage):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        if len(self.title.split()) > 1:
            return self.title.split()[1]
        return self.title

    def get_stage_number(self):
        if len(self.title.split()) > 1:
            return (int(self.title.split()[1]))
        return 0

class CompanyStageReport(CommonStage):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='company_stage_report')
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE, blank=True, null=True)
    date_updated = models.DateTimeField('Date updated', default=datetime.now)
    stage = models.ForeignKey('MasterStage', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.stage = self.calcStage()
        return super(CompanyStageReport, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.company.name)

    """
    Calculate the stage of a company based on MasterStage table values.
    1. Store all master stages in 2d list (funding, product_stage, has_customers, revenue, ft employees)
    2. Place current stage entry in list (same order as above)
    3. Iterate through and compare values, add 1 for each matching pair. Or add 1 if value is greater for that stage
    """
    def calcStage(self):
        stages = MasterStage.objects.all().order_by("title")
        comp_stage = 0

        # Create matrix list that pulls from MasterStage models
        master_stage_matrix = []
        for s in stages:
            iter_stage = [
                s.funding,
                s.product_stage.title,
                s.has_customers,
                s.revenue,
                s.fulltime_employees
            ]
            master_stage_matrix.append(iter_stage)

        curr_stage_list = [
            self.funding,
            self.product_stage.title,
            self.has_customers,
            self.revenue,
            self.fulltime_employees
        ]

        # Implement similarity model below
        weight_list = []
        for row in range(len(master_stage_matrix)):
            weight_list.append(0)
            for i in range(len(master_stage_matrix[row])):
                # bools check
                if isinstance(master_stage_matrix[row][i], bool):
                    if master_stage_matrix[row][i] == curr_stage_list[i]:
                        weight_list[row] += 1
                # check if value is a str
                elif isinstance(master_stage_matrix[row][i], str):
                    if master_stage_matrix[row][i] == curr_stage_list[i]:
                        weight_list[row] += 1
                # value is a number
                else:
                    if master_stage_matrix[row][i] <= curr_stage_list[i]:
                        weight_list[row] += 1

        print(weight_list)
        max_match = max(weight_list)
        print(max_match)
        stage_match = [l for l, j in enumerate(weight_list) if j == max_match]
        print(stage_match)
        # Get the smaller match of the two
        best_match = min(stage_match)
        print(best_match)

        return MasterStage.objects.get(title=stages[best_match].title)
        
class Founder(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    linked_in = models.URLField(blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name

class Investor(models.Model):
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class ProductStage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class CompanyComment(models.Model):
    content = models.TextField()
    date_added = models.DateTimeField('date', auto_now_add=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)