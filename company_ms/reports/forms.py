from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from django import forms
from django.shortcuts import get_object_or_404

from production_lines.models import *
from .models import *


#Select Production Line on the Homepage Form      
class SelectLineForm(forms.Form):
    production_line = forms.ModelChoiceField(queryset=ProductionLine.objects.none(), label='')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # print(user)
        super(SelectLineForm, self).__init__(*args, **kwargs)
        self.fields['production_line'].queryset = ProductionLine.objects.filter(
            team_leader__user__username=user)


#Select Report
class ReportResultForm(forms.Form):
    production_line = forms.ModelChoiceField(queryset=ProductionLine.objects.all())
    day             = forms.CharField(widget=forms.DateTimeInput(attrs={ 'class':'datepicker' }))


#Report Form
class ReportForm(forms.ModelForm):
    
    class Meta:
        model  = Report
        #fields = '__all__'
        exclude = ( 'user', 'production_line', )
    
    def __init__(self, *args, **kwargs):
        production_line = kwargs.pop('production_line', None)
        super().__init__(*args, **kwargs)
        if production_line is not None:
            line = get_object_or_404(ProductionLine, name=production_line)
            #print("LINE NAME: ", line.name)
            self.fields['product'].queryset = line.products.all()
        
#Problems Reported Form
class ProblemReportedForm(forms.ModelForm):
    
    class Meta:
        model  = ProblemReported
        #fields = '__all__'
        exclude = ( 'user', 'report', 'problem_id',)
        

