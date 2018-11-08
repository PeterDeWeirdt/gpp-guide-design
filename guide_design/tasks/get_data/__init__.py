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

class TestData(luigi.ExternalTask):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/SpCas9_test_guides.csv')

class AzimuthPredictions(luigi.Task):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/raw/')
