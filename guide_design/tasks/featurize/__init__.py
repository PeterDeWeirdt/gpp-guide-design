from ..get_data import RS2CombData, DoenchTestData, AchillesTestData, Gv2Test, RS3Train
from ..filter_data import FilteredRS2Data, FilteredAchillesData, FilteredRS3Data
import luigi
from utils.luigi import task
from utils.featurization import featurize_guides
import pandas as pd
from sklearn import preprocessing
import pickle
from luigi.util import inherits

class BaseFeaturize(luigi.Task):
    __version__ = '0.8'
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
    # ["Cd28", "Cd3e", "CD45", "Cd5", "Cd43", "H2-K", "Thy1",
    #  "CD13_TF-1", "CD13_NB4", "CD33_NB4", "CD33_MOLM-13",
    #  "CD15_MOLM-13", "CCDC101_AZD", "CUL3_PLX",
    #  "HPRT1_6TG", "MED12_AZD", "MED12_PLX", "NF1_PLX", "NF2_PLX",
    #  "TADA1_AZD", "TADA2B_AZD"]

    filtered = task.Requirement(FilteredRS3Data,
                                assays = ["CD45", "Cd28", "Cd5", "Cd43", "H2-K", "Thy1",
                                          "CD13_TF-1", "CD33_MOLM-13",
                                          "CD15_MOLM-13", "CCDC101_AZD",
                                          "HPRT1_6TG", "MED12_AZD", "NF1_PLX", "NF2_PLX",
                                          "TADA1_AZD", "TADA2B_AZD"],
                                assays_end = ["CD45", "Cd5", "Cd43", "H2-K", "Thy1",
                                               "CD33_MOLM-13", "HPRT1_6TG", "MED12_AZD",
                                                "NF1_PLX", "NF2_PLX", "TADA2B_AZD"]
,
                                assays_start = ["CD13_TF-1","CD15_MOLM-13", "CD45"],
                                perc_pep_end = 80, perc_pep_start = 20)

class FeaturizeDoenchTest(BaseFeaturize):

    filtered = task.Requirement(DoenchTestData)

class FeaturizeAchillesTest(BaseFeaturize):

    filtered = task.Requirement(Gv2Test)


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
