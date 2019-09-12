import requests
from bs4 import BeautifulSoup
def link(inp):
	import requests
	from bs4 import BeautifulSoup
	page=requests.get("https://www.cricbuzz.com/cricket-series/2697/icc-cricket-world-cup-2019/matches")
	soup=BeautifulSoup(page.content,'html.parser')
	# print(soup.prettify())
	f=[]
	d=[]
	e=[]
	a=soup.find_all('a',class_="text-hvr-underline")
	# print(a)
	for ch in range(0,len(a)-2):
		sp=a[ch].get_text().split(',')
		f.append(sp[0])
	date=soup.find_all('div',class_="cb-col-25 cb-col pad10 schedule-date ng-isolate-scope")

	for child in range(0,len(a)-2):
		b=a[child].get('href')
		
		try:
			c=b.split('/')
			d.append(c[2])
			e.append(c[3])
			
		except AttributeError:
			pass
	# print(d,e)
	final_hr=[]
	final_hr1=[]
	hr='https://www.cricbuzz.com/cricket-match-facts/'
	hr1='https://www.cricbuzz.com/live-cricket-scorecard/'
	for a1,a2 in zip(d,e):
		final_hr.append(hr+a1+'/'+a2)
		final_hr1.append(hr1+a1+'/'+a2)
	# for i in range(0,len(f)):
	# 	print(i+1,f[i])
	sendhr=final_hr[inp-1]
	sendhr1=final_hr1[inp-1]
	final=[sendhr,sendhr1]
	return final
# a=link(1)
# print(a[1])
	# print(sendhr1)
	# print(final_hr[0])
