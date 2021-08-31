from spacy.matcher import PhraseMatcher
from .base_term_extractor import BaseTermExtractor

class DictionaryTermExtractor(BaseTermExtractor):
    
    def __init__(self, nlp, term_list, term_label, case_sensitive=False):
        self.term_list = term_list
        self.term_label = term_label
        matcher_attr = "TEXT" if case_sensitive else "LOWER"
        self.matcher = PhraseMatcher(nlp.vocab, attr=matcher_attr)
        self.matcher.add(term_label, [nlp.make_doc(term) for term in term_list])
        self.case_sensitive = case_sensitive
            
    def extract_offsets(self, doc):
        offsets = []
        for _, start, end in self.matcher(doc):
            offsets.append((start, end, self.term_label))
        return offsets