Installation
============
Bethic Photo Survey (BPS) runs on Linux, Mac, and Windows operating systems. There are a few different ways to install BPS. You can `download the code`_ from the `bitbucket`_, you can install with the python `pip`_ installer, or you can `git`_ to clone the code from the `bitbucket`_ repository. More details are provided below along with information about software requirements and details specific to installing on different platforms.

Requirements
------------
The following items need to be installed in order for BPS to work.

1. `Python 2.7`_ BPS may work on older versions of Python but I wouldn't bet on it
2. `pyexiv2`_ has actually been deprecated now. I will eventually rewrite the code to use GExiv2 but, for now, pyexiv2 is required.
3. `Matplotlib`_ can be installed as part of `SciPy`_.

Ways to Get BPS
---------------
There are two different ways to get release versions of BPS and one way to get the latest code from the repository.

Installing the Latest Release with pip
______________________________________

Go to the command line and type ``pip install BenthicPhotoSurvey``. Depending on your OS, you may need to type ``sudo pip install BenthicPhotoSurvey`` instead and enter your root password.

In order to run BPS, you have to figure out where `pip`_ installed the code and that can vary according to OS and configuration. If you have version of pip >= 1.2.1.post1, you can figure it out by typing ``pip show BenthicPhotoSurvey`` on your command line. The response should contain the location of the ``benthic_photo_survey`` directory. To run BPS, navigate to that directory and start BPS by typing ``python benthic_photo_survey.py`` (on Windows, you'll leave off the ``python`` and just type ``benthic_photo_survey.py``).

On my computer it looks somthing like this::

    blah@blahbidyblah:~$ pip show BenthicPhotoSurvey
    ---
    Name: BenthicPhotoSurvey
    Version: 0.1
    Location: /usr/local/lib/python2.7/dist-packages
    Requires: 

So, to launch, I type::

    blah@blahbidyblah:~$ cd /usr/local/lib/python2.7/dist-packages/benthic_photo_survey
    blah@blahbidyblah:/usr/local/lib/python2.7/dist-packages/benthic_photo_survey$ python benthic_photo_survey.py

...and the program should run and you can move on to the :doc:`tutorial`. I will, hopefully, get around to packaging BPS a little better so it's easier to launch after installing but this will have to do for now.

Downloading and Installing a Release from bitbucket
___________________________________________________

Use your web browser to `download the code`_ from bitbucket. Unzip that file somewhere. Navigate into the ``benthic_photo_survey`` directory that contains ``benthic_photo_survey.py`` and type ``python benthic_photo_survey.py`` (on Windows, you'll leave off the ``python`` and just type ``benthic_photo_survey.py``).

Getting the Latest Code from bitbucket
______________________________________

This method is not recommended unless you want the very latest code because the development code may be full of bugs. First, make sure you have `git`_ installed. Then open the command line where you'd like to put the code and type ``git clone https://jkibele@bitbucket.org/jkibele/benthic_photo_survey.git``. That will download the latest code **which may not be stable**. To run it just follw the instructions from the previous subsection.

Windows
-------

I will write up the exact steps for Windows here. I think you may be able to get all the requirements taken care of with the `PythonXY`_ installer.

Mac
---

Need to write up these steps too.

Ubuntu
------

Need to write up these steps too.

Testing
-------

I will describe how to run the automated tests and how to use the test data that's installed with BPS to make sure everything is working.

.. _download the code: https://bitbucket.org/jkibele/benthic_photo_survey/downloads
.. _bitbucket: https://bitbucket.org/jkibele/benthic_photo_survey
.. _pip: https://pypi.python.org/pypi/pip
.. _git: http://git-scm.com/
.. _Python 2.7: http://www.python.org/download/releases/2.7.3/
.. _pyexiv2: http://tilloy.net/dev/pyexiv2/
.. _Matplotlib: http://matplotlib.org/
.. _SciPy: http://scipy.org/
.. _PythonXY: http://code.google.com/p/pythonxy/
