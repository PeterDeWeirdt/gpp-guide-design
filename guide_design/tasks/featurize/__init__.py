from ..get_data import RS2CombData
import luigi
from utils.luigi import task
from utils.featurization import featurize_guides
import pandas as pd


class Featurize(luigi.Task):
    __version__ = '0.1'
    activity_column = luigi.Parameter()
    kmer_column = luigi.Parameter()
    features = luigi.DictParameter()
    pam_start = luigi.IntParameter()
    pam_length = luigi.IntParameter()
    guide_start = luigi.IntParameter()
    guide_length = luigi.IntParameter()

    requires = task.Requires()
    filtered = task.Requirement(RS2CombData)
    output = task.SaltedOutput(base_dir='data/featurized', ext='.csv')

    def run(self):
        reqs = self.requires()
        interim_target = reqs['filtered'].output()
        with interim_target.open('r') as interim_file:
            interim_mat = pd.read_csv(interim_file)
        kmers = interim_mat[self.kmer_column]
        featurized_kmers = featurize_guides(kmers, self.features, self.pam_start,
                                            self.pam_length, self.guide_start,
                                            self.guide_length)
        featurized_kmers['activity'] = interim_mat[self.activity_column]
        with self.output().open('w') as f:
            featurized_kmers.to_csv(f)
