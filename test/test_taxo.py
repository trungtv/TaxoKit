import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taxokit.taxonomy import Taxonomy
from taxokit.terms.base_term import BaseTerm

taxo = Taxonomy()

term_1 = BaseTerm('Data Science', [], ['Data Analysis', 'Machine Learning'], 'Data Science', 'DS', 'DS', 'DS Description...')
term_2 = BaseTerm('Data Analysis', ['Data Science'], [], 'Data Analysis', 'DA', 'DA', 'DA Description...')
term_3 = BaseTerm('Machine Learning', ['Data Science'], [], 'Machine Learning', 'ML', 'ML', 'ML Description...')

terms = [term_1, term_2, term_3]

taxo.build_or_update(terms)
print('The first build:')
for term_uri, term_data_dict in taxo.taxonomy_graph.nodes.items():
    print('{}: {}'.format(term_uri, term_data_dict))
print('='*50)

term_4 = BaseTerm('Deep Learning', ['Machine Learning'], [], 'Deep Learning', 'DL', 'DL', 'DL Description...')
taxo.build_or_update([term_4])
print('After the update:')
for term_uri, term_data_dict in taxo.taxonomy_graph.nodes.items():
    print('{}: {}'.format(term_uri, term_data_dict))
taxo.save_to_neo4j()

