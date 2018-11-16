from ..model import PredictModel
import luigi
from utils.luigi import task
from ..get_data import


class AnalyzePredictions(luigi.Task):
    __version__ = '0.1'
    guide_start = luigi.IntParameter()
    guide_length = luigi.IntParameter()
    pam_start = luigi.IntParameter()
    pam_length = luigi.IntParameter()

    requires = task.Requires()
    azimuth_predictions = task.Requirement()
    rs2_predictions = task.Requirement(PredictModel,
                             features = {'Pos. Ind. 1mer': True,
                                          'Pos. Ind. 2mer': True,
                                          'Pos. Ind. 3mer': False,
                                          'Pos. Dep. 1mer': True,
                                          'Pos. Dep. 2mer': True,
                                          'Pos. Dep. 3mer': False,
                                          'GC content': True,
                                          'Tm': True})
    dimer_predictions = task.Requirement(PredictModel,
                             features = {'Pos. Ind. 1mer': False,
                                          'Pos. Ind. 2mer': False,
                                          'Pos. Ind. 3mer': False,
                                          'Pos. Dep. 1mer': False,
                                          'Pos. Dep. 2mer': True,
                                          'Pos. Dep. 3mer': False,
                                          'GC content': True,
                                          'Tm': False})



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
        predictions = model.predict(X_train)
        prediction_mat = pd.DataFrame({'kmer': test_mat['kmer'], 'true': y, 'predicted': predictions})
        with self.output().open('w') as f:
            prediction_mat.to_csv(f, index=False)




