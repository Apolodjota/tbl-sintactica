import sys
import ply.lex as lex
import ply.yacc as yacc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont

# --------------------
# 1. LÉXICO (TOKENIZER)
# Se definen los componentes léxicos (tokens) de nuestra gramática.
# --------------------
tokens = (
    'SALUDO',  # Palabras como 'Hola', 'Buenos días'
    'SUJETO',  # Una palabra que empieza con mayúscula (Nombre propio)
    'PALABRA',  # Cualquier palabra en minúsculas (actuará como verbo o parte del complemento)
    'DESPEDIDA',  # Palabras como 'Adiós', 'Chao'
    'COMA',  # El símbolo ','
    'PUNTO'  # El símbolo '.'
)

# Reglas de Expresiones Regulares para tokens simples
t_COMA = r','
t_PUNTO = r'\.'


# REGLAS CON PRIORIDAD (DEFINIDAS COMO FUNCIONES)
# Ply da prioridad a las reglas definidas como funciones sobre las variables.

def t_SALUDO(t):
    r'Hola|Buenos\sdías|Qué\stal'
    return t


def t_DESPEDIDA(t):
    r'Adiós|Hasta\sluego|Nos\svemos|Chao'
    return t


def t_SUJETO(t):
    r'[A-Z][a-z]+'  # Una palabra que inicia con mayúscula
    # Se verifica que no sea una palabra reservada (saludo/despedida)
    if t.value in ['Hola', 'Buenos días', 'Qué tal']:
        t.type = 'SALUDO'
    elif t.value in ['Adiós', 'Hasta luego', 'Nos vemos', 'Chao']:
        t.type = 'DESPEDIDA'
    return t


def t_PALABRA(t):
    r'[a-z]+'  # Cualquier palabra en minúsculas.
    return t


# Caracteres a ignorar (espacios y tabulaciones)
t_ignore = ' \t'


# Manejo de saltos de línea para contar las líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1


# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Construir el lexer
lexer = lex.lex()

# --------------------
# 2. SINTÁCTICO (PARSER)
# Se define la estructura gramatical de la oración.
# --------------------

# Variable global para almacenar los pasos del análisis para la tabla
tabla_sintactica = []


# Definición de la gramática
def p_oracion(p):
    '''oracion : SALUDO COMA SUJETO PALABRA complemento PUNTO DESPEDIDA'''
    # Esta regla principal se activa si la oración es completamente válida.
    # p[0] es el resultado de la regla.
    # p[1]...p[7] son los valores de los tokens en orden.
    global tabla_sintactica
    tabla_sintactica = [
        ["SALUDO", p[1], "SAL → Hola | Buenos días | ...", "SAL"],
        ["COMA", p[2], "Símbolo de puntuación", ","],
        ["SUJETO", p[3], "S → [A-Z][a-z]+", "S"],
        ["VERBO", p[4], "V → [a-z]+", "V"],
        ["COMPLEMENTO", p[5], "C → PALABRA C | PALABRA", "C"],
        ["PUNTO", p[6], "Símbolo de puntuación", "."],
        ["DESPEDIDA", p[7], "D → Adiós | Chao | ...", "D"]
    ]
    p[0] = "Oración Válida"  # Devuelve un éxito


def p_complemento_recursivo(p):
    '''complemento : PALABRA complemento'''
    # Regla recursiva: una palabra seguida de otro complemento
    p[0] = p[1] + " " + p[2]


def p_complemento_base(p):
    '''complemento : PALABRA'''
    # Caso base: el complemento es una sola palabra
    p[0] = p[1]


# Manejo de errores de sintaxis
def p_error(p):
    global tabla_sintactica
    if p:
        mensaje = f"Error de sintaxis en '{p.value}' (Tipo: {p.type})"
        tabla_sintactica = [["ERROR", p.value, mensaje, "-"]]
    else:
        mensaje = "Error de sintaxis al final de la entrada (EOF)."
        tabla_sintactica = [["ERROR", "EOF", mensaje, "-"]]


# Construir el parser
parser = yacc.yacc()


# --------------------
# 3. INTERFAZ GRÁFICA (PyQt5)
# --------------------

class AnalizadorSintactico(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Validador Sintáctico con GLC")
        self.setGeometry(100, 100, 750, 550)

        # Layout principal
        self.layout = QVBoxLayout()

        # 1. Etiqueta para mostrar la Gramática (GLC)
        self.glc_label = QLabel("<b>Gramática Libre de Contexto (GLC)</b>")
        self.layout.addWidget(self.glc_label)

        glc_text = """
        <pre>
        O (Oración) → SALUDO , SUJETO VERBO COMPLEMENTO . DESPEDIDA
        SALUDO      → Hola | Buenos días | Qué tal
        SUJETO      → [A-Z][a-z]+  (Ej: Maria, Pedro)
        VERBO       → [a-z]+       (Ej: corre, come)
        COMPLEMENTO → PALABRA COMPLEMENTO | PALABRA
        PALABRA     → [a-z]+       (Ej: en, el, parque)
        DESPEDIDA   → Adiós | Hasta luego | Nos vemos | Chao
        </pre>
        """
        self.grammar_display = QLabel(glc_text)
        self.grammar_display.setFont(QFont("Courier New", 10))
        self.layout.addWidget(self.grammar_display)

        # 2. Entrada de texto
        self.label = QLabel("<b>Ingresa una oración para validar:</b>")
        self.layout.addWidget(self.label)

        self.input_text = QTextEdit()
        self.input_text.setFixedHeight(60)
        self.input_text.setPlaceholderText("Ej: Hola, Maria corre en el parque. Adiós")
        self.layout.addWidget(self.input_text)

        # 3. Botón de análisis
        self.button = QPushButton("Analizar")
        self.button.clicked.connect(self.analizar)
        self.layout.addWidget(self.button)

        # 4. Etiqueta de resultado
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.layout.addWidget(self.result_label)

        # 5. Tabla para mostrar el análisis sintáctico
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Componente", "Lexema (Entrada)", "Regla Aplicada", "No Terminal"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.tabla)

        self.setLayout(self.layout)

    def analizar(self):
        global tabla_sintactica
        tabla_sintactica = []  # Limpiar la tabla de resultados anteriores

        texto = self.input_text.toPlainText().strip()
        if not texto:
            self.result_label.setText("📝 Por favor, ingresa una oración.")
            self.tabla.setRowCount(0)
            return

        # Realizar el análisis sintáctico
        parser.parse(texto, lexer=lexer)

        # Determinar el resultado y actualizar la etiqueta
        if tabla_sintactica and tabla_sintactica[0][0] != "ERROR":
            self.result_label.setText("✅ Oración VÁLIDA según la GLC.")
            self.result_label.setStyleSheet("color: green;")
        else:
            self.result_label.setText("❌ Oración INVÁLIDA.")
            self.result_label.setStyleSheet("color: red;")
            if not tabla_sintactica:  # Si la tabla está vacía, es un error no capturado
                tabla_sintactica.append(["ERROR", texto, "La estructura no coincide con la gramática.", "-"])

        # Poblar la tabla con los resultados
        self.tabla.setRowCount(len(tabla_sintactica))
        for row_idx, fila in enumerate(tabla_sintactica):
            for col_idx, valor in enumerate(fila):
                self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AnalizadorSintactico()
    ventana.show()
    sys.exit(app.exec_())