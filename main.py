import luigi
from guide_design.tasks.featurize import FeaturizeTrain, FeaturizeDoenchTest
from guide_design.tasks.cross_validate import CrossValidate
from guide_design.tasks.model import BestModel, PredictModel, ModelCoefficients
from guide_design.tasks.fasta_format import Fasta
from guide_design.tasks.get_data import DoenchTestData
from guide_design.tasks.filter_data import FilteredAchillesData, FilteredRS2Data
import numpy as np


if __name__ == '__main__':
    stage = 'predict'
    feats = {'Pos. Ind. 1mer': True,
            'Pos. Ind. 2mer': True,
            'Pos. Ind. 3mer': False,
            'Pos. Ind. Zipper': True,
            'Pos. Dep. 1mer': True,
            'Pos. Dep. 2mer': True,
            'Pos. Dep. 3mer': False,
            'Pos. Dep. Zipper': True,
            'Pos. Ind. Rep.': True,
            'GC content': True,
            'Tm': True,
            'Cas9 PAM': False,
            'Physio': True,
            'OOF Mutation Rate': True,
            'Double Zipper': False}
    if stage == 'feat':
        luigi.build([FeaturizeTrain(activity_column ='score_drug_gene_rank',
                                    kmer_column = '30mer',
                                    features = {'Pos. Ind. 1mer': True,
                                            'Pos. Ind. 2mer': True,
                                            'Pos. Ind. 3mer': False,
                                            'Pos. Dep. 1mer': True,
                                            'Pos. Dep. 2mer': True,
                                            'Pos. Dep. 3mer': False,
                                            'GC content': True,
                                            'Tm': True,
                                            'Cas9 PAM': False,
                                            'Physio': False,
                                            'OOF Mutation Rate': True
                                                },
                                    guide_start = 5, guide_length = 20,
                                    pam_start = 25, pam_length = 3)], local_scheduler=True)
    elif stage == 'cv':
        luigi.build([CrossValidate(model_str = model_str, folds = 10,
                                  param_grid = param_grid)
                     for model_str, param_grid in {'lasso': {'alpha': np.logspace(-1, 0, 1).tolist()},
                                                   'GB': {'max_depth': [int(x) for x in np.linspace(2, 40, 1)],
                                                          'max_features': ['log2', 'sqrt'],
                                                          'min_samples_split': np.linspace(0.2,0.4,1).tolist(),
                                                          'subsample': [0.8]}}.items()],
                    local_scheduler=True, workers=2)
    elif stage == 'model':
        luigi.build([BestModel()], local_scheduler=True, workers=2)
    elif stage == 'predict':
        luigi.build([PredictModel(features=feats,
                                guide_start = 5, guide_length = 20,
                                pam_start = 25, pam_length = 3)], local_scheduler=True, workers=1)
    elif stage == 'fasta':
        luigi.build([Fasta(seq_col = '30mer')], local_scheduler=True)
    elif stage == 'coefs':
        luigi.build([ModelCoefficients(features=feats,
                                guide_start = 5, guide_length = 20,
                                pam_start = 25, pam_length = 3)], local_scheduler=True, workers = 1)
    elif stage == 'filter':
        luigi.build([FilteredAchillesData(), FilteredRS2Data()], local_scheduler=True,
                    workers = 1)
