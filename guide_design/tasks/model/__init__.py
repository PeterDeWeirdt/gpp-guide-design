from ..cross_validate import CrossValidate
import luigi
from luigi.util import inherits
from utils.luigi import task
import pickle
import numpy as np
from ..featurize import FeaturizeTrain, FeaturizeDoenchTest, Standardize, FeaturizeAchillesTest
from ..featurize import DoenchTestData
import pandas as pd
from sklearn import ensemble
from sklearn import linear_model
from sklearn import preprocessing
from copy import deepcopy


class BestModel(luigi.Task):
    __version__ = '0.3'
    features = luigi.DictParameter()
    guide_start = luigi.IntParameter()
    guide_length = luigi.IntParameter()
    pam_start = luigi.IntParameter()
    pam_length = luigi.IntParameter()
    activity_column = luigi.Parameter()
    kmer_column = luigi.Parameter()

    requires = task.Requires()

    example = True
    if example:
        cv_lasso = task.Requirement(CrossValidate, model_str='lasso',
                                    param_grid = {'alpha': np.logspace(-3, 0, 100).tolist()})
    else:
        cv_gb = task.Requirement(CrossValidate, model_str='GB',
                                 param_grid = {'max_depth': [int(x) for x in np.linspace(2, 40, 30)],
                                              'max_features': np.linspace(0.01, 0.3, 50).tolist(),
                                              'min_samples_split': np.linspace(0.01, 0.4, 50).tolist(),
                                              'subsample': np.linspace(0.6, 1, 50).tolist(),
                                               'alpha': np.linspace(0.5,0.99, 50).tolist()})
    # cv_nn = task.Requirement(CrossValidate, model_str = 'NN',
    #                          param_grid = {'alpha':np.logspace(-4, -0.01, 100).tolist(),
    #                                        'learning_rate_init': np.linspace(0.001, 0.3, 50).tolist()})
    # cv_gb = task.Requirement(CrossValidate, model_str = 'GB',
    #                         param_grid = {'alpha': [0.5]})

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

def score_coefs(X, y, B, a):
    """Rank each model coefficient by fraction of variance explained

    :param X: predictor matrix
    :param y: response matrix
    :param B: model coefficients
    :return ranked_coefs: vector of variance explained for each coefficient in B
    """
    model_residuals = np.matmul(X, B) + a - y
    model_variance = np.var(model_residuals)
    coef_score = []
    for i in range(len(B)):
        if B[i] == 0:
            coef_score.append(0)
        else:
            curr_B = deepcopy(B)
            curr_B[i] = 0
            curr_residuals = np.matmul(X, curr_B) + a - y
            curr_variance = np.var(curr_residuals)
            coef_score.append(1-model_variance/curr_variance)
    return coef_score*np.sign(B)


class ModelCoefficients(luigi.Task):
    __version__ = '0.3'
    features = luigi.DictParameter()
    guide_start = luigi.IntParameter()
    guide_length = luigi.IntParameter()
    pam_start = luigi.IntParameter()
    pam_length = luigi.IntParameter()

    requires = task.Requires()

    model = task.Requirement(BestModel, activity_column ='percentile',
                                  kmer_column = 'X30mer')
    scaler = task.Requirement(Standardize, activity_column='percentile',
                              kmer_column='X30mer')
    train_mat = task.Requirement(FeaturizeTrain, activity_column = 'percentile',
                                 kmer_column = 'X30mer')
    output = task.SaltedOutput(base_dir='data/models', ext='.csv')

    def run(self):
        reqs = self.requires()
        with reqs['model'].output().open('rb') as f:
            model = pickle.load(f)
        with reqs['train_mat'].output().open('r') as f:
            train_mat = pd.read_csv(f)
        with reqs['scaler'].output().open('r') as f:
            scaler = pickle.load(f)
        X = train_mat[train_mat.columns.difference(['activity', 'kmer'])]
        if model.__class__ == ensemble.GradientBoostingRegressor:
            importances = model.feature_importances_
        elif model.__class__ == linear_model.Lasso:
            importances = score_coefs(scaler.transform(X), train_mat['activity'],
                                      model.coef_, model.intercept_)
        feature_importances = pd.DataFrame({'feature': X.keys(),
                                            'importance': importances})
        with self.output().open('w') as f:
            feature_importances.to_csv(f, index=False)


class PredictModel(luigi.Task):
    __version__ = '0.2'
    features = luigi.DictParameter()
    guide_start = luigi.IntParameter()
    guide_length = luigi.IntParameter()
    pam_start = luigi.IntParameter()
    pam_length = luigi.IntParameter()
    true_val = luigi.BoolParameter(default=True)

    requires = task.Requires()
    model = task.Requirement(BestModel, activity_column ='percentile',
                                  kmer_column = 'X30mer')
    test_mat = task.Requirement(FeaturizeAchillesTest, activity_column='sgRNA.measured.value',
                                kmer_column='X30mer')
    scaler = task.Requirement(Standardize, activity_column ='percentile',
                                   kmer_column = 'X30mer')

    output = task.SaltedOutput(base_dir='data/predictions', ext='.csv')

    def run(self):
        reqs = self.requires()
        with reqs['model'].output().open('rb') as f:
            model = pickle.load(f)
        with reqs['test_mat'].output().open('r') as f:
            test_mat = pd.read_csv(f)
        with reqs['scaler'].output().open('rb') as f:
           scaler = pickle.load(f)
        y = test_mat['activity']
        X = test_mat[test_mat.columns.difference(['activity', 'kmer'])]
        X_train = scaler.transform(X)
        #X_train = X
        predictions = model.predict(X_train)
        prediction_mat = pd.DataFrame({'kmer': test_mat['kmer'], 'true': y, 'predicted': predictions})
        with self.output().open('w') as f:
            prediction_mat.to_csv(f, index=False)





