
#!/usr/bin/python
# -*- coding: utf-8 -*-
# *** Just learning python ***
# sample by www.brunoneves.com 01/28/2016
# feel free for modify and improve the code
# Simple sample news for blind using speech recognition.
# Just run the script and using your voice for listen at the google news top 10's that do you want to listen.
# This sample work on OSX. For others systems you'll need to use pyttsx. https://pypi.python.org/pypi/pyttsx
# For other languages just change:
# QUERY -> 'hl' : "pt-br"

import htmllib, urllib2 ,re, urllib, os, time, simplejson, unicodedata, sys, pyprind, subprocess


google_api = 'https://ajax.googleapis.com/ajax/services/search/news?'


QUERY = { 
		'v' : '1.0', 
		'rsz' : "1", 
		'hl' : "pt-br", 
		'q' : '',
		'start' : '' 
}

MESSAGES = {
	'TITLE' : 'As top 10 noticias sobre: ',
	'START' : 'Saber mais sobre: ',
	'CONFIRMING_QUESTION' : 'Voce quer saber mais sobre: ',
	'REPEAT_QUESTION' : 'Repita sobre o que voce quer saber novamente.',
	'I_DONT_UNDERSTAND_YOUR_QUESTION' : 'Nao entendi, por favor repita sua pergunta novamente.',
	'SORRY_QUESTION_NOT_FOUND' : 'Desculpe, mas nao consegui encontrar nada. Por favor repita novamente.',
	'CONFIRM?' : 'Confirmar?'
}

INPUT_MESSAGES = {
	'CONFIRM' : ['yes','sim','confirmar','confirma']
}


TAG_RE = re.compile(r'<[^>]+>')


def init(_question):
	s = subprocess.call("say "+ _question, shell=True)
	if s == 0:
		start_recognizer()


def start_recognizer():
	
	QUERY['q'] = recognizer()

	print MESSAGES['START'] + QUERY['q'].upper()

	subprocess.call('say ' + MESSAGES['CONFIRMING_QUESTION'] + QUERY['q'] + '? ' + MESSAGES['CONFIRM?'] ,shell=True)

	confirm = recognizer()

	if confirm.lower() in ( INPUT_MESSAGES['CONFIRM'] ):
		call_news()
	else:
		init( MESSAGES['REPEAT_QUESTION'] )


def recognizer():
	import speech_recognition as sr
	# obtain audio from the microphone
	r = sr.Recognizer()
	r.dynamic_energy_threshold = True
	r.dynamic_energy_adjustment_damping = 0.15
	r.dynamic_energy_adjustment_ratio = 1.5

	with sr.Microphone() as source:  
		audio = r.listen(source)

	try:
		# recognize speech using Google Speech Recognition
		saw = r.recognize_google(audio, key = None, language = QUERY['hl'], show_all = False).encode("utf-8")
	except sr.UnknownValueError:
	    print("Google Speech Recognition could not understand audio")
	    init( MESSAGES['I_DONT_UNDERSTAND_YOUR_QUESTION'] )
	except sr.RequestError as e:
	    print("Could not request results from Google Speech Recognition service; {0}".format(e))
	    init( MESSAGES['SORRY_QUESTION_NOT_FOUND'] )
	else:
		return saw


def news( _page ):

	QUERY['start'] = _page

	try: 
		url = google_api + urllib.urlencode(QUERY) 
		response = urllib2.urlopen(url)
		data = simplejson.load(response)
		content = data['responseData']['results'][0]['content']
		title = remove_tags( unescape(content).encode("utf-8") )

	except urllib2.HTTPError as e: 
		print e.code
		init( MESSAGES['REPEAT_QUESTION'] )
	
	except urllib2.URLError as e: 
		print e.reason
		init( MESSAGES['SORRY_QUESTION_NOT_FOUND'] )
	
	finally:
		print title
		command = "say " + title
		subprocess.call(command ,shell=True)


def call_news():
	for i in range(0, 10):
		news(i)
		time.sleep(3)


def remove_tags(_text):
    return TAG_RE.sub('', _text)


def unescape(s):
    s = s.replace("&quot;", "")
    s = s.replace("&#39;", "")
    s = s.replace("&nbsp;", "")
    s = s.replace("(", "dia")
    s = s.replace(")", ",")

    return s


init( MESSAGES['TITLE'] )

 




