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


@inherits(FeaturizeTrain) # Inherits Featurize Train's parameters
class CrossValidate(luigi.Task):
    __version__ = '0.4'
    model_str = luigi.Parameter()
    folds = luigi.IntParameter(default=10)
    param_grid = luigi.DictParameter()
    requires = task.Requires()
    #scaler = task.Requirement(Standardize, activity_column ='score_drug_gene_rank',
    #                                kmer_column = '30mer')

    featurized = task.Requirement(FeaturizeTrain)

    output = task.SaltedOutput(base_dir='data/cv', ext='.pickle', format=luigi.format.Nop)

    def run(self):
        reqs = self.requires()
        featurized = reqs['featurized']
        with featurized.output().open('r') as f:
            featurized_df = pd.read_csv(f)
        #with reqs['scaler'].output().open('rb') as f:
        #    scaler = pickle.load(f)
        y = featurized_df['activity']
        X = featurized_df[featurized_df.columns.difference(['activity', 'kmer'])]
        #X_train = scaler.transform(X)
        X_train = X
        if self.model_str == 'GB':
            model = ensemble.GradientBoostingRegressor(alpha=0.5, init=None, learning_rate=0.1, loss='ls',
             max_depth=3, max_features=None, max_leaf_nodes=None,
             min_samples_leaf=1, min_samples_split=2,
             min_weight_fraction_leaf=0.0, n_estimators=100,
             presort='auto', random_state=1, subsample=1.0, verbose=0,
             warm_start=False)
        elif self.model_str == 'RF':
            model = ensemble.RandomForestRegressor()
        elif self.model_str == 'lasso':
            model = linear_model.Lasso(max_iter = 10000)
        elif self.model_str == 'EN':
            model = linear_model.ElasticNet(max_iter= 10000)
        elif self.model_str == 'NN':
            model = neural_network.MLPRegressor()
        grid_search = model_selection.GridSearchCV(model, dict(self.param_grid),
                                                   cv = self.folds,
                                                   scoring='neg_mean_squared_error')
        grid_search.fit(X_train, y)
        # Use path because we have to write binary (stack: localTarget pickle)
        with self.output().open('wb') as f:
            pickle.dump(grid_search, f)




