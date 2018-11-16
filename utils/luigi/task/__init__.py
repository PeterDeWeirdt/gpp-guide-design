import luigi
from hashlib import sha256
import os



class Requirement:
    def __init__(self, task_class, **params):
        self.task_class = task_class
        self.params = params

    def __get__(self, task, cls):
        if task is None:
            return self
        return task.clone(
            self.task_class,
            **self.params)



class Requires:
    """Composition to replace :meth:`luigi.task.Task.requires`

    Example::

        class MyTask(Task):
            # Replace task.requires()
            requires = Requires()
            other = Requirement(OtherTask)

            def run(self):
                # Convenient access here...
                with self.other.output().open('r') as f:
                    ...

        >>> MyTask().requires()
        {'other': OtherTask()}

    """

    def __get__(self, task, cls):
        # Bind self/task in a closure
        return lambda : self(task)

    def __call__(self, task):
        """Returns the requirements of a task

        Assumes the task class has :class:`.Requirement` descriptors, which
        can clone the appropriate dependences from the task instance.

        :returns: requirements compatible with `task.requires()`
        :rtype: dict
        """
        # Search task.__class__ for Requirement instances
        # return
        print(task)
        return_dict = {k: v.__get__(task, self) for k, v in task.__class__.__dict__.items() if
                isinstance(v, Requirement)}
        return return_dict

def get_salted_version(task):
    """Create a salted id/version for this task and lineage

    :returns: a unique, deterministic hexdigest for this task
    :rtype: str

    CITE: https://github.com/gorlins/salted
    """

    msg = ""

    # Salt with lineage

    # Note that order is important and impacts the hash - if task
    # requirements are a dict, then consider doing this is sorted order
    msg += '|'.join([get_salted_version(req)[:8] for req in luigi.task.flatten(task.requires())])

    # Uniquely specify this task
    msg += '\t' + '|'.join([

            # Basic capture of input type
            task.__class__.__name__,

            # Change __version__ at class level when everything needs rerunning!
            task.__version__,

        ] + [
            # Depending on strictness - skipping params is acceptable if
            # output already is partitioned by their params; including every
            # param may make hash *too* sensitive
            '{}={}'.format(param_name, repr(task.param_kwargs[param_name]))
            for param_name, param in sorted(task.get_params())
            if param.significant
        ]
    )
    log_str = msg + '\t' + sha256(msg.encode()).hexdigest()[:8] + '\n'
    if log_str not in open('data/hash.txt').read():
        with open('data/hash.txt', 'a') as f:
            f.write(log_str)
    return sha256(msg.encode()).hexdigest()

class SaltedOutput:
    def __init__(self, base_dir='data', file_pattern='{task.__class__.__name__}-{hash}',
                 ext='.txt', **target_kwargs):
        self.base_dir = base_dir
        self.file_pattern = file_pattern
        self.ext = ext
        self.target_kwargs = target_kwargs

    def __get__(self, task, cls):
        # Determine the path etc here
        return lambda: luigi.LocalTarget(os.path.join(self.base_dir,
                                         self.file_pattern.format(task=task, hash=get_salted_version(task)[:8]) + self.ext),
                                         **self.target_kwargs)
