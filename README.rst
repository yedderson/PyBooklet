PyBooklet
---------

.. image:: http://cloud.github.com/downloads/yedderson/PyBooklet/PyBooklet_screenshot.PNG
  :align: center

A GUI utility to convert a PDF file into 2 Pages-Per-Sheet double-sided booklet ready for printing.


THE IDEA:
---------

I needed to print a large pdf book about starting QT/Python programming and I couldn't find out how to make the print
double-sided with 2 pages per sheet, so I made this tool ... with Python and QT.

Learning by doing, yes. And again, the intention behind is to start a substantial open source project to familiarize
with all the aspects from working on a Version Control System and build a project structure to finally packaging
and distributing.

Usage:
------
two files are generated from the provided pdf file, the Front-side and Back-side file, they are to be printed in sequence :

.. image:: picture.png
  :align: center


Installation:
-------------
.. _download: http://github.com/yedderson/PyBooklet/downloads
A binary distribution for Windows is available to download_. or, if you want run it from source, run :

``pip install PyBooklet``

and
``Python PyBooklet.py`` afterward (PyBooklet.py will be in the scripts directory) to run the application


uninstall:
-----------
``pip uninstall Pybooklet``
