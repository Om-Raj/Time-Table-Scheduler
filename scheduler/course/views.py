from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Course
from scheduler.organization.models import Organization
from .models import Room

# helper function to get course object
def get_course_object(self, queryset = None):
    if queryset is None:
        queryset = self.get_queryset()
    org_id = self.kwargs['org_id']
    course_id = self.kwargs['course_id']
    try:
        return queryset.get(organization__id=org_id, course_id=course_id)
    except:
        return Http404('Course not found')


# helper function to get success url
def get_course_success_url(self):
    return reverse('course_detail', kwargs={
        'org_id': self.object.organization.id,
        'course_id': self.object.course_id,
    })

class CourseListView(ListView):
    model = Course
    template_name = 'scheduler/course/list.html'

    def get_queryset(self):
        org_id = self.kwargs['org_id']
        return Course.objects.filter(organization__id=org_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = Organization.objects.get(id=self.kwargs['org_id'])
        return context
    
class CourseCreateView(CreateView):
    model = Course
    template_name = 'scheduler/course/create.html'
    fields = ('course_id', 'title', 'rooms')

    def get_organization(self):
        return get_object_or_404(Organization, id=self.kwargs['org_id'])
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        org = self.get_organization()
        form.fields['rooms'].queryset = Room.objects.filter(
            organization=org
        )
        return form

    def get_success_url(self):
        return get_course_success_url(self)

    def form_valid(self, form):
        org_id = self.kwargs['org_id']
        form.instance.organization = Organization.objects.get(id=org_id)
        return super().form_valid(form)
    

class CourseDetailView(DetailView):
    model = Course
    template_name = 'scheduler/course/detail.html'

    def get_object(self, queryset = None):
        return get_course_object(self, queryset=queryset)
    

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'scheduler/course/delete.html'

    def get_object(self, queryset = None):
        return get_course_object(self, queryset=queryset)

    def get_success_url(self):
        return reverse('course_list', kwargs={'org_id': self.kwargs['org_id']})
    

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'scheduler/course/update.html'
    fields = ('course_id', 'title', 'rooms')

    def get_organization(self):
        return get_object_or_404(Organization, id=self.kwargs['org_id'])
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        org = self.get_organization()
        form.fields['rooms'].queryset = Room.objects.filter(
            organization=org
        )
        return form

    def get_object(self, queryset = None):
        return get_course_object(self, queryset=queryset)

    def get_success_url(self):
        return get_course_success_url(self)