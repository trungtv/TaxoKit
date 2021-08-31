from py2neo import Graph, Node, Relationship, NodeMatcher
from py2neo.errors import ClientError
import os

NEO4J_HOST = os.environ.get("NEO4J_HOST", "localhost")
NEO4J_PORT = 7687
NEO4J_USER = "neo4j"
NEO4J_PASS = "123456"
NEO4J_URL = "http://bolt://{}:{}@{}:{}".format(NEO4J_USER, NEO4J_PASS, NEO4J_HOST, NEO4J_PORT)
NEO4J_RELATIONSHIP_NAME = 'IS_PARENT_OF'
NEO4J_NODE_LABEL = 'Term'

class Neo4jConnector:
    def __init__(self):
        self.graph = Graph("bolt://{}:7687".format(NEO4J_HOST), auth=(NEO4J_USER, NEO4J_PASS))
        try:
            self.graph.schema.create_uniqueness_constraint(NEO4J_NODE_LABEL, 'uri')
        except ClientError:
            pass
        self.matcher = NodeMatcher(self.graph)

    def add_term(self, term):
        term_node = Node(NEO4J_NODE_LABEL, **term.__dict__)
        try:
            self.graph.create(term_node)
        except ClientError:
            print("{} '{}' existed".format(NEO4J_NODE_LABEL, term_node['uri']))

    def add_relation(self, parent_term, child_term):
        parent_node = self.matcher.match(NEO4J_NODE_LABEL, **parent_term.__dict__).first()
        child_node = self.matcher.match(NEO4J_NODE_LABEL, **child_term.__dict__).first()
        parent_to_child = Relationship(parent_node, NEO4J_RELATIONSHIP_NAME, child_node)
        self.graph.create(parent_to_child)

    def delete_all(self):
        self.graph.delete_all()

    # def remove_term(self):
    #     pass

    # def remove_relation(self):
    #     pass

    # def export_to_file(self):
    #     pass

    # def import_from_file(self):
    #     pass