#!/usr/bin/env python
#    ------------------------------------------------------------------------------------------
#    Copyright 2012 Hassen Ben Yedder. All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without modification, are
#    permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice, this list of
#          conditions and the following disclaimer.
#
#       2. Redistributions in binary form must reproduce the above copyright notice, this list
#          of conditions and the following disclaimer in the documentation and/or other materials
#          provided with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE AUTHOR ''AS IS'' AND ANY EXPRESS OR IMPLIED
#    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#    FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#    ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#    The views and conclusions contained in the software and documentation are those of the
#    authors and should not be interpreted as representing official policies, either expressed
#    or implied, of the author.
#    ------------------------------------------------------------------------------------------

__author__ = 'Hassen Ben Yedder'
__version__ = '1.0.0'
__license__ = 'BSD license'

import sys
import platform
from PySide import QtGui, QtCore
import time
import PySide
from PyBooklet_ui import Ui_MainWindow as UI
from bookletgen import BookletGenerator, ProgressStatus, Job



class MainWindow(QtGui.QMainWindow, UI):
    def __init__(self, parent=None):
        """
        The main window, the controller.

        Setup the UI and handles all the the user interactions, shows confirmation dialogs
        and connects signals.
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.progress = ProgressUpdater()
        self.progress.progress_signal.connect(self.update_progress)
        self.progress.finished.connect(self.finished_)

        self.generate.clicked.connect(self.generate_clicked)
        self.select_file.clicked.connect(self.select_file_clicked)
        self.select_directory.clicked.connect(self.select_directory_clicked)


        def actionAbout():
            """
            Pop-up the AboutBox dialog.
            """
            QtGui.QMessageBox.about(self,
                                    "About PyBooklet",
                                    """<b>PyBooklet</b> v %s
                                    <p>Copyright (c) 2011, %s.
                                    All rights reserved in accordance with The %s
                                    <p>This application can be used to create PDF booklets.
                                    <p>Python %s -  PySide version %s - Qt version %s on %s""" %
                                    (__version__, __author__, __license__,
                                     platform.python_version(),
                                     PySide.__version__,
                                     PySide.QtCore.__version__,
                                     platform.system()))

        self.actionAbout.activated.connect(actionAbout)

    def select_file_clicked(self):
        """
        pop up a file dialog and reflect the inputs to the selected_file textbox.
        """
        self.selected_file.setText(
            QtGui.QFileDialog.getOpenFileName(self, str("Open File"), "/", str("PDF Files (*.pdf)"))[0])

    def select_directory_clicked(self):
        """
        pop up a directory dialog and reflect the inputs to the selected_directory textbox.
        """
        self.selected_directory.setText(QtGui.QFileDialog.getExistingDirectory(self))

    def generate_clicked(self):
        """
        when clicked it fire the Generator and the ProgressUpdater
        thread with all the details gathered from the UI.
        it then toggle to allow abortion of the running threads.
        """

        if self.generate.text() == "Generate PDFs":

            job = Job(pdf_file=self.selected_file.text(),
                      directory=self.selected_directory.text(),
                      form=self.page_size.currentText(),
                      pps=self.pps.currentText())

            gen = BookletGenerator(job)

            if gen.validate_inputs():
                self.progress.exiting = False
                BookletGenerator.exiting = False

                gen.setParent(self)
                gen.start()
                self.progress.start()

                self.generate.setText("Cancel")

            else:
                QtGui.QMessageBox.warning(self, "PyBooklet", "No such file or directory" + " " * 30)
        else:
            self.progress.exiting = True
            BookletGenerator.exiting = True
            
            self.generate.setText("Generate PDFs")

    def finished_(self):
        """
        pop up a dialog when the generator returns or when the job is cancelled
        and reset the progress bar ot its initial state.
        """
        if QtGui.QMessageBox.information(self, "PyBooklet", "Finished" + " " * 30) == QtGui.QMessageBox.Ok:
            ProgressStatus.message = "Ready"
            ProgressStatus.percentage = 0
            self.progressBar_label.setText(ProgressStatus.message)
            self.progressBar.setValue(ProgressStatus.percentage)

            self.generate.setText("Generate PDFs")
            
            ProgressUpdater.exiting = False
            BookletGenerator.exiting = False

    def update_progress(self, message, percentage):
        """
        receives signals from ProgressUpdater and refreshes the
        progressBar component with the emitted values.
        """
        self.progressBar.setValue(percentage)
        self.progressBar_label.setText(message)


class ProgressUpdater(QtCore.QThread):
    progress_signal = QtCore.Signal(str, int)
    exiting = False

    def __init__(self, parent=None):
        """
        ProgressBar Updater thread.
        """

        QtCore.QThread.__init__(self, parent)


    def run(self):
        """
        When running, it follow the BookletGenerator progress status and emit signals to
        update the ProgressBar and the text associated with it. Signals are connected to
        the UpdateProgress() through the mainWindow to keep track of the progress without
        freezing the UI.
        """

        while not ProgressStatus.message == "Finished" and not self.exiting:
            self.progress_signal.emit(ProgressStatus.message, ProgressStatus.percentage)
            time.sleep(0.2)


            
        return
if __name__ == "__main__":
    Application = QtGui.QApplication(sys.argv)
    Application.setApplicationName("PyBooklet")
    Application.setStyle('cleanlooks')
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(Application.exec_())