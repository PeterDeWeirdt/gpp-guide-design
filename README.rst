=============================
Broad GPP SpCas9 Guide Design
=============================






Build machine learning Models to predict CRISPR Cas9 guide activity.



Features
--------

* Luigi for task workflow organization
* Salted outputs for model version control


Usage
-----
This app is for building models and does not
include any out-of-the-box predictors.

Installation
^^^^^^^^^^^^
In a local directory, use

.. code-block:: bash

    git clone git@github.com:PeterDeWeirdt/gpp-guide-design.git

Then configure the app using the py3.6_venv included in this repo.
We recommend PyCharm_ for configuration_.

.. _configuration: https://www.jetbrains.com/help/pycharm-edu/configuring-local-python-interpreters.html.
.. _PyCharm: https://www.jetbrains.com/pycharm/download/#section=mac

Example
^^^^^^^
After configuration, you can build models from the included training data and predict
on our test data by running main.py.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
