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

class RS2model(luigi.ExternalTask):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/RS2_outputs')

class Cpf1_A375_Controls(luigi.ExternalTask):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/A375_EEF2_controls.csv')

class Cpf1_A375_Control_Context(luigi.ExternalTask):
    __version__ = '0.1'
    def output(self):
        return luigi.LocalTarget('./data/EEF2_control_context_output.csv')
