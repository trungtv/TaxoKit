from spacy.tokens import DocBin
import spacy
import glob
import os

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

    def populate_terms(self, term_extractor):
        for i in range(len(self.docs)):
            self.docs[i] = term_extractor.populate_terms(self.docs[i])