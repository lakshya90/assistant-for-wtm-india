
import json
import os
import pandas as pd
import numpy as np
from flask import Flask,render_template
from flask import request,jsonify
from flask import make_response,Response

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/wtm',methods=['POST'])
def leads():
	input = request.get_json()
	result = input.get('result')
	action = result.get('action')
	
	parameters = result.get('parameters')
	chapters = parameters.get('Chapters')
	
	print 'Action is:'
	print action

	#print("Request:")
    	#print(json.dumps(input, indent=4))
	
	if action == 'wtm.india.chapters':
		print 'Chapters'
		res = makeResponse_chapters(chapters.encode('utf-8'))
	elif action == 'wtm.india.leads':
		print 'Leads'
		res = makeResponse_leads(chapters)
	elif action == 'WTMIndiaChapters.WTMIndiaChapters-yes':
		print 'Chapters Followup'
		context = result.get('contexts')
		param = [d['parameters'] for d in context if d['name'] == 'wtmindiachapters-followup'][0]
		chapter_prev = param.get('Chapters.original')
		chapter_curr = param.get('Chapters')	
		res = makeResponse_chapters_yes(chapter_prev,chapter_curr)
	
	elif action == 'WTMIndiaChapters.WTMIndiaChapters-yes.WTMIndiaChapters-yes-no':
		speech = 'Have a wonderful day!'
        	res = {
        	"speech": speech,
        	"displayText": speech,
}
	elif action == 'WomenTechmakersLead.WomenTechmakersLead-yes':
		print 'Leads Followup'
                context = result.get('contexts')
                param = [d['parameters'] for d in context if d['name'] == 'womentechmakerslead-followup'][0]
		chapter = param.get('Chapters')	
		res = makeResponse_leads_followup(chapter)			
	#print("Response:")
        #print(json.dumps(res, indent=4))
	return jsonify(res)




def makeResponse_leads(data):
	lead_directory = pd.read_csv('WTM_Leads.csv')
        lead_directory['Full Name'] = lead_directory['WTM Lead First Name']+' ' +lead_directory['WTM Lead Last Name']
	if data in lead_directory['GDG Chapter Name'].tolist():
                result = lead_directory[lead_directory['GDG Chapter Name']== data]['Full Name']
        
	speech = 'The WTM Lead for ' +data+ ' is '+result.item();
	speech+='. Do you want her contact details too?'
	return {
        "speech": speech,
        "displayText": speech,
}

def makeResponse_leads_followup(data):
	lead_directory = pd.read_csv('WTM_Leads.csv')
        if data in lead_directory['GDG Chapter Name'].tolist():
                result = lead_directory[lead_directory['GDG Chapter Name']== data]['Email ID']

	speech = 'The email ID of the WTM lead for ' +data+ ' is '+result.item();
        speech+='. Is there anything else I can help you with?'
        return {
        "speech": speech,
        "displayText": speech,
}
def makeResponse_chapters(chapter_count):
	if chapter_count == 'chapters':
		lead_directory = pd.read_csv('WTM_Leads.csv')
		result = lead_directory['GDG Chapter Name']
        	no_of_chapters = len(result)
		speech = 'Currently there are '+str(no_of_chapters)+ ' active Women Techmakers chapters in India. Do you wish to know which are those '+str(no_of_chapters)+ ' chapters?';

		print speech
		return {
        	"speech": speech,
       		"displayText": speech,
} 		

def makeResponse_chapters_yes(chapter_prev, chapter_curr):
	if chapter_prev == chapter_curr:
		lead_directory = pd.read_csv('WTM_Leads.csv')
                result = lead_directory['GDG Chapter Name']
		chapters = []
		for i in range(0,len(result)):
			chapters.append(result[i])	
		speech = 'The list of chapters in India are : '
		for i in range(0,len(chapters)):
			speech+=chapters.pop()
			speech+=', '
                speech+= '. Is there anything else that I can help you with?'
		print speech
                return {
                "speech": speech,
                "displayText": speech,
}
if __name__ == '__main__':
    app.run()


