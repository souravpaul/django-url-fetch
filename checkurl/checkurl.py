import requests
import threading
from requests.exceptions import ConnectionError
from django.db import models
from .models import CheckURL

class urlFetch(threading.Thread):
	def __init__(self,url,key):
		threading.Thread.__init__(self)
		self.url=url
		self.key=key
	
	def run(self):
		self.fetchURL()

	#Fetching content with url and return response
	def getURLResponse(self,url):
		response=requests.get(url)
		response.encoding='ISO-8859-1'
		return response

	#Save URL to DB
	def save(self,url,code,reason):
		print "url> ",url," -",code, " - ",reason
		url = CheckURL(key=self.key,url=self.url,status_code=code,comment=reason)
		url.save()
		
	
	#Controlling the fetching operation
	def fetchURL(self):
		global success
		url=self.url
		url=url.strip()
		try:
			response=self.getURLResponse(url)
			self.save(url,response.status_code,response.reason)
		except ConnectionError as e:
			self.save(url,-1,"Connection Error")
		except Exception as e:
			self.save(url,-2,("Error "+str(e)))

