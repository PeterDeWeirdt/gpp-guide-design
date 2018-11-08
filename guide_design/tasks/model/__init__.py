from ..cross_validate import CrossValidate
import luigi
from utils.luigi import task
import pickle
import numpy as np
from ..featurize import FeaturizeTrain, FeaturizeTest
from ..featurize import TestData
import pandas as pd

class BestModel(luigi.Task):
    __version__ = '0.2'

    requires = task.Requires()
    cv_lasso = task.Requirement(CrossValidate, model_str='lasso',
                                param_grid = {'alpha': np.logspace(-4, 0, 48).tolist()})
    cv_gb = task.Requirement(CrossValidate, model_str='GB',
                             param_grid = {'max_depth': [int(x) for x in np.linspace(2, 40, 4)],
                                          'max_features': ['log2', 'sqrt'],
                                          'min_samples_split': np.linspace(0.01, 0.4, 3).tolist(),
                                          'subsample': [0.8, 1]})

    output = task.SaltedOutput(base_dir='data/models', ext='.pickle', format=luigi.format.Nop)

    def run(self):
        reqs = self.requires()
        best_fit = None
        for model, cv_x in reqs.items():
            with cv_x.output().open('rb') as f:
                cv_model = pickle.load(f)
                score = cv_model.best_score_
                curr_estimator =  cv_model.best_estimator_
                if best_fit is None:
                    best_estimator = curr_estimator
                    best_fit = score
                elif best_fit < score:
                    best_estimator = curr_estimator
                    best_fit = score

        with self.output().open('wb') as f:
            pickle.dump(best_estimator, f)

class ModelCoefficients(luigi.Task):
    __version__ = '0.1'
    model = task.Requirement(BestModel)

    requires = task.Requires()

    output = task.SaltedOutput(base_dir='data/figures', ext='.csv')

    def run(self):
        ...

class PredictModel(luigi.Task):
    __version__ = '0.2'

    requires = task.Requires()
    model = task.Requirement(BestModel)
    test_mat = task.Requirement(FeaturizeTest, activity_column ='percentile',
                                kmer_column = 'X30mer',
                                features = {'Pos. Ind. 1mer': True,
                                                        'Pos. Ind. 2mer': True,
                                                        'Pos. Ind. 3mer': False,
                                                        'Pos. Dep. 1mer': True,
                                                        'Pos. Dep. 2mer': True,
                                                        'Pos. Dep. 3mer': False,
                                                        'GC content': True,
                                                        'Tm': True},
                                guide_start = 5, guide_length = 20,
                                pam_start = 25, pam_length = 3)

    output = task.SaltedOutput(base_dir='data/predictions', ext='.csv')

    def run(self):
        reqs = self.requires()
        with reqs['model'].output().open('rb') as f:
            model = pickle.load(f)
        with reqs['test_mat'].output().open('r') as f:
            test_mat = pd.read_csv(f)
        y = test_mat['activity']
        X = test_mat[test_mat.columns.difference(['activity', 'kmer'])]
        predictions = model.predict(X)
        prediction_mat = pd.DataFrame({'kmer': test_mat['kmer'], 'true': y, 'predicted': predictions})
        with self.output().open('w') as f:
            prediction_mat.to_csv(f)





