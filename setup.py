from distutils.core import setup

setup(
    name='PyBooklet',
    version='1.0.0',
    author='Hassen Ben Yedder',
    author_email='hassenbenyedder@gmail.com',
    packages=['PyBooklet',],
    url='http://PyBooklet.sourceforge.net',
    download_url='http://PyBooklet.sourceforge.net',
    requires=['pyPdf', 'PySide'],
    provides=['PyBooklet'],
    keywords=['pdf', 'book', 'print'],
    description="Converts PDFs to booklets",
    long_description= "a GUI utility to convert a regular pdf book file into 2 pages-per-sheet / double sided booklet ready for printing",
    platforms='any',
    license='BSD',
    classifiers=['Topic :: Utilities',
                 'Topic :: Printing',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Intended Audience :: End Users/Desktop',
                 'Development Status :: 5 - Production/Stable',
                 'Programming Language :: Python :: 2.7'],
    package_data={'PyBooklet': ['resources/*.qrc','resources/*.ui','resources/images/*'],},
    py_modules=['PyBooklet','PyBooklet.Generator'],
    scripts = ['PyBooklet.py']
    )