from os import path, stat
from PySide.QtCore import QThread
import gc
from pyPdf.pdf import PdfFileWriter, PdfFileReader, PageObject

class Job(object):
    def __init__(self, pdf_file, directory, form, pps):
        """
        Constructs a job model with all details for the BookletGenerator() to work on it.
        """
        self.pdf_file = pdf_file
        self.directory = directory
        self.form = form
        self.pps = pps

    def paper_dimensions(self):
        """

        """
        pass


class BookletGenerator(QThread):
    exiting = False

    def __init__(self, job, parent=None):
        """
        The core class, The Generator.
        """
        QThread.__init__(self, parent)
        self.job = job

    def validate_inputs(self):
        """
        check if the job have a real file name and directory parameters.
        """
        try:
            path.isfile(self.job.pdf_file)
            #if PdfFileReader(file(self.job.pdf_file, "rb")).getIsEncrypted(): raise
            stat(self.job.directory)
            return True

        except (IOError, OSError):
            return False

    def pair_pages(self):
        """
        construct a new copy of the pdf file and append as many blank pages to
        the end to pair the pages.
        """
        paired_pages = PdfFileWriter()

        for page in PdfFileReader(file(self.job.pdf_file, "rb")).pages:
            paired_pages.addPage(page)

        while paired_pages.getNumPages() % 4 != 0:
            paired_pages.addBlankPage()

        return  paired_pages

    def order_pages(self, pages):
        """
        couple each two pages, and returns the front side and back side pages numbers.
        """

        pages_count = pages.getNumPages()

        front_side_pages = zip(range(1, pages_count / 2, 2), range(pages_count - 2, 0, -2))
        back_side_pages = reversed(zip(range(0, pages_count, 2), range(pages_count - 1, pages_count / 2, -2)))

        ProgressStatus.message = "Ordering pages ..."
        ProgressStatus.percentage = 5

        return pages, front_side_pages, back_side_pages

    def generate_files(self, pages, front_side_pages, back_side_pages):
        """
        scale each two pages to fit into one sheet, construct the document
        and write out two files: the front side and the back side files.
        """
        front_output = PdfFileWriter()
        back_output = PdfFileWriter()
        size = 841 / 2
        num_pages = pages.getNumPages()

        for index, page in enumerate(front_side_pages):
            #(w, h) = page_model.mediaBox.upperRight
            page_model = PageObject.createBlankPage(width=841, height=595)
            page_model.mergeScaledTranslatedPage(pages.getPage(page[0]), tx=0, ty=0, scale=0.7)
            page_model.mergeScaledTranslatedPage(pages.getPage(page[1]), tx=size, ty=0, scale=0.7)
            front_output.addPage(page_model)

            ProgressStatus.message = "Processing front  pages ... (%s of %s)" % (index, num_pages / 4)
            ProgressStatus.percentage = float(index) / float(pages.getNumPages() / 4) * 50
            if self.exiting: return

        for index, page in enumerate(back_side_pages):
            page_model = PageObject.createBlankPage(width=841, height=595)
            page_model.mergeScaledTranslatedPage(pages.getPage(page[0]), tx=0, ty=0, scale=0.7)
            page_model.mergeScaledTranslatedPage(pages.getPage(page[1]), tx=size, ty=0, scale=0.7)
            back_output.addPage(page_model)
            ProgressStatus.message = "Processing back pages ... (%s of %s)" % (index, num_pages / 4)
            ProgressStatus.percentage = float(index) / float(pages.getNumPages() / 4) * 50 + 50
            if self.exiting: return

        with file(path.join(self.job.directory, "(front_side_pages) " + path.basename(self.job.pdf_file)), "wb") as stream:
            ProgressStatus.message = "Writing files..."
            front_output.write(stream)

        with file(path.join(self.job.directory, "(back_side_pages) " + path.basename(self.job.pdf_file)), "wb") as stream:
            ProgressStatus.message = "Writing files..."
            back_output.write(stream)

        ProgressStatus.message = "Finished"
        ProgressStatus.percentage = 100


    def run(self):
        """
        the entry point for the BookletGenerator thread.
        """
        pp = self.pair_pages()
        op, fp, bp = self.order_pages(pp)
        self.generate_files(op, fp, bp)


class ProgressStatus(object):
    message = "Ready"
    percentage = 0