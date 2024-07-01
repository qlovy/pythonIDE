# Départ de l'exemple de geeksforgeeks.com
# source: https://www.geeksforgeeks.org/creating-your-own-python-ide-in-python/

# import des différents modules
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTextBrowser, QWidget # pour l'interface
from PyQt5.QtCore import QProcess


class PythonIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)    # dimension de la page
        self.setWindowTitle('Python IDE')       # nom de la page

        # l'endroit pour éditer le texte
        self.text_editor = QTextEdit(self)
        self.text_editor.setGeometry(10, 10, 780, 300)

        # l'endroit que renvoie le résultat du code
        self.output_widget = QTextBrowser(self)
        self.output_widget.setGeometry(10, 320, 780, 200)

        # le bouton pour interpreter le code
        self.run_button = QPushButton('Run', self)
        self.run_button.setGeometry(10, 530, 780, 30)
        self.run_button.clicked.connect(self.run_code)

    def run_code(self):
        code = self.text_editor.toPlainText()   # récupère le texte écrit dans l'espace
        try:
            self.process = QProcess()
            self.process.start("python", ['-c', code])
            self.process.finished.connect(self.process_finished)
            self.run_button.setEnabled(False)
        except Exception as e:
            self.output_widget.append(f"Error: {e}")
            self.run_button.setEnabled(True)

    def process_finished(self, return_code):
        if return_code == 0:
            output = self.process.readAllStandardOutput().data().decode()
            self.output_widget.append(output.strip())
            self.run_button.setEnabled(True)
        else:
            error = self.process.readAllStandardError().data().decode()
            self.output_widget.append(f"Error: {error}")
            self.run_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = PythonIDE()
    ide.show()
    sys.exit(app.exec_())
