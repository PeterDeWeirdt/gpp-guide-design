from ..get_data import ResData, FcData, Cpf1_A375_Controls, Cpf1_A375_Control_Context
import luigi
from utils.luigi import task


class CombineFilterData(luigi.Task):
    """Filter resistance and flow data for condition/gene combinations in the original paper.
    Combine both datasets"""

    requires = task.Requires()
    fc_data = task.Requirement(FcData)
    res_data = task.Requirement(ResData)


    def run(self):
        reqs = self.requires()
        fc_data = reqs['fc_data'].output()
        res_data = reqs['res_data'].output()


