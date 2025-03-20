from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QFontMetricsF
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules: list[tuple[QRegExp, QTextCharFormat]] = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#Cf79c6"))  # Rose

        other_keyword_format = QTextCharFormat()
        other_keyword_format.setForeground(QColor("#000090"))  # Bleu

        name_format = QTextCharFormat()
        name_format.setForeground(QColor("#3030D0"))  # Bleu clair

        class_name_format = QTextCharFormat()
        class_name_format.setForeground(QColor("#007000"))  # Vert foncé

        def_name_format = QTextCharFormat()
        def_name_format.setForeground(QColor("#A0A010"))  # Jaune

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#42B442"))  # Vert

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#C03000"))  # Orange

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#62B472"))  # Gris vert
        comment_format.setFontItalic(True)

        keywords = [
            "import", "from", "as", "return", "if", "else", "assert",
            "elif", "while", "for", "break", "continue", "try", "except",
            "finally", "with", "yield", "del", "pass", "raise"
        ]
        others_keywords = [ "class", "def", "False", "True", "None", "global", "nonlocal", "and", "or", "not", "is", "in", "lambda" ]

        self.highlighting_rules.append((QRegExp(r'(([0-9]+)|(0x[0-9a-fA-F]+)|(0b(0|1)+))(?![a-zA-Z0-9])'), number_format))
        self.highlighting_rules.append((QRegExp(r'[A-Z][a-zA-Z0-9_]*'), class_name_format))
        self.highlighting_rules.append((QRegExp(r'\b[a-z_][a-zA-Z0-9_]*\b'), name_format))
        self.highlighting_rules.append((QRegExp(r'\b[a-z_][a-zA-Z0-9_]*\s?(?=\()'), def_name_format))
        self.highlighting_rules.append((QRegExp(r'(\b' + r"\b)|(\b".join(keywords) + r'\b)'), keyword_format))
        self.highlighting_rules.append((QRegExp(r'(\b' + r"\b)|(\b".join(others_keywords) + r'\b)'), other_keyword_format))
        self.highlighting_rules.append((QRegExp(r'(".*")|(\'.*\')'), string_format))
        self.highlighting_rules.append((QRegExp(r'#.*'), comment_format))

    def highlightBlock(self, text):
        for pattern, char_format in self.highlighting_rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, char_format)
                index = pattern.indexIn(text, index + length)

class CodeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.text_edit = QTextEdit()
        self.text_edit.setTabStopDistance(QFontMetricsF(self.text_edit.font()).horizontalAdvance(' ') * 4)
        self.layout().addWidget(self.text_edit)

        self.highlighter = PythonHighlighter(self.text_edit.document())


