import os
import openai
from bibtexparser.bparser import BibTexParser

class RefParser:
    
    def __init__(self):
        super(RefParser, self).__init__()
        self.question=None
        self.completion=openai.Completion(api_key=os.environ['OPEN_AI_API'])
        self.template='create a bibtex entry for each reference in "{}"'

    def get_list(self, question):
        r=self.get_answer(question)
        if r:
            p=BibTexParser()
            d=p.parse(r)
            return d.entries

    def get_answer(self, question):
        try:
            r=self.completion.create(
                prompt=self.template.format(question),
                model='text-davinci-003',
                top_p=0.1,
                max_tokens=3000)
            return r['choices'][0]['text']
        except:
            return 'Could not fetch an answer from OPENAI'

