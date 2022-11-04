from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from production_lines.models import *
from .models import *
from .forms import *


#-----------------------------------------------------------------------------------------
#Home View
class HomeView(FormView):
    template_name = 'reports/home.html'
    form_class = SelectLineForm

    def get_form_kwargs(self):
        kwargs = super(HomeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, *args, **kwargs):
        prod_line = self.request.POST.get("prod_line")
        return redirect('reports:report-view', production_line=prod_line)


#-----------------------------------------------------------------------------------------
#Select Report View
class SelectView(LoginRequiredMixin, FormView):
    template_name = 'reports/select_report.html'
    form_class    = ReportResultForm
    success_url   = reverse_lazy('reports:summary-view')
    
    def form_valid(self, form):
        self.request.session['day'] = self.request.POST.get('day', None)
        self.request.session['production_line'] = self.request.POST.get('production_line', None)
        #print("OVO JE DAN IZ POSTA: ", self.request.session['day'])
        return super(SelectView, self).form_valid(form)


#-----------------------------------------------------------------------------------------
#Report Summary View
@login_required
def main_report_summary(request):
    try:
        day              = request.session.get('day', None)
        
        prod_id          = request.session.get('production_line', None)
        production_line  = ProductionLine.objects.get(id=prod_id)
        execution_qs     = Report.objects.get_by_line_and_day(day, prod_id).aggregate_execution()['execution__sum']
        plan_qs          = Report.objects.get_by_line_and_day(day, prod_id).aggregate_plan()['plan__sum']
        problems = ProblemReported.objects.get_problems_by_day_and_line(
            day, production_line)
    except:
        return redirect('reports:select-report')
    
    del request.session['day']
    del request.session['production_line']
    
    context = { 'execution_qs'    : execution_qs,
                'plan_qs'         : plan_qs,
                'problems'        : problems,
                'day'             : day,
                'production_line' : production_line }
    return render(request, 'reports/summary.html', context)
    


#-----------------------------------------------------------------------------------------
#Report View
@login_required
def report_view(request, production_line):
    #Querying data from reports model to show up in the table
    queryset = Report.objects.filter(production_line__name=production_line)
    
    form  = ReportForm(production_line=production_line)  
    pform = ProblemReportedForm()
    
    #Since I have two forms in one html template, I need to enable submitting only one form at a time (I get name="submitbtn1" and name="submitbtn2" from buttons for submitting forms from within templates)
    if "submitbtn1" in request.POST:
        #Form for Reporting Problems in Production
        r_id   = request.POST.get("report_id") #getting the variable from the modal (js variable in report.html template)
        if request.method == 'POST':
            pform = ProblemReportedForm(request.POST or None)
            if pform.is_valid():
                report        = Report.objects.get(id=r_id) #than I get the report from the database with that ID
                object        = pform.save(commit=False) #i assign the the form.save to an object variable, but I am not saving it yet, because firstly I need to pass in the two form fields that are supposed to be automatically filled in (user and report)
                object.user   = request.user
                object.report = report
                object.save() #now i can save
                #messages.success(request, "Problem successfully reported.")
                # pform  = ProblemReportedForm()
                # form = ReportForm()
                return redirect(request.META.get('HTTP_REFERER'))
            else:
            #     messages.error(request, 'Problem processing your request')
                print("ERRORS: ", pform.errors)
    elif "submitbtn2" in request.POST:
        #Form for Creating Reports
        if request.method == 'POST':
            form = ReportForm(request.POST or None, production_line=production_line)
            if form.is_valid():
                line                   = get_object_or_404(ProductionLine, name=production_line) 
                object                 = form.save(commit=False) #i assign the the form.save to an object variable, but I am not saving it yet, because firstly I need to pass in the two form fields that are supposed to be automatically filled in (user and production line)
                object.user            = request.user
                object.production_line = line
                object.save() #now i can save
                #messages.success(request, "Report successfully created.")
                # pform  = ProblemReportedForm()
                # form = ReportForm()
                return redirect(request.META.get('HTTP_REFERER'))
            else:
            #     messages.error(request, 'Problem processing your request')
                print("ERRORS: ", form.errors)
        
    context = { 'form'        : form,
                'pform'       : pform,
                'object_list' : queryset}
    return render(request, 'reports/report.html', context)


#-----------------------------------------------------------------------------------------
#Delete View
@login_required
def delete_view(request, *args, **kwargs):
    r_id = kwargs.get('pk')
    object = Report.objects.get(id=r_id)
    object.delete()
    return redirect(request.META.get('HTTP_REFERER'))


#-----------------------------------------------------------------------------------------
#Update View
class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model         = Report
    form_class    = ReportForm
    template_name = 'reports/update_report.html'
    
    def get_success_url(self):
        #return super().get_success_url()
        return self.request.path