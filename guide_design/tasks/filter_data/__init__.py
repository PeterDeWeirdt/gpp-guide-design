from ..get_data import RS2CombData, AchillesTestData, OofFc, OofGv2, OofRes
import luigi
from utils.luigi import task
import pandas as pd




class FilteredRS2Data(luigi.Task):
    __version__ = '0.1'
    requires = task.Requires()
    rs2_file = task.Requirement(RS2CombData)
    oof_fc_file = task.Requirement(OofFc)
    oof_res_file = task.Requirement(OofRes)

    output = task.SaltedOutput(base_dir='./data/filtered', ext='.csv')

    def run(self):
        with self.rs2_file.output().open('r') as f:
            rs2_data = pd.read_csv(f)
        with self.oof_fc_file.output().open('r') as f:
            oof_fc_data = pd.read_csv(f)
        with self.oof_res_file.output().open('r') as f:
            oof_res_data = pd.read_csv(f)
        rs2_oof_data = (pd.merge(oof_res_data[['30mer', 'OOF mutation rate']],
                                 oof_fc_data[['30mer', 'OOF mutation rate']], how = 'outer')
                            .merge(rs2_data, how='inner', on='30mer')
                            .drop_duplicates()
                        )


        with self.output().open('w') as f:
            rs2_oof_data.to_csv(f)


class FilteredAchillesData(luigi.Task):
    __version__ = '0.1'
    requires = task.Requires()
    achilles_file = task.Requirement(AchillesTestData)

    oof_gv2_file = task.Requirement(OofGv2)

    output = task.SaltedOutput(base_dir='./data/filtered', ext='.csv')

    def run(self):
        with self.achilles_file.output().open('r') as f:
            achilles_data = pd.read_csv(f)
        with self.oof_gv2_file.output().open('r') as f:
            oof_gv2_data = pd.read_csv(f)
        achilles_oof_data = (pd.merge(achilles_data, oof_gv2_data.drop_duplicates(),
                                      how='inner', on='X30mer')
                     .drop(['X', 'Unnamed: 0'], axis = 1)
                     .drop_duplicates())
        with self.output().open('w') as f:
            achilles_oof_data.to_csv(f)
