def playing(inp):
	from criclink import link
	import requests
	from bs4 import BeautifulSoup
	st=inp.split('/')
	srch='https://www.cricbuzz.com/cricket-match-facts/' + st[-2] + '/' + st[-1]
	print(srch)
	headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
			 'referer': 'https://pb-calc.herokuapp.com/player/team',
	}
	proxies={
		'http': 'http://217.182.120.166:8080',
		'https':'http://217.182.120.166:8080',
	}
	page=requests.get(srch,headers=headers,proxies=proxies)
	print(page)
	soup=BeautifulSoup(page.content,'lxml')
	a=soup.find_all('div',class_="cb-col cb-col-27 cb-mat-fct-itm text-bold",string="Playing XI:")
	print(a)
	# team=[]
	# for i in range(0,len(a)):
	# 	team.append(a[i].get_text())
	# print(team)
	b=a[0].next_sibling.next_sibling
	c=a[1].next_sibling.next_sibling
	team1playing=[]
	team2playing=[]
	for child1,child2 in zip(b.children,c.children):
		try:
			team1playing.append({'value':child1.get_text(),'data':child1.get_text(),})
			team1playing.append({'value':child2.get_text(),'data':child2.get_text(),})
		except AttributeError:
			pass
	return team1playing
