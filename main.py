import guide_design
import luigi
from utils.luigi import task



class DumbTask(luigi.Task):
    __version__='0.1'
    bool = luigi.BoolParameter()
    if bool == True:
        int = 2
    else:
        int = 3
    output = task.SaltedOutput(base_dir='./data', ext='.txt')
    def run(self):
        with self.output().open('w') as f:
            f.write('hello world!')


class AltDumbTask(luigi.Task):
    __version__='0.4'
    bool = luigi.BoolParameter()
    if bool == True:
        int = 2
    else:
        int = 3
    output = task.SaltedOutput(base_dir='./data', ext='.txt')
    def run(self):
        with self.output().open('w') as f:
            f.write('hello world?')

class DumbTask2(luigi.Task):
    __version__='0.2'
    bool = luigi.BoolParameter()
    requires = task.Requires()
    dt = task.Requirement(AltDumbTask)
    output = task.SaltedOutput(base_dir='./data', ext='.txt')
    def run(self):
        reqs = self.requires()
        with reqs['dt'].output().open('r') as in_f:
            with self.output().open('w') as out_f:
                out_f.write(in_f.read())

if __name__ == '__main__':
    luigi.build([DumbTask2(bool = True)], local_scheduler=True)
