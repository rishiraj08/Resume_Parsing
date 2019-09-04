
import os
import re
import pandas as pd
import numpy as np
#import nltk
import spacy
from spacy.matcher import Matcher
#from nltk.corpus import stopwords
nlp=spacy.load('en_core_web_sm')
matcher=Matcher(nlp.vocab)
import PyPDF2
from pywintypes import com_error
import win32com.client as win32

def extract_names(document):
    nlp_text=nlp(document)
    pattern=[{'POS':'PROPN'},{'POS':'PROPN'}]
    matcher.add('NAME',None,pattern)
    matches=matcher(nlp_text)
    for match_id,start,end in matches:
        span=nlp_text[start:end]
        return span.text

def extract_email_addresses(text):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(text)

def extract_mobile_number(text):
    #mno = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,15}[0-9]', text)
    mno = re.findall(r'[\+\(]?[1-9][0-9 \-\(\)]{8,15}[0-9]', text)
    mono = []
    for i in range(len(mno)):
        digit = 0
        for j in mno[i]:
            if j.isnumeric():
                digit+=1
        if digit > 9 and digit < 15:
            mono.append(mno[i])         
    return mono


def extract_skill_set(text):
    with open("C:\\Users\\PritamDevadattaJena\\Desktop\\alisha\\skills.txt","r") as skill:
        skill_set = skill.read().split("\n")    
    f = []
    for s in skill_set:
        #if re.search(s, text, re.I):
        if s in text:
            if len(s)>2:
                f.append(s)
    
    return f


def generate_ngrams(filename, n):
    
    words = filename.split()
    output = []  
    for i in range(len(words)-n+1):
        output.append(words[i:i+n])
    f=[]            
    for i in output:
        if 'years' in i:
            f.append(output[output.index(i)])
            if len(f)==1:
                n=f[0][0]
                n=n + " " + "years"
                break
    
    if len(f)<1:
        n='Not specified'
    return n


def exper(fullText):
    mi=fullText.lower()
    #print(mi)
    h=mi.replace("_"," ")
    h=h.replace("-"," ")
    h=h.replace(","," ")
    h=h.replace("("," ")
    h=h.replace(")"," ")
    h=h.replace(".docx"," ")
    h=h.replace(".pdf"," ")
    h=h.split()              #look at h only years get it
    if 'years' in h and 'months' in h:
        d=h[h.index('years')-1] + " " + h[h.index('years')]+ " " +h[h.index('months')-1] + " " +h[h.index('months')]
    #elif 'year' in h:
        #d=h[h.index('year')-1] + " " + h[h.index('year')]
    elif 'years' in h:
        d=h[h.index('years')-1] + " " + h[h.index('years')]
    elif 'months' in h:
        d=h[h.index('months')-1] + " " + h[h.index('months')]
    #elif 'month' in h:
     #   d=h[h.index('month')-1] + " " + h[h.index('month')]
    elif re.search('no experience',str(h),re.M|re.I) :
        d='No Experience'
    else:
        d=generate_ngrams(fullText, 2)  
    return d    



def count_skills(doc):
    a = doc.lower()
    a = re.sub('[^A-Za-z0-9]+', ' ', a)
    a = a.split()
    return a.count('python'),a.count('excel'),a.count('vba')



#------------------------------------------------------------------------------#

path = "C:\\Users\\PritamDevadattaJena\\Desktop\\alisha\\resumes\\"

data = []

####IMPORTING DOC & DOCX FILES ONLY
word = win32.Dispatch("Word.Application")
word.Visible = 0
try:
    for filename in os.listdir(path):
        if filename.endswith(('.doc','.docx')):
            print(filename)
            DOC_FILEPATH = path + filename        
            doc = win32.GetObject(DOC_FILEPATH)
            res = doc.Range().Text           
        name=extract_names(res)
        email = extract_email_addresses(res)
        cno = extract_mobile_number(res)
        skills = extract_skill_set(res)
        exp= exper(res)
        python_count, excel_count,vba_count = count_skills(res)
        data.append({"FileName":filename, "FileContents":res, "Name":name, "Email Address":email,\
                 "Contact Number":cno, "Skills":skills, "Experience": exp, "python_count": python_count,\
                 "excel_count":excel_count,"vba_count":vba_count})        
        df = pd.DataFrame(data, columns = ["FileName","FileContents","Name","Email Address","Contact Number","Skills","Experience","python_count","excel_count","vba_count"])    
        df.to_csv("resumes_filter8.csv", index=False)
        #doc.Saved = False
        #doc.Save()
        #doc.Close()
    word.Quit()
except com_error:
    print('error')
    pass

####IMPORTING PDF ONLY
for filename in os.listdir(path):
    if filename.endswith('.pdf'):
        print(filename)
        pdfFileObj = open(path + filename ,'rb')     #'rb' for read binary mode
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        number_of_pages = pdfReader.getNumPages()
        ls=[]
        for page_number in range(number_of_pages):   # use xrange in Py2
            page = pdfReader.getPage(page_number)
            page_content = page.extractText()
            ls.append(page_content)
            res = ''.join(''.join(map(str, row)) for row in ls)    
        name=extract_names(res)
        email = extract_email_addresses(res)
        cno = extract_mobile_number(res)
        skills = extract_skill_set(res)
        exp= exper(res)
        python_count, excel_count,vba_count = count_skills(res)
        data.append({"FileName":filename, "FileContents":res, "Name":name, "Email Address":email,\
                 "Contact Number":cno, "Skills":skills, "Experience": exp, "python_count": python_count,\
                 "excel_count":excel_count,"vba_count":vba_count})
        
        df = pd.DataFrame(data, columns = ["FileName","FileContents","Name","Email Address","Contact Number","Skills","Experience","python_count","excel_count","vba_count"])    
        df.to_csv("resumes_filter8.csv", index=False)


###IMPORTING AND CREATING RANKING    
data = pd.read_csv("C:/Users/PritamDevadattaJena/Desktop/alisha/resumes_filter8.csv")    

data['occurance'] = np.add(np.where(data['python_count']>=1,1,0),
                np.where(data['excel_count']>=1,1,0),
                np.where(data['vba_count']>=1,1,0))

data['ranking_score'] = (data['occurance'] * 1) + (data['python_count'] * 3) + \
                        (data['vba_count'] * 2) +(data['occurance']*1)  
                        
data['rank'] = data['ranking_score'].rank(ascending=False)   
data.sort_values('rank', inplace=True)
data.to_csv("resumes_filter8.csv", index=False) 
