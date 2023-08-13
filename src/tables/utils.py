import os
import re
import hashlib
import pdftotext
import requests
import fake_useragent
from pypdf import PdfReader
from bs4 import BeautifulSoup
from summa import keywords as skey
from summa import summarizer as ssum

def keywords(text, *args, **kwargs):

    if text:
        keys=skey.keywords(text, split=True, deaccent=True, **kwargs)
        return ' '.join(keys)
    else:
        return ''

def summarize(text, *args, **kwargs):
    if text:
        summary=ssum.summarize(text, *args, split=True, **kwargs)
        return ' '.join(summary)
    else:
        return ''

def getHash(filePath):

    if os.path.isfile(filePath):
        file_hash = hashlib.md5()
        with open(filePath, 'rb') as f:
            chunk = f.read(4096)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(4096)
        dhash=file_hash.hexdigest()
        return dhash

def getPDFContent(path):
    try:
        with open(path, "rb") as f:
            pdf = pdftotext.PDF(f)
            content=' '.join([text for text in pdf])
            content=content.replace('\n', ' ') 
        return content
    except:
        return ''

def getPDFMetadata(path):

    data={}
    with open(path, 'rb') as f:
        pdf = PdfReader(f)
        info = pdf.metadata
        data['pages'] = len(pdf.pages)
    if info.author:
        data['author'] = str(info.author)
    if info.title:
        data['title'] = str(info.title)

    return data

def get_soup(url):
    ua=fake_useragent.UserAgent()
    header={'User-Agent': str(ua.random)}
    raw = requests.get(url, headers=header)
    if raw.status_code == 200:
        html=raw.content
        soup=BeautifulSoup(html, 'lxml')
        return soup

def getUrlTitleAndContent(path):

    try:
        soup=get_soup(path)
    except:
        return path, '', ''

    try:

        titles=[]
        for title in soup.find_all('title'):
            titles+=[title.get_text()]
        title=' | '.join(titles)
        title=re.sub('[\n\r]', ' ', title)
        title=re.sub('  *', ' ', title)
        title=title.strip(' ')

    except:
        
        title=path

    try:

        body=soup.find('body')
        body_alone=body.findChildren(recursive=False)
        for data in  body(['style', 'script']):
            data.decompose()
        body_alone=' '.join(body.stripped_strings)
        clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        body_clean=re.sub(clean, ' ', body_alone)
        body_clean=re.sub('[\n\r]', ' ', body_clean)
        content=re.sub('  *', ' ', body_clean)
        html=soup.contents[1]

    except:
        
        content, html = '', ''

    return title, content, html

def updateBibliography(data):
    raise
    dhash=data['hash']
    entries=[]
    for a in bib.values():
        entries+=self.ref_parser.get_list(a['text'])
    data['metadata']={}
    data['cite']={}
    for i, entry in enumerate(entries):
        entry['bibkey']=entry['ID'].lower()
        entry.pop('ID')
        data['metadata'][i]=entry
        data['cite'][i]={'citing_hash':dhash, 'cited_bibkey':entry['bibkey']}
