import re
import csv
import mechanize
from chatterbot import ChatBot

br=mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False) # Ignore robots.txt
br.set_handle_refresh(False)
#Google demands a user-agent that isn't a robot
br.addheaders=[('User-agent','Firefox')]

AI_Bot = ChatBot("Scofield",
		  storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
		  io_adapters=[
			  "chatterbot.adapters.io.TerminalAdapter"
		  ],
		  database="scofield")

ques=""
    
def crawl(ques):
    try:
        
        br.open("https://www.google.co.in")
    
        br.select_form(nr=0)   
        br.form['q']=ques
        br.submit()
        src_code=br.response().read()
        
        answer=re.search(r'<span>(.*)',src_code)
        if answer:
            answer=answer.group()[:400]
            if 'wiki' in answer:
                answer=re.search(r'<span>(.*)<a',answer)
                if answer : return answer.group(1)
            else:
                answer=re.search(r'<span>(.*)</span></div></div><div',answer)
                if answer : return answer.group(1)
        spg=1
        answer=re.search(r'"_sPg">(.*)',src_code)
        if answer==None:
            answer=re.search(r'<ol><li>(.*)',src_code)
            spg=0
            
        if answer :
            answer=answer.group()[:400]
            if spg:
                answer=re.search(r'"_sPg">(.*)</div></div><div',answer)
                if answer : return answer.group(1)
            else:
                answer=re.search(r'<ol><li>(.*)</li>',answer)
                if answer : return answer.group(1)
                    
        return AI_Bot.get_response(ques)

    except:
        return AI_Bot.get_response(ques)

fp=open('log.csv', 'w')
a = csv.writer(fp, delimiter=',')

data=[['Query','Response']]

print 'AI Bot Initiated\n'

while(1):
    ques=raw_input()
    if ques in ['bye','bbye']:
        break
    ans=str(crawl(ques))
    ans=ans.replace("<b>","")
    ans=ans.replace("</b>","")
    ans=ans.replace("&quot;","")
    ans=ans.replace("&#39;","")
    print ans
    data.append([ques,ans])

a.writerows(data)
