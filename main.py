import luigi
from guide_design.tasks.featurize import FeaturizeTrain, FeaturizeTest
from guide_design.tasks.cross_validate import CrossValidate
from guide_design.tasks.model import BestModel, PredictModel
from guide_design.tasks.fasta_format import Fasta
from guide_design.tasks.get_data import TestData
import numpy as np


if __name__ == '__main__':
    stage = 'predict'
    if stage == 'feat':
        luigi.build([FeaturizeTest(activity_column ='percentile',
                                    kmer_column = 'X30mer',
                                    features = {'Pos. Ind. 1mer': True,
                                           'Pos. Ind. 2mer': True,
                                           'Pos. Ind. 3mer': True,
                                           'Pos. Dep. 1mer': True,
                                           'Pos. Dep. 2mer': True,
                                           'Pos. Dep. 3mer': True,
                                           'GC content': True,
                                           'Tm': True},
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
        luigi.build([PredictModel()], local_scheduler=True, workers=1)
    elif stage == 'fasta':
        luigi.build([Fasta(seq_col = '30mer')], local_scheduler=True)
