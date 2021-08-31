from abc import ABCMeta, abstractmethod
from spacy.tokens import Span, Doc
from typing import List, Tuple

class ITermExtractor:
    __metaclass__ = ABCMeta

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'version') and 
                callable(subclass.version) and 
                hasattr(subclass, 'extract_offsets') and 
                callable(subclass.extract_offsets) and
               hasattr(subclass, 'extract_spans') and 
                callable(subclass.extract_spans))
    
    @classmethod
    def version(self): return '1.0'
    
    @abstractmethod
    def extract_offsets(self, doc: Doc) -> List[Tuple[int, int, str]]: raise NotImplementedError
    
    @abstractmethod
    def extract_spans(self, doc: Doc, offsets: List[Tuple[int, int, str]]) -> List[Span]: raise NotImplementedError

    @abstractmethod
    def populate_terms(self, doc:Doc) -> Doc: raise NotImplementedError 

class BaseTermExtractor(ITermExtractor):
    
    def extract_offsets(self, doc):
        raise NotImplementedError
        
    def extract_spans(self, doc):
        offsets = self.extract_offsets(doc)
        spans = []
        for offset in offsets:
            spans.append(Span(doc, offset[0], offset[1], offset[2]))
        return spans
    
    def populate_terms(self, doc):
        spans = self.extract_spans(doc)
        doc.ents = spans
        return doc
