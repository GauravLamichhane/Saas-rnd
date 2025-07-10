from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisit
def home_view(request, *args, **kwargs):
  return about_view(request, *args, **kwargs)

def about_view(request, *args, **kwargs):
  qs = PageVisit.objects.all()
  page_qs = PageVisit.objects.filter(path = request.path)
  try:
    percent = (page_qs.count() * 100.0) / qs.count()
  except:
    percent = 0
  title = "My Page"
  context = {
    'page_title':title,
    'page_visit_count':page_qs.count(),
    'total_visit_count':qs.count(),
    'percent':percent  }

  path = request.path
  print("path", path)
  PageVisit.objects.create(path=request.path)
  return render(request,'home.html',context)


#1:11:18