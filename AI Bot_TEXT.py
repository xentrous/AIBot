import re
import os
import sys
import pyttsx
import requests
import mechanize
import speech_recognition
from time import sleep
from chatterbot import ChatBot

net_detect=0 # It sets to 1 if active network connection is found
exit_condition=0

try:

    engine=pyttsx.init()
    #engine.setProperty('rate', 180)# words per minute
    engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    
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
    
    def anonmail(name,ques):
        net_detect=0
        br.open("http://anonymouse.org/anonemail.html")
        net_detect=1
        br.select_form(nr=0)
        br.form['to']='xentrous@gmail.com' # Enter Your EMail-Id Here
        br.form['subject']='AI Bot Upgradation Required'
        br.form['text']=str(name+" found the following query unresolved:-\n"+ques)
        br.submit()

    def whois():
        
        net_detect=0
        response=br.open("https://www.google.co.in")
        net_detect=1

        br.select_form(nr=0)   
        br.form['q']=ques
        br.submit()
        src_code=br.response().read()
        
        answer=re.search(r'<span>(.*)',src_code)
        answer=answer.group()[:400]
        if 'wiki' in answer:
            answer=re.search(r'<span>(.*)<a',answer).group(1)
        else:
            answer=re.search(r'<span>(.*)</span></div></div><div',answer).group(1)
        engine.say(answer)
        print answer
    
    def whatis():

        net_detect=0
        response=br.open("https://www.google.co.in")
        net_detect=1

        br.select_form(nr=0)   
        br.form['q']=ques
        br.submit()
        src_code=br.response().read()
        
        spg=1
        answer=re.search(r'"_sPg">(.*)',src_code)
        if answer==None:
            answer=re.search(r'<ol><li>(.*)',src_code)
            spg=0
        if answer==None:
            whois()
            return
        answer=answer.group()[:400]
        if '<b>' in answer:
            answer=answer.replace("<b>","")
            answer=answer.replace("</b>","")
        if spg:
            answer=re.search(r'"_sPg">(.*)</div></div><div',answer).group(1)
        else:
            answer=re.search(r'<ol><li>(.*)</li>',answer).group(1)
        engine.say(answer)
        print answer

    def trained():
        
        answer=AI_Bot.get_response(ques)
        engine.say(answer)
        print answer

    print "Enter your Name:- "
    engine.say("Enter your Name")
    engine.runAndWait()
    name=raw_input()
    print "Hello",name
    engine.say("Hello"+name)

    ques='a'
    ques_no=0

    print "How can I assist you?"
    engine.say("How can I assist you?")
    engine.runAndWait()

    while True:
        ques=raw_input().strip()#keyboard input
        '''
        microphone=speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            audio=microphone.listen(source)
            ques=microphone.recognize_google(audio)
            print ques
        '''

        ques=ques.lower()
        
        if ques=='bye':
            print "Hoping that you enjoyed having this conversation."
            print "Thank You."
            exit_condition=1
            engine.say("Hoping that you enjoyed having this conversation")
            engine.say("Thank You")
            engine.runAndWait()
            sys.exit(1)
            
        ques_no+=1

        if 'who' in ques:
            if 'you' in ques:
                trained()
            else:
                whois()
        elif 'what' in ques:
            if 'name' in ques:
                trained()
            else:
                whatis()
        else:
            trained()

        engine.runAndWait()

except:
    if exit_condition==1:
        pass
    
    elif net_detect==0:
        print "Internet and I aren't talking right now."
        print "Try after Sometime. Thank You"
        engine.say("Internet and I aren't talking right now.")
        engine.say("Try After Sometime. Thank You")
        engine.runAndWait()
        sleep(1)
        
    else:
        trained()
        #anonmail(name,ques)#Anonymous mail takes atmost 12 hours to reach.
