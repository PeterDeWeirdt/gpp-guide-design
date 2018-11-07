from ..get_data import RS2CombData
import luigi
from utils.luigi import task
import pandas as pd

class Fasta(luigi.Task):
    __version__ = '0.1'
    seq_col = luigi.Parameter()
    requires = task.Requires()
    seq_data = task.Requirement(RS2CombData)

    output = task.SaltedOutput(base_dir='./data/raw', ext='.FASTA')

    def run(self):
        reqs = self.requires()
        with reqs['seq_data'].output().open('r') as f:
            seq_data = pd.read_csv(f)
        seqs = seq_data[self.seq_col]
        with self.output().open('w') as f:
            for seq in seqs:
                f.write('>' + seq + '\n')
                f.write(seq + '\n')

