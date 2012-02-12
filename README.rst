PyBooklet
---------
A GUI utility to convert PDF files into a 2 Pages-Per-Sheet double-sided booklets ready for printing.

.. image:: https://github.com/downloads/yedderson/PyBooklet/PyBooklet_screenshot.PNG


THE IDEA
--------
I needed to print a large pdf book about starting development with Python and QT and I couldn't find out how to make the print
double-sided with 2 pages per sheet, so I made this tool ... with Python and QT.

Learning by doing, yes. And again, the intention behind is to start an open source project from the ground up to familiarize
with all the aspects from working on a VCS System and organizing a project structure to packaging and distributing.

Usage
-----
Two files are generated from the provided pdf file, the Front-side and Back-side files, they are to be printed in sequence :

.. image:: https://github.com/downloads/yedderson/PyBooklet/pybooklet_manual.png
  :scale: 80 %


Installation
------------
.. _download: http://github.com/yedderson/PyBooklet/downloads
A binary distribution for Windows is available to download_. or, if you want run it from source, install it with : ::

 pip install PyBooklet

A launcher script will be placed in the Python's Scripts directory, to run the application use: ::

 Python PyBooklet.py

uninstall
---------

 ::

 pip uninstall PyBooklet

