from ..get_data import ResData, FcData
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



