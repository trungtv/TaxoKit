class BaseTerm:
    def __init__(self, uri, boarder_uris, narrower_uris, \
        preferred_term, alternative_terms, hidden_terms, description): #, **kwargs):
        """
        uri: uri or id of the term
        boarder_uris: list of boarder terms' uri
        narrower_uris: list of narrower terms' uri
        preferred_term: the popular title of the term
        alternative_terms: list of alternative titles of the term
        hidden_terms: list of less popular titles of the term
        description: description of the term
        """
        self.uri = uri
        self.boarder_uris = boarder_uris
        self.narrower_uris = narrower_uris
        self.preferred_term = preferred_term
        self.alternative_terms = alternative_terms
        self.hidden_terms = hidden_terms
        self.description = description
