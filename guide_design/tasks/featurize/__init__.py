from ..get_data import RS2CombData
import luigi
from utils.luigi import task


class Featurize(luigi.Task):
    __version__ = '0.0'
    activity_column = luigi.Parameter()
    kmer_column = luigi.Parameter()
    requires = task.Requires()
    filtered_exp = task.Requirement(RS2CombData)
    output = task.SaltedOutput(base_dir='data/featurized', ext='.csv')

    def run(self):


