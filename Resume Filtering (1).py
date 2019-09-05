import re,nltk,docx2txt,csv,os,datetime
# import textract - textract library works only for Linux (ubuntu)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

############################################################################

def extract_phone_numbers(string):
    #r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    mobile = ""
    match_mobile = re.search(r'((?:\(?\+91\)?)?\d{10})',string)
    #phone_numbers = r.findall(string)
    #return [re.sub(r'\D', '', number) for number in phone_numbers]
    if(match_mobile != None):
        mobile = match_mobile.group(0)
    return mobile

###################################################################################
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)


#################################################################################

def extract_names(document):
    nouns = [] #empty to array to hold all nouns
    
    stop = stopwords.words('english')
    stop.append("Resume")
    stop.append("RESUME")
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    for sentence in sentences:
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
            if (pos == 'NNP' and len(word)>2):
                nouns.append(word)
    nouns=' '.join(map(str,nouns))
    nouns=nouns.split()                
    return nouns            

##############################################################################
    ##encode("utf-8", "replace")

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

###########################################################

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

############################################################
"""

a=[]    
for q in skill_set:
    fullText.find(q)
    a.append(q)
"""
#####################################################

def get_convert_to_text(filename):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
     
    if filename.endswith(".docx"):
        fullText = docx2txt.process(filename)
    elif filename.endswith(".pdf"):
        fullText=str(textract.process(filename))
        fullText = fullText.replace("\\n"," ")
    else:
        print ("File format is currently not supported")
        exit(0)
        
    details=[];ab=[];a=[]
    name_coll = extract_names(fullText)
    #print(name_coll)
    fullText=fullText.replace('b"',"")
    stop = stopwords.words('english')
    stop.append("Resume")
    stop.append("RESUME")
    abc=fullText.split()
    
    
    b=extract_phone_numbers(fullText)
    c=set(extract_email_addresses(fullText))
    e=modification_date(filename)
    
    mi=filename.lower()
    #print(mi)
    h=mi.replace("_"," ")
    h=h.replace("-"," ")
    h=h.replace(","," ")
    h=h.replace(".docx"," ")
    h=h.replace(".pdf"," ")
    h=h.split()
    if 'years' in h and 'months' in h:
        d=h[h.index('years')-1] + " " + h[h.index('years')]+ " " +h[h.index('months')-1] + " " +h[h.index('months')]
    elif 'years' in h:
        d=h[h.index('years')-1] + " " + h[h.index('years')]
    elif 'months' in h:
        d=h[h.index('months')-1] + " " + h[h.index('months')]
    elif re.search('no experience',str(h),re.M|re.I) :
        d='No Experience'
    else:
        d=generate_ngrams(fullText, 2)  
        
       
    
    
    
    for i in name_coll :
        if re.search(i, str(c),re.M|re.I) or re.search(i,filename,re.M|re.I) :
            ab.append(i)
            if len(ab)==1:
                break
    
    with open("/home/palak/Documents/Filter Profile/Resumes/all_linked_skills.txt","r") as skill:
        skill_set = skill.read().split("\n")    


    f=[]
    for s in skill_set:
        if s in fullText:
            if len(s)>2:
                f.append(s)
                
    
    #a='palak'
    a=abc[abc.index(ab[0])] + " " + abc[abc.index(ab[0])+1]
    c=" ".join(str(x) for x in c)
    details={'Name':a,'Mob no':b,'Email':c,'Resume':filename,'Number of exp' : d,'Last Modified' : e,'Skills Set' : f}
    return (details)

####################################################################  





###MAIN Program #################################

if __name__ == '__main__':
    output=[]
    #files_list=[]
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".docx"):
                output.append(get_convert_to_text(file))
            if file.endswith(".pdf"):
                output.append(get_convert_to_text(file))
with open('names.csv', 'w') as csvfile:
    fieldnames = ['Name', 'Mob no','Email','Resume','Number of exp', 'Last Modified','Skills Set']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(output)):
        writer.writerow(output[i])
print()
print("########Resume Filter############")
print("Please check the CSV file , Data loaded into it ")