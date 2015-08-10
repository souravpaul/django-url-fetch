from django.shortcuts import render,render_to_response,RequestContext
from .forms import URLForm
from django import forms
import json 
from django.http import HttpResponse,HttpResponseRedirect
from  .checkurl import urlFetch
from .models import CheckURL
from datetime import datetime
from django.core import serializers
import hashlib,smtplib,thread

# Create your views here.
def report(request):
	key=request.GET['key'];
	urls=request.GET['urls']
	return render_to_response('report.html',locals(),context_instance=RequestContext(request))

def urlform(request):
	if request.method == 'POST': # If the form has been submitted...
		form = URLForm(request.POST,request.FILES) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			urls= form.cleaned_data['urls']
			if len(urls)>5:
				url_list=[s.strip() for s in urls.splitlines()]
			elif request.FILES:
				url_list=[s.strip() for s in request.FILES['file'].readlines()]
				email=form.cleaned_data['email']
			else:
				raise forms.ValidationError("Invalid form submission")
			
			key=get_client_ip(request)+str(datetime.now())
			key=hashlib.sha224(key).hexdigest()
			#Creating threads for url fetching operation and start
			if len(urls)>5:
				start_processing(url_list,key,None)
			else:
				thread.start_new_thread( start_processing, (url_list,key,email) )
				return HttpResponseRedirect('/emailreport') # Redirect after POST
			return HttpResponseRedirect('/report?key='+key+"&urls="+str(len(url_list))) # Redirect after POST
	else:
		form = URLForm() # An unbound form
	return render_to_response('urlform.html',locals(),context_instance=RequestContext(request))
 
def fetchreport(request):
	key=request.GET['key']
	response_data=serializers.serialize("json", CheckURL.objects.filter(key=key))
	return HttpResponse(response_data, content_type="application/json")


def emailreport(request):
	return render_to_response('emailreport.html',locals(),context_instance=RequestContext(request))
	
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def sendEmail(email,key):
	message="<table><th><td>SL No</td><td>URL</td><td>Status</td><td>Comment</td></th>"
	rows=CheckURL.objects.filter(key=key)
	for count in range(len(rows)):
		message=message+"<tr><td>"+str(count)+"</td><td>"+rows[count].url+"</td><td>"+str(rows[count].status_code)+"</td><td>"+rows[count].comment+"</td></tr>"
	message=message+"</table>"
	print message
	try:
		smtpObj=smtplib.SMTP("localhost")
		smtpObj.sendmail("sourav@localhost.com",email,message)
	except smtplib.SMTPException:
		print "Sending email failed."
	except Exception:
		print "Sending email failed."
		
def start_processing(url_list,key,email):
	for url in url_list:
		if len(url)<3:
			url_list.remove(url)
		else:
			thread=urlFetch(url,key)
			thread.start()
			if email:
				thread.join()
	if email:
		sendEmail(email,key)