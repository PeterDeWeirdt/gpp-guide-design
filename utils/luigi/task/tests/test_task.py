from .. import *
import luigi
import os

class HelloTask(luigi.ExternalTask):
    rd = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(os.path.join(self.rd, 'data/hello.txt'))

class Hello2(luigi.Task):
    rd = luigi.Parameter()
    requires = Requires()
    hellotask = Requirement(HelloTask)

    def output(self):
        return luigi.LocalTarget(os.path.join(self.rd, 'data/hello2.txt'))

    def run(self):
        with self.hellotask.output().open('r') as hello_file:
            hello = hello_file.readlines()
        with self.output().open('w') as f:
            f.writelines(hello)

def test_task(rootdir):
    luigi.build([Hello2(rd=rootdir)], local_scheduler=True)
    os.remove(os.path.join(rootdir, 'data/hello2.txt'))


