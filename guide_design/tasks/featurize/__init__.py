from ..get_data import RS2CombData, DoenchTestData, AchillesTestData
from ..filter_data import FilteredRS2Data, FilteredAchillesData
import luigi
from utils.luigi import task
from utils.featurization import featurize_guides
import pandas as pd
from sklearn import preprocessing
import pickle
from luigi.util import inherits

class BaseFeaturize(luigi.Task):
    __version__ = '0.6'
    activity_column = luigi.Parameter()
    kmer_column = luigi.Parameter()
    features = luigi.DictParameter()
    pam_start = luigi.IntParameter()
    pam_length = luigi.IntParameter()
    guide_start = luigi.IntParameter()
    guide_length = luigi.IntParameter()

    requires = task.Requires()
    output = task.SaltedOutput(base_dir='data/featurized', ext='.csv')

    def run(self):
        reqs = self.requires()
        interim_target = reqs['filtered'].output()
        with interim_target.open('r') as interim_file:
            interim_mat = pd.read_csv(interim_file)
        kmers = interim_mat[self.kmer_column]
        featurized_kmers = featurize_guides(kmers, self.features, self.pam_start,
                                            self.pam_length, self.guide_start,
                                            self.guide_length,
                                            oof_mutation_rates=interim_mat['OOF mutation rate'])
        featurized_kmers['activity'] = interim_mat[self.activity_column]
        featurized_kmers['kmer'] = interim_mat[self.kmer_column]
        with self.output().open('w') as f:
            featurized_kmers.to_csv(f, index=False)


class FeaturizeTrain(BaseFeaturize):

    filtered = task.Requirement(FilteredRS2Data)




class FeaturizeDoenchTest(BaseFeaturize):

    filtered = task.Requirement(DoenchTestData)

class FeaturizeAchillesTest(BaseFeaturize):

    filtered = task.Requirement(FilteredAchillesData)


class Standardize(luigi.Task):
    __version__ = '0.1'
    activity_column = luigi.Parameter()
    kmer_column = luigi.Parameter()
    features = luigi.DictParameter()
    guide_start = luigi.IntParameter()
    guide_length = luigi.IntParameter()
    pam_start = luigi.IntParameter()
    pam_length = luigi.IntParameter()

    requires = task.Requires()
    featurized = task.Requirement(FeaturizeTrain)

    output = task.SaltedOutput(base_dir='data/featurized', ext='.csv',
                               format=luigi.format.Nop)

    def run(self):
        reqs = self.requires()
        with reqs['featurized'].output().open('r') as f:
            test_mat = pd.read_csv(f)
        X = test_mat[test_mat.columns.difference(['activity', 'kmer'])]
        scaler = preprocessing.StandardScaler().fit(X)
        with self.output().open('wb') as f:
            pickle.dump(scaler, f)
