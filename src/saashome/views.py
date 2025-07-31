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

VALID_CODE = 'abc123'
def pw_protected_page(request, *args, **kwargs):
  is_allowed = request.session.get('protected_page_allowed') or 0
  print(request.session.get('protected_page_allowed'), type(request.session.get('protected_page_allowed')))
  if request.method == "POST":
    user_pw_sent = request.POST.get("code") or None
    if user_pw_sent == VALID_CODE:
      is_allowed = 1
      request.session['protected_page_allowed'] = is_allowed
  if is_allowed:
    return render(request, "protected/view.html",{})
  return render(request, "protected/entry.html",{})