.. image:: https://travis-ci.com/PeterDeWeirdt/gpp-guide-design.svg?branch=master
    :target: https://travis-ci.com/PeterDeWeirdt/gpp-guide-design

=============================
Broad GPP SpCas9 Guide Design
=============================

Build machine learning Models to predict CRISPR Cas9 guide activity.

Features
--------

* Luigi for task workflow organization
* Salted outputs for file version control
* Docker for a reproducible environment

Usage
-----
This app is for building models and does not
include any out-of-the-box predictors.

Installation
^^^^^^^^^^^^
In a local directory, use

.. code-block:: bash

    git clone git@github.com:PeterDeWeirdt/gpp-guide-design.git

For a completely reproducible environment install Docker_ and
`Docker Compose`_. If you use the professional edition of PyCharm you
can `set it up`_ to use docker-compose as the default interpreter,
otherwise you can use the command line.

.. _Docker: https://docs.docker.com/install/#reporting-security-issues
.. _`Docker Compose`: https://docs.docker.com/compose/install/
.. _`set it up`: https://www.jetbrains.com/help/pycharm/docker-compose.html

Example
^^^^^^^

Once these dependencies are installed, in the gpp-guide-design directory
you can build your environment

.. code-block:: bash

    docker-compose build

And run the example workflow

.. code-block:: bash

    docker-compose run app python main.py

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
