# Départ de l'exemple de geeksforgeeks.com
# source: https://www.geeksforgeeks.org/creating-your-own-python-ide-in-python/

# import des différents modules
import sys

from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTextBrowser  # pour l'interface


class PythonIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)  # dimension de la page
        self.setWindowTitle('Python IDE')  # nom de la page

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

    # Gestion de l'exécution du code
    def run_code(self):
        code = self.text_editor.toPlainText()  # récupère le texte écrit dans l'espace
        try:
            self.process = QProcess()  # créer un processus
            self.process.start("python", ['-c', code])  # lance le script python
            self.process.finished.connect(
                self.process_finished)  # liaison de la console pour l'afficher dans l'interface
            self.run_button.setEnabled(False)  # Désactive le bouton Run
        except Exception as e:
            self.output_widget.append(f"Error: {e}")  # Affiche l'erreur
            self.run_button.setEnabled(True)  # Active le bouton Run

    # Gestion de l'affichage dans l'interface du résultat de la console
    def process_finished(self, return_code):
        self.output_widget.clear()  # Nettoye le résultat précédent
        # S'il n'y a pas eu d'erreur
        if return_code == 0:
            output = self.process.readAllStandardOutput().data().decode()  # récupère le contenu de la console
            self.output_widget.append(output.strip())  # Affiche le contenu récupèrer dans l'interface
            self.run_button.setEnabled(True)  # Active le bouton Run
        # S'il y a une erreur
        else:
            # Même chose mais pour une erreur
            error = self.process.readAllStandardError().data().decode()
            self.output_widget.append(f"Error: {error}")
            self.run_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = PythonIDE()
    ide.show()
    sys.exit(app.exec_())
