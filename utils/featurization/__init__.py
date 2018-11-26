import pandas as pd
from Bio.SeqUtils import MeltingTemp
import numpy as np


def get_frac_g_or_c(dict, guide_sequence):
    """Get gc content

    :param context: sequence
    :param len: length of guide
    :param guide_start: position that guide starts
    :return: curr_dict with gc content
    """
    g_count = guide_sequence.count('G')
    c_count = guide_sequence.count('C')
    gc_frac = (g_count + c_count)/len(guide_sequence)
    dict['g_or_c'] = gc_frac
    return dict


def get_one_nt_counts(dict, guide, nts):
    for nt in nts:
        nt_frac = guide.count(nt)/len(guide)
        dict[nt] = nt_frac
    return dict


def get_two_nt_counts(dict, guide, nts):
    for nt1 in nts:
        for nt2 in nts:
            two_mer = nt1 + nt2
            nts_counts = guide.count(two_mer)
            nts_frac = nts_counts/(len(guide) - 1)
            dict[nt1 + nt2] = nts_frac
    return dict


def get_three_nt_counts(dict, guide, nts):
    for nt1 in nts:
        for nt2 in nts:
            for nt3 in nts:
                k_mer = nt1 + nt2 + nt3
                nts_counts = guide.count(k_mer)
                nts_frac = nts_counts/(len(guide) - 2)
                dict[nt1 + nt2 + nt3] = nts_frac
    return dict


def get_one_nt_pos(dict, context_sequence, nts, context_order):
    for i in range(len(context_order)):
        curr_nt = context_sequence[i]
        for nt in nts:
            key = context_order[i] + nt
            if curr_nt == nt:
                dict[key] = 1
            else:
                dict[key] = 0
    return dict


def get_two_nt_pos(dict, context_sequence, nts, context_order):
    for i in range(len(context_order) - 1):
        curr_nts = context_sequence[i:i+2]
        for nt1 in nts:
            for nt2 in nts:
                match_nts = nt1+nt2
                key = context_order[i] + match_nts
                if curr_nts == match_nts:
                    dict[key] = 1
                else:
                    dict[key] = 0
    return dict


def get_three_nt_pos(dict, context_sequence, nts, context_order):
    for i in range(len(context_order) - 2):
        curr_nts = context_sequence[i:i+3]
        for nt1 in nts:
            for nt2 in nts:
                for nt3 in nts:
                    match_nts = nt1+nt2+nt3
                    key = context_order[i] + match_nts
                    if curr_nts == match_nts:
                        dict[key] = 1
                    else:
                        dict[key] = 0
    return dict


def get_thermo(dict, guide_sequence, context_sequence):
    # Use Biopython to get thermo info. from context and guides
    dict['Tm, context'] = MeltingTemp.Tm_NN(context_sequence)
    dict['Tm, 5mer-15'] = MeltingTemp.Tm_NN(guide_sequence[-5:])
    dict['Tm, 5mer-3'] = MeltingTemp.Tm_NN(guide_sequence[2:7])
    dict['Tm, middle'] = MeltingTemp.Tm_NN(guide_sequence[7:-5])
    return dict

def get_cas9_pam_n(dict, context_sequence, nts):
    for nt1 in nts:
        for nt2 in nts:
            motif = nt1 + 'G' + 'G' + nt2
            if context_sequence[24:28] == motif:
                dict['20' + motif] = 1
            else:
                dict['20' + motif] = 0
    return dict

def get_context_order(k, pam_start, pam_length, guide_start, guide_length):
    """

    :param k: length of kmer
    :param pam_start: indexed starting at one
    :param pam_length:
    :param guide_start:
    :param guide_length:
    :return: list of characters of each nt position
    """
    pam_order = ['P' + str(x) for x in range(1, pam_length + 1)]
    guide_order = [str(x) for x in range(1, guide_length + 1)]
    if pam_start == min(pam_start, guide_start):
        second_ord = pam_order
        third_ord = guide_order
    else:
        second_ord = guide_order
        third_ord = pam_order

    context_order = ['-' + str(x) for x in reversed(range(1, min(pam_start, guide_start)))] + \
                    second_ord + third_ord + ['+' + str(x) for x in range(1, k - min(pam_start, guide_start) + 1 -
                                                                          len(second_ord) -
                                                                          len(third_ord) + 1)]
    return context_order


def get_guide_sequence(context, guide_start, guide_length):
    return context[guide_start-1:(guide_start-1 + guide_length)]


def get_physiochemical(curr_dict, guide, nts, physiochemical_data):
    nt_counts = np.array([guide.count(nt1+nt2) for nt1 in nts for nt2 in nts])
    dinucs = physiochemical_data['Dinucleotides']
    no_dinucs = physiochemical_data.drop(columns=['Dinucleotides'])
    numeric_physio = np.transpose(np.array(no_dinucs))
    physio_sum = np.sum(nt_counts*numeric_physio, axis = 1)
    curr_dict = {**curr_dict, **dict(zip(no_dinucs.keys(), physio_sum))}
    return curr_dict

def get_zipper(dict, context_sequence, nts, context_order):
    for i in range(len(context_order) - 2):
        curr_nts = context_sequence[i] + context_sequence[i+2]
        for nt1 in nts:
            for nt2 in nts:
                match_nts = nt1+nt2
                key = context_order[i] + nt1 + 'N' + nt2
                if curr_nts == match_nts:
                    dict[key] = 1
                else:
                    dict[key] = 0
    return dict

def get_double_zipper(dict, context_sequence, nts, context_order):
    for i in range(len(context_order) - 3):
        curr_nts = context_sequence[i] + context_sequence[i+3]
        for nt1 in nts:
            for nt2 in nts:
                match_nts = nt1+nt2
                key = context_order[i] + nt1 + 'NN' + nt2
                if curr_nts == match_nts:
                    dict[key] = 1
                else:
                    dict[key] = 0
    return dict


def featurize_guides(kmers, features, pam_start, pam_length, guide_start, guide_length,
                     oof_mutation_rates=None):
    """Take guides and encodes for modeling

    :param kmers: vector with
    :param features: boolean dictionary of which feature types to inlcude
    :param pam_start: int
    :param pam_end: int
    :param guide_start: int
    :param guide_end: int
    :return: featurized matrix
    """
    physiochemical_data = pd.read_csv('data/raw/physiochem.csv')
    k = len(kmers[0])
    context_order = get_context_order(k, pam_start, pam_length, guide_start, guide_length)
    print(context_order)
    nts = ['A', 'C', 'T', 'G']
    feature_dict_list = []
    for i in range(len(kmers)):
        if i % 1000 == 0:
            print(str(i) + " guides coded")
        curr_dict = {}
        context = kmers[i]
        guide_sequence = get_guide_sequence(context, guide_start, guide_length)
        if features['GC content']:
            curr_dict = get_frac_g_or_c(curr_dict, guide_sequence)
        if features['Pos. Ind. 1mer']:
            curr_dict = get_one_nt_counts(curr_dict, guide_sequence, nts)
        if features['Pos. Ind. 2mer']:
            curr_dict = get_two_nt_counts(curr_dict, guide_sequence, nts)
        if features['Pos. Ind. 3mer']:
            curr_dict = get_three_nt_counts(curr_dict, guide_sequence, nts)
        if features['Pos. Dep. 1mer']:
            curr_dict = get_one_nt_pos(curr_dict, context, nts, context_order)
        if features['Pos. Dep. 2mer']:
            curr_dict = get_two_nt_pos(curr_dict, context, nts, context_order)
        if features['Pos. Dep. 3mer']:
            curr_dict = get_three_nt_pos(curr_dict, context, nts, context_order)
        if features['Tm']:
            curr_dict = get_thermo(curr_dict, guide_sequence, context)
        if features['Cas9 PAM']:
            curr_dict = get_cas9_pam_n(curr_dict, context, nts)
        if features['Physio']:
            curr_dict = get_physiochemical(curr_dict, guide_sequence, ['A','C','G','T'], physiochemical_data)
        if features['OOF Mutation Rate']:
            curr_dict['OOF Mutation Rate'] = oof_mutation_rates[i]
        if features['Zipper']:
            curr_dict = get_zipper(curr_dict, context, nts, context_order)
        if features['Double Zipper']:
            curr_dict = get_double_zipper(curr_dict, context, nts, context_order)
        feature_dict_list.append(curr_dict)
    feature_matrix = pd.DataFrame(feature_dict_list)
    return feature_matrix
