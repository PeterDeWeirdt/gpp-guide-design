from ..featurize import FeaturizeTrain, Standardize
import luigi
from luigi.util import inherits
from utils.luigi import task
import pandas as pd
from sklearn import ensemble
from sklearn import linear_model
from sklearn import model_selection
from sklearn import preprocessing
import pickle
from ..get_data import RS2CombData
from sklearn import neural_network
from sklearn import metrics


@inherits(FeaturizeTrain) # Inherits Featurize Train's parameters
class CrossValidate(luigi.Task):
    __version__ = '0.5'
    model_str = luigi.Parameter()
    folds = luigi.IntParameter(default=10)
    param_grid = luigi.DictParameter()
    requires = task.Requires()
    scaler = task.Requirement(Standardize, activity_column ='percentile',
                                   kmer_column = 'X30mer')

    featurized = task.Requirement(FeaturizeTrain)

    output = task.SaltedOutput(base_dir='data/cv', ext='.pickle', format=luigi.format.Nop)

    def run(self):
        reqs = self.requires()
        featurized = reqs['featurized']
        with featurized.output().open('r') as f:
            featurized_df = pd.read_csv(f)
        with reqs['scaler'].output().open('rb') as f:
           scaler = pickle.load(f)
        y = featurized_df['activity']
        X = featurized_df[featurized_df.columns.difference(['activity', 'kmer'])]
        X_train = scaler.transform(X)
        #X_train = X
        if self.model_str == 'GB':
            model = ensemble.GradientBoostingRegressor()
        elif self.model_str == 'RF':
            model = ensemble.RandomForestRegressor()
        elif self.model_str == 'lasso':
            model = linear_model.Lasso()
        elif self.model_str == 'EN':
            model = linear_model.ElasticNet()
        elif self.model_str == 'NN':
            model = neural_network.MLPRegressor()
        grid_search = model_selection.RandomizedSearchCV(model, dict(self.param_grid),
                                                   cv = self.folds,
                                                   scoring='neg_mean_squared_error',
                                                         n_iter=40, n_jobs=10)
        grid_search.fit(X_train, y)
        # Use path because we have to write binary (stack: localTarget pickle)
        with self.output().open('wb') as f:
            pickle.dump(grid_search, f)




