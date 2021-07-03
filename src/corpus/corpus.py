from spacy.tokens import DocBin
import spacy
import glob
import os
from spacy.tokens import Doc
import jsonlines

class Corpus():
    def __init__(self, nlp, name = 'taxokit'):
        self.name = name
        self.docs = []
        self.nlp = nlp

    def from_folder(self, path, glob_pattern='/**/*.txt', encoding='utf-8'):
        self.path = path
        self.docs = []

        for file_path in glob.glob(path + glob_pattern, recursive=True):
            with open(file_path, 'r', encoding = encoding) as f:
                doc = self.nlp(("\n".join(f.readlines())))
                self.docs.append(doc)

    def to_disk(self, folder='./'):
        doc_bin = DocBin(docs = self.docs)
        doc_bin.to_disk(os.path.join(folder,self.name + '.spacy'))

    def from_disk(self, folder='./'):
        doc_bin = DocBin().from_disk(os.path.join(folder,self.name + '.spacy'))
        self.docs = list(doc_bin.get_docs(self.nlp.vocab))

    def to_json(self, docs, replace_to_space=True):
        """
        :doc (Doc): source doc
        Returns (list (dict)): deccano format json
        """
        if isinstance(docs, Doc):
            docs = [docs]
            
        djson = list()
        for doc in docs:
            for sent in doc.sents:
                labels = list()
                for e in sent.ents:
                    labels.append([e.start_char, e.end_char, e.label_])
                djson.append({'text': sent.text.replace('_', ' ') if replace_to_space else sent.text, "labels": labels})
        return djson

    def to_jsonl_file(self, docs, output_file, replace_to_space=True):
        json = self.to_doccano(docs, replace_to_space)
        with jsonlines.open(output_file, 'w') as writer:
            writer.write_all(json)

    def from_jsonl_file(self, input_file, replace_to_space=False):
        json = []
        with jsonlines.open(input_file) as reader:
            for line in reader:
                #if replace_to_space:
                #    line['text'] = line['text'].replace('_', ' ') 
                json.append(line)
        return self.from_json(json, replace_to_space)

    def from_json(self, djson, replace_to_space=False):
        docs = []
        for line in djson:
            doc = self.nlp(line['text'].replace('_', ' ') if replace_to_space else line['text'])
            spans = []
            for item in line['labels']:
                span = doc.char_span(item[0], item[1], alignment_mode='expand', label=item[2])
                spans.append(span)
            doc.ents = spans
            docs.append(doc)
        return docs

    def populate_terms(self, term_extractor):
        for i in range(len(self.docs)):
            self.docs[i] = term_extractor.populate_terms(self.docs[i])