def calculate(link,players1,players2):
	import requests
	from bs4 import BeautifulSoup
	def comparetwo(a, b):
		return [c for c in a if c.isalpha()] == [c for c in b if c.isalpha()]
	def totalruns(cmp,playing,r):
		total_runs=0
		for compare in cmp:
			for name,runs in playing:
				if(comparetwo(compare,name)):
					if(r==0):
						total_runs+=int(runs)
					else:
						total_runs+=20*int(runs)
		return total_runs
	st=link.split('/')
	srch='https://www.cricbuzz.com/live-cricket-scorecard/' + st[-2] + '/' + st[-1]
	print(srch)
	page=requests.get(srch)
	soup=BeautifulSoup(page.content,'lxml')
	a=soup.find_all('div',class_="cb-col cb-col-100 cb-scrd-itms")
	batsman=[]
	batsman_runs=[]
	bowler=[]
	bowler_wickets=[]
	for child in a:
		if (len(child)==15):
				try:
					b=child.a
					c=child.find('div',class_="cb-col cb-col-8 text-right text-bold")
					batsman.append(b.get_text())
					batsman_runs.append(c.get_text())
				except  AttributeError:
					pass
		elif(len(child)==17):
				try:
					d=child.a
					e=child.find('div',class_="cb-col cb-col-8 text-right text-bold")
					bowler.append(d.get_text())
					bowler_wickets.append(e.get_text())
				except AttributeError:
					pass
		


	batsman_runs_final=list(zip(batsman,batsman_runs))
	bowler_wickets_final=list(zip(bowler,bowler_wickets))
	print(batsman_runs_final,bowler_wickets_final)
	cmp1=players1
	cmp2=players2
	compare_names1=[]
	compare_names2=[]
	for compare1,compare2 in zip(cmp1,cmp2):
		compare_names1.append(compare1)
		compare_names2.append(compare2)
	print(compare_names1,compare_names2)
	t1=totalruns(compare_names1,batsman_runs_final,0)
	w1=totalruns(compare_names1,bowler_wickets_final,1)
	t2=totalruns(compare_names2,batsman_runs_final,0)
	w2=totalruns(compare_names2,bowler_wickets_final,1)
	print(t1,w1)
	print(t2,w2)
	calc=(t1+w1)-(t2+w2)
	return calc