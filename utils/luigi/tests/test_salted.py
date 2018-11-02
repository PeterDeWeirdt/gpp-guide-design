from tempfile import TemporaryDirectory
from ..task import Requires, SaltedOutput
from unittest import TestCase
from luigi import *
import os


class SaltedTests(TestCase):
    def test_salted_tasks(self):
        with TemporaryDirectory() as tmp:
            class SomeTask(Task):
                __version__ = '0.1'
                output = SaltedOutput(base_dir=tmp)
                requires = Requires()

                def run(self):
                    with self.output().open('w') as f:
                        f.writelines(['hello world'])

            build([SomeTask()], local_scheduler=True)
            class SomeTask(Task):
                __version__ = '0.2'
                output = SaltedOutput(base_dir=tmp)
                requires = Requires()

                def run(self):
                    with self.output().open('w') as f:
                        f.writelines(['hello world'])

            build([SomeTask()], local_scheduler=True)
            assert len(os.listdir(tmp)) == 2



