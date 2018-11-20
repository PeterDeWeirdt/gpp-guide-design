import luigi


class ResData(luigi.ExternalTask):
    """Resistence data"""
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/RES_essential_nonessential_2017-08-17_v5.csv')


class FcData(luigi.ExternalTask):
    """Flow Cytometry Data"""
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/FC_essential_nonessential_2017-08-17_v5.csv')

class RS2CombData(luigi.ExternalTask):
    "All data from Rule Set 2"
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/RS2_data/V3_data.csv')

class DoenchTestData(luigi.ExternalTask):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/SpCas9_test_guides.csv')

class AchillesTestData(luigi.ExternalTask):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/EWS502_BONE_essential.csv')

class AzimuthPredictions(luigi.Task):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/')

class ScorePredictions(luigi.Task):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/ddAUC/Gv2_all_scores.txt')

class OofRes(luigi.Task):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/RES_data_mutation_rates.csv')

class OofFc(luigi.Task):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/FC_OOF_activity.csv')

class OofGv2(luigi.Task):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/Gv2_oof_scores.csv')
