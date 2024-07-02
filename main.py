# Départ de l'exemple de geeksforgeeks.com
# source: https://www.geeksforgeeks.org/creating-your-own-python-ide-in-python/

import keyword as key_py
# import des différents modules
import sys

from PyQt5.QtCore import QProcess, QRegExp
from PyQt5.QtGui import QFont, QFontDatabase, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTextBrowser, QAction, \
    QFileDialog, QTabWidget  # pour l'interface


class PythonIDE(QMainWindow):
    # L'initialisation de L'IDE
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)  # dimension de la page
        self.setWindowTitle('Python IDE')  # nom de la page

        # polices personnalisées
        QFontDatabase.addApplicationFont("fonts/DejaVuSansMono.ttf")
        # dejavu_font = QFont("DejaVu Sans Mono", 10)

        QFontDatabase.addApplicationFont("fonts/OpenSans-Regular.ttf")
        open_sans_font = QFont("Open Sans", 10)

        # Applique la police a toute l'interface
        self.setFont(open_sans_font)

        # Création du menu
        menu_bar = self.menuBar()

        # Création du menu "File"
        file_menu = menu_bar.addMenu('File')

        # Création de l'action pour creér un nouveau fichier
        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)  # ajout de l'action au menu

        # Création de l'action pour ouvrir un fichier
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Création de l'action pour sauver un fichier
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Création de l'action pour enregistrer sous un fichier
        save_as_action = QAction('Save as', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        # le nom du fichier au début
        self.filename = "newfile.py"

        # l'endroit pour éditer le texte
        # L'onglet
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(10, 25, 780, 280)
        # Le partie texte
        self.text_editor = QTextEdit()
        self.text_editor.setTabStopWidth(12)  # défini la tabulation à 4 espaces
        self.text_editor.setGeometry(10, 25, 780, 280)
        self.tab_widget.addTab(self.text_editor, self.filename)

        # l'endroit que renvoie le résultat du code
        self.output_widget = QTextBrowser(self)
        self.output_widget.setGeometry(10, 320, 780, 200)

        # le bouton pour interpreter le code
        self.run_button = QPushButton('Run', self)
        self.run_button.setGeometry(10, 530, 780, 30)
        self.run_button.clicked.connect(self.run_code)

        # Initalisation du processus
        self.process = QProcess()

        syntax_highlighter(self.text_editor)

    # Création d'un nouveau fichier
    def new_file(self):
        self.text_editor.clear()
        self.tab_widget.addTab(self.text_editor, "newfile.py")

    # Ouverture d'un fichier
    def open_file(self):
        self.text_editor.clear()
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', './',
                                                    "Python Files (*.py)")  # Ouvre l'interface pour ouvrir un fichier
        # Si le fichier est séléctionné
        if self.filename[0]:
            # On l'ouvre
            with open(self.filename[0], 'r') as f:
                text = f.read()  # On récupère le contenu du fichier
                self.text_editor.insertPlainText(text)  # On affiche le code récupèrer
        self.tab_widget.addTab(self.text_editor, self.filename[0].split("/")[
            -1])  # Actualise le nom de l'onglet et récupère le nom du fichier

    # Enregistrer sous un fichier
    def save_as_file(self):
        self.filename = QFileDialog.getSaveFileName(self, 'Save File', './',
                                                    "Python Files (*.py)")  # Ouvre l'interface pour sauver un fichier
        # Si le fichier est séléctionné
        if self.filename[0]:
            text = self.text_editor.toPlainText()  # récupère le code
            with open(self.filename[0], 'w') as f:
                f.write(text)  # écrit le code dans le fichier

        self.tab_widget.addTab(self.text_editor, self.filename[0].split("/")[-1])

    # Enregister un fichier
    def save_file(self):
        # si le fichier n'est pas encore enregistrer
        if self.filename == "newfile.py":
            self.save_as_file()  # processus d'enregistrer sous
        if self.filename[0]:
            text = self.text_editor.toPlainText()  # récupère le code
            with open(self.filename[0], 'w') as f:
                f.write(text)  # écrit le code dans le fichier

    # Gestion de l'exécution du code
    def run_code(self):
        code = self.text_editor.toPlainText()  # récupère le texte écrit dans l'espace
        try:
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


# Met en couleur les différents mots du code
class syntax_highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(syntax_highlighter, self).__init__(parent)  # Appelle le constructeur

        keyword_format = QTextCharFormat()
        keyword_format.setFontWeight(QFont.Bold)  # On met la police en gras
        keyword_format.setForeground(QColor("blue"))  # On définit la couleur pour qu'elle soit bleue

        self.highlightingRules = []  # Contient tous les mots clé du langages

        # Ajout des mots-clés dans la liste
        for key in key_py.kwlist:
            self.highlightingRules.append((QRegExp(fr"\b{key}\b"), keyword_format))

    # Appelé pour chaque bloque de texte dans l'éditeur (text_editor)
    def highlightBlock(self, text):
        # Nous parcourons la liste highlightingRules
        # et pour chaque règle, nous recherchons une occurrence de l'expression régulière
        # dans le bloc actuel en utilisant la méthode indexIn.
        for pattern, format in self.highlightingRules:
            index = pattern.indexIn(text)
            while index >= 0:
                # si on trouve une occurrence, on calcule sa longueur en utilisant la méthode matchedLength()
                length = pattern.matchedLength()
                # Si l'index est possible et le mot-clé n'est pas entouré de guillemets
                if index > 0 and index - 1 < len(text) and text[index - 1] == '"':
                    index = pattern.indexIn(text, index + length)
                # Si l'index est possible et le mot-clé n'est pas entouré de guillemets
                elif index + length <= len(text) and text[index + length - 1] == '"':
                    index = pattern.indexIn(text, index + length)
                # Sinon on applique juste le format
                else:
                    self.apply_format(index, length, format)
                    index = pattern.indexIn(text, index + length)
                # puis on continue dans le reste du bloc

    def apply_format(self, start, length, format):
        self.setFormat(start, length, format)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = PythonIDE()
    ide.show()
    sys.exit(app.exec_())
