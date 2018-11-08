from ..featurize import FeaturizeTrain
import luigi
from utils.luigi import task
import pandas as pd
from sklearn import ensemble
from sklearn import linear_model
from sklearn import model_selection
import pickle
from ..get_data import RS2CombData


class CrossValidate(luigi.Task):
    __version__ = '0.3'
    model_str = luigi.Parameter()
    folds = luigi.IntParameter(default=10)
    param_grid = luigi.DictParameter()
    requires = task.Requires()

    featurized = task.Requirement(FeaturizeTrain, activity_column ='score_drug_gene_rank',
                                  kmer_column = '30mer',
                                  features = {'Pos. Ind. 1mer': True,
                                                        'Pos. Ind. 2mer': True,
                                                        'Pos. Ind. 3mer': False,
                                                        'Pos. Dep. 1mer': True,
                                                        'Pos. Dep. 2mer': True,
                                                        'Pos. Dep. 3mer': False,
                                                        'GC content': True,
                                                        'Tm': True},
                                  guide_start = 5, guide_length = 20,
                                  pam_start = 25, pam_length = 3,
                                  InterimTask = RS2CombData)

    output = task.SaltedOutput(base_dir='data/cv', ext='.pickle', format=luigi.format.Nop)

    def run(self):
        reqs = self.requires()
        featurized = reqs['featurized']
        with featurized.output().open('r') as f:
            featurized_df = pd.read_csv(f)
        y = featurized_df['activity']
        X = featurized_df[featurized_df.columns.difference(['activity', 'kmer'])]
        if self.model_str == 'GB':
            model = ensemble.GradientBoostingRegressor(n_estimators=100,
                                                       min_samples_leaf=3)
        elif self.model_str == 'RF':
            model = ensemble.RandomForestRegressor()
        elif self.model_str == 'lasso':
            model = linear_model.Lasso(max_iter = 10000, normalize=True)
        elif self.model_str == 'EN':
            model = linear_model.ElasticNet(max_iter= 10000, normalize=True)
        grid_search = model_selection.GridSearchCV(model, dict(self.param_grid),
                                                   cv = self.folds,
                                                   scoring='neg_mean_squared_error')
        grid_search.fit(X, y)
        # Use path because we have to write binary (stack: localTarget pickle)
        with self.output().open('wb') as f:
            pickle.dump(grid_search, f)




