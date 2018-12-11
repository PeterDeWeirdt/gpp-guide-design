'''
Author: Mudra Hegde
Email: mhegde@broadinstitute.org
Gets guide context given the guide sequence, PAM length, Transcript ID and taxon
'''

from urllib import request
import pandas as pd
import csv


def revcom(s):
    basecomp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    letters = list(s[::-1])
    letters = [basecomp[base] for base in letters]
    return ''.join(letters)


def get_t_seq(t, taxon):
    url = 'http://useast.ensembl.org/'+taxon+'/Export/Output/Transcript?db=core;flank3_display=25;flank5_display=25;output=fasta;strand=forward;t='+t+';param=coding;param=peptide;param=utr5;param=utr3;param=exon;param=intron;genomic=unmasked;_format=Text'
    try:
        req = request.Request(url)
        response = request.urlopen(req).read()
        response = response.decode('utf8').replace("\r", "")
        features = response.split('>')
        full_seq = features[len(features)-1]
        lines = full_seq.split('\n')
        gene_seq = ''.join(lines[1:len(lines)])
    except:
        gene_seq = ''
    return gene_seq


def get_guide_context(sgrna, pam_length, t, taxon):
    num_nuc = 36 - len(sgrna) - pam_length - 4
    seq = get_t_seq(t, taxon)
    pos = seq.find(sgrna)
    if pos == -1:
        pos = seq.find(revcom(sgrna))
        if pos == -1:
            con_seq = ''
        else:
            con_seq = revcom(seq[(pos - pam_length - num_nuc):(pos + len(sgrna) + 4)])
    else:
        con_seq = seq[(pos - 4):(pos+len(sgrna)+pam_length+num_nuc)]
    return con_seq


if __name__ == '__main__':
    outputfile = './data/raw/CD45_guides_context.csv'
    sgrnas = pd.read_csv('./data/raw/CD45_guides.csv')
    with open(outputfile, 'w') as o:
        w = csv.writer(o,delimiter='\t')
        w.writerow(['ID','Target','PAM Index'])
        for i, r in sgrnas.iterrows():
            context = get_guide_context(r[0], 3, r[1], r[2])
            if i % 100 == 0:
                print(i)
            print(context)
            w.writerow([r[0]+'_'+r[1], context, 24])

