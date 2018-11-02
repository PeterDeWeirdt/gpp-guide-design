from .. import *
import pandas as pd

def test_context_order():
    assert get_context_order(34, 5, 4, 10, 23) == ['-4', '-3', '-2', '-1', 'P1', 'P2', 'P3', 'P4',
                                              '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                              '10', '11', '12', '13', '14', '15', '16', '17',
                                              '18', '19', '20', '21', '22', '23', '+1', '+2', '+3']

def test_guide_seq():
    assert get_guide_sequence('CGTCCCCATCCACGGCCTTCACCCGGGCAG', 5, 20) == 'CCCATCCACGGCCTTCACCC'


def test_featurization():
    features = {'Pos. Ind. 1mer': True,
                'Pos. Ind. 2mer': True,
                'Pos. Ind. 3mer': True,
                'Pos. Dep. 1mer': True,
                'Pos. Dep. 2mer': True,
                'Pos. Dep. 3mer': True,
                'GC content': True,
                'Tm': True}
    kmers = pd.Series(['ACTGGG'])
    one_hot = featurize_guides(kmers, features, pam_start=2,
                                      pam_length=1, guide_start=3, guide_length=3).iloc[0]
    assert (one_hot['+1G'] == 1) & (one_hot['TGG'] == 1.0) & (one_hot['g_or_c'] == 2/3) &\
    (one_hot['Tm, guide'] != 0) & (one_hot['1TG'] == 1) & (one_hot['2GGG'] == 1) &\
    (one_hot['G'] == 2/3) & (one_hot['TG'] == 1/2)
