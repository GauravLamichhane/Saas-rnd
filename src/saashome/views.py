from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisit
def home_page_view(request, *args, **kwargs):
  qs = PageVisit.objects.all()
  page_qs = PageVisit.objects.filter(path = request.path)
  title = "My Page"
  context = {
    'page_title':title,
    'page_visit_count':page_qs.count(),
    'total_visit_count':qs.count(),
  }

  path = request.path
  print("path", path)
  PageVisit.objects.create(path=request.path)#This line creates a new row in the DB like path = '/contact/' timestamp = 2025-0-0

  return render(request,'home.html',context)

#1:11:18