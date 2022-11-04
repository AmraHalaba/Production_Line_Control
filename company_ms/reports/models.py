from django.utils import timezone
from django.db import models
import random
from django.urls import reverse
from django.db.models import Sum
from datetime import datetime

from products.models import *
from production_lines.models import *
from categories.models import *


##############
# Report Model Manager
class ReportManager(models.Manager):
  
  def get_queryset(self):
    return ReportQueryset(self.model, using=self._db)
  
  def get_by_line_and_day(self, day, line_id):
    #return Report.objects.filter(day=day)      
    return self.get_queryset().get_by_line_and_day(day, line_id)
  
  def aggregate_execution(self):
    return self.get_queryset().aggregate_execution()
  
  def aggregate_plan(self):
    return self.get_queryset().aggregate_plan()
  
 


##############
# Report Model Manager - For getting custom querysets
class ReportQueryset(models.QuerySet):
      
  def get_by_line_and_day(self, day, line_id):     
    return self.filter(day=day, production_line__id=line_id)
  
  def aggregate_execution(self):
    return self.aggregate(Sum('execution'))
  
  def aggregate_plan(self):
    return self.aggregate(Sum('plan'))


##############
# Report Model

hours = (
          [ (str(x), str(x)) for x in range(1, 25) ]
        )

class Report(models.Model):
    #Basic Fields
    day             = models.DateField(default=timezone.now)
    start_hour      = models.CharField(max_length=2, choices=hours)
    end_hour        = models.CharField(max_length=2, choices=hours)
    plan            = models.PositiveIntegerField()
    execution       = models.PositiveIntegerField()
    
    #Related fields
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE,     null=True)
    
    #Utility fields
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    
    objects         = ReportManager()
    
    def __str__(self):
      return "{}-{}-{}".format(self.start_hour, self.end_hour, self.production_line)
    
    def get_day(self):
      return self.day.strftime('%Y/%m/%d')
    
    def get_absolute_url(self):
      return reverse("reports:update-view", kwargs={ 'production_line':self.production_line , 'pk':self.pk })
    
    class Meta:
      ordering = ('-day',)
    

##############
# Report Problem Model

#Code for generating automatic problem_id field
elements_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
     'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def random_id():
  random.shuffle(elements_list)
  code = [str(x) for x in elements_list[:12]]
  str_code = ''.join(code)

  return str_code


#Model Manager for ProblemReported
class ProblemReportedManager(models.Manager):
    
  def get_problems_by_day_and_line(self, day, line):
    return super().get_queryset().filter(report__day=day, report__production_line__name=line)

  def problems_from_today(self):
    now = datetime.now().strftime('%Y-%m-%d')
    return super().get_queryset().filter(report__day=now)    


class ProblemReported(models.Model):
  #Basic fields
  problem_id  = models.CharField(max_length=12, unique=True, blank=True, default=random_id)
  description = models.TextField()
  breakdown   = models.PositiveIntegerField()
  public      = models.BooleanField(default=False)
  
  
  #Related fields
  category    = models.ForeignKey(Category, on_delete=models.CASCADE)
  user        = models.ForeignKey(User, on_delete=models.CASCADE)
  report      = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
  
  #Utility fields
  created   = models.DateTimeField(auto_now_add=True)
  updated   = models.DateTimeField(auto_now=True)
  
  objects   = ProblemReportedManager()
  
  class Meta:
    verbose_name = 'problem reported'
    verbose_name_plural = 'problems reported'
        
  def __str__(self):
    return "{}-{}".format(self.category.name, self.description[:20])