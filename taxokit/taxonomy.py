import networkx as nx
from networkx.exception import NetworkXError

from taxokit.db_connector.neo4j_connector import *
from taxokit.terms.base_term import BaseTerm

class Taxonomy:
    def __init__(self):
        self.taxonomy_graph = nx.DiGraph()
        self.neo4j_connector = Neo4jConnector()

    def build_or_update(self, terms):
        nodes = [(term.uri, term.__dict__) for term in terms]

        self.taxonomy_graph.remove_nodes_from([node[0] for node in nodes])
        self.taxonomy_graph.add_nodes_from(nodes)

        edges = set()
        for term in terms:
            edges = edges.union(edges, set([(start, term.uri) for start in term.boarder_uris]))
            edges = edges.union(edges, set([(term.uri, end) for end in term.narrower_uris]))
        self.taxonomy_graph.add_edges_from(list(edges))

    def add_term(self, term):
        self.taxonomy_graph.add_node(term.uri, term.__dict__)

    def add_relationship(self, parent_term_uri, child_term_uri):
        self.taxonomy_graph.add_edge(parent_term_uri, child_term_uri)

    def remove_term(self, term_uri):
        try:
            self.taxonomy_graph.remove_node(term_uri)
        except NetworkXError:
            print("{} '{}' doesn't exist".format(NEO4J_NODE_LABEL, term.uri))

    def remove_relationship(self, parent_term_uri, child_term_uri):
        try:
            self.taxonomy_graph.remove_edge(parent_term_uri, child_term_uri)
        except NetworkXError:
            print("Relationship between '{}' and '{}' doesn't exist".format(parent_term_uri, child_term_uri))

    def edit_term(self, term):
        try:
            self.taxonomy_graph.nodes[term.uri].update(term.__dict__)  
        except KeyError: # Be careful
            print("{} '{}' doesn't exist".format(NEO4J_NODE_LABEL, term.uri))

    # def edit_relationship(self): # Relation have no properties
    #     pass

    def save_to_neo4j(self):
        # Or try: nx.write_graphml(g, 'path/to/file.graphml')
        # Save taxonomy_graph to Neo4J DB
        self.neo4j_connector.delete_all()

        for term_uri, term_data_dict in self.taxonomy_graph.nodes.items():
            this_term = BaseTerm(**term_data_dict)
            self.neo4j_connector.add_term(this_term)

        for term_uri, term_data_dict in self.taxonomy_graph.nodes.items():
            this_term = BaseTerm(**term_data_dict)

            for pterm_uri in term_data_dict['boarder_uris']:
                pterm = BaseTerm(**self.taxonomy_graph.nodes[pterm_uri])
                self.neo4j_connector.add_relation(pterm, this_term)

            for cterm_uri in term_data_dict['narrower_uris']:
                cterm = BaseTerm(**self.taxonomy_graph.nodes[cterm_uri])
                self.neo4j_connector.add_relation(this_term, cterm)

    # def load_from_neo4j(self):
    #     # Load taxonomy_graph from Neo4J DB
    

    

    