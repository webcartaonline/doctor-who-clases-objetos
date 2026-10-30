# ==============================================================
#    DOCTOR WHO - Clases y Objetos en Python (versión gráfica)
# ==============================================================
#
#  Una CLASE es el "molde" (la plantilla).
#  Un OBJETO es una "galleta" hecha con ese molde.
#
#  - ATRIBUTOS = características del objeto (nombre, planeta...)
#  - MÉTODOS   = acciones que puede hacer (presentarse, viajar...)
#  - HERENCIA  = una clase HIJA copia todo lo de su clase PADRE
#                y además añade cosas propias.
#
#  Para que se vea "bonito" usamos:
#  - Colores (códigos especiales que entiende la consola)
#  - Recuadros dibujados con caracteres como ╔ ═ ╗ ║
#  - Dibujos hechos con letras y símbolos (arte ASCII)
#
#  No hace falta instalar nada: solo Python.
#  Para ejecutarlo:  python doctor_who.py
# ==============================================================

import os    # para limpiar la pantalla
import re    # para medir texto que lleva colores
import sys   # para configurar la consola
import time  # para hacer pausas en las animaciones

# Preparar la consola de Windows para que acepte colores y símbolos
os.system("")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ==============================================================
#  PARTE 1: HERRAMIENTAS DE DIBUJO
#  (no son de Doctor Who, solo sirven para pintar en pantalla)
# ==============================================================

class Color:
    """Guarda los códigos de colores. Es una clase usada como 'caja de pinturas'."""
    RESET = "\033[0m"      # vuelve al color normal
    NEGRITA = "\033[1m"
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CIAN = "\033[96m"
    BLANCO = "\033[97m"
    GRIS = "\033[90m"


ANCHO = 62  # ancho de todos los recuadros


def pintar(texto, color):
    """Devuelve el texto pintado de un color."""
    return color + texto + Color.RESET


def largo_visible(texto):
    """Cuenta las letras que SE VEN (sin contar los códigos de color)."""
    return len(re.sub(r"\033\[[0-9;]*m", "", texto))


def rellenar(texto, ancho):
    """Añade espacios al final hasta llegar al ancho indicado."""
    return texto + " " * max(0, ancho - largo_visible(texto))


def centrar(texto, ancho):
    """Centra un texto (aunque tenga colores) en el ancho indicado."""
    hueco = max(0, ancho - largo_visible(texto))
    izquierda = hueco // 2
    return " " * izquierda + texto + " " * (hueco - izquierda)


def limpiar():
    """Borra la pantalla."""
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input(pintar("\n   Pulsa ENTER para continuar...", Color.GRIS))


def escribir_lento(texto, color=Color.BLANCO, velocidad=0.02):
    """Escribe letra a letra, como una máquina de escribir."""
    for letra in texto:
        print(pintar(letra, color), end="", flush=True)
        time.sleep(velocidad)
    print()


def caja(lineas, color=Color.CIAN, titulo=""):
    """Dibuja un recuadro (como una 'ventana') alrededor de unas líneas."""
    interior = ANCHO - 2
    print(pintar("╔" + "═" * interior + "╗", color))
    if titulo:
        texto_titulo = pintar(titulo, Color.NEGRITA + Color.AMARILLO)
        print(pintar("║", color) + centrar(texto_titulo, interior) + pintar("║", color))
        print(pintar("╠" + "═" * interior + "╣", color))
    for linea in lineas:
        print(pintar("║", color) + " " + rellenar(linea, interior - 2) + " " + pintar("║", color))
    print(pintar("╚" + "═" * interior + "╝", color))


def barra(actual, maximo, color, ancho=20):
    """Dibuja una barra tipo 'vida' o 'carga':  ██████░░░░"""
    llenos = round(ancho * actual / maximo)
    return pintar("█" * llenos, color) + pintar("░" * (ancho - llenos), Color.GRIS)


def animacion_carga(texto, color, segundos=2):
    """Barra de progreso que se va llenando de 0% a 100%."""
    pasos = 30
    for i in range(pasos + 1):
        porcentaje = int(i * 100 / pasos)
        print(f"\r   {pintar(texto, color)} {barra(i, pasos, color, 30)} {porcentaje:3d}%", end="", flush=True)
        time.sleep(segundos / pasos)
    print()


# ==============================================================
#  PARTE 2: DIBUJOS (ARTE ASCII)
#  Cada dibujo es una lista de líneas de texto.
#  La "r" delante de las comillas evita problemas con la barra \
# ==============================================================

ARTE_TITULO = [
    r" ___   ___   ___ _____ ___  ___  __      ___  _  ___  ",
    r"|   \ / _ \ / __|_   _/ _ \| _ \ \ \    / / || |/ _ \ ",
    r"| |) | (_) | (__  | || (_) |   /  \ \/\/ /| __ | (_) |",
    r"|___/ \___/ \___| |_| \___/|_|_\   \_/\_/ |_||_|\___/ ",
]

ARTE_VORTICE = [
    r"      .  *    .        *       .     *    ",
    r"   *     .-~~~~~~~~-.      .        .     ",
    r"     .  / .-~~~~~~-. \   *     .          ",
    r"   .   | | .-~~~~-. | |      .     *      ",
    r"       | | | (@)  | | |  .       .        ",
    r"   *   | | '-~~~~-' | |     *         .   ",
    r"     .  \ '-~~~~~~-' /  .       *         ",
    r"   .     '-~~~~~~~~-'      .        .     ",
    r"      *     .     *     .      *          ",
]

# Reloj de bolsillo: representa a un Señor del Tiempo
ARTE_RELOJ = [
    r"        _O_        ",
    r"     .-'   '-.     ",
    r"    /   12    \    ",
    r"   |  9  o--3  |   ",
    r"    \    6    /    ",
    r"     '-.___.-'     ",
]

# Persona sencilla: representa a un acompañante humano
ARTE_PERSONA = [
    r"       .---.       ",
    r"      ( o o )      ",
    r"       \ - /       ",
    r"     .-'   '-.     ",
    r"    /|       |\    ",
    r"     |_______|     ",
    r"      |     |      ",
]

# Calavera de peligro: representa a un villano
ARTE_CALAVERA = [
    r"      _______      ",
    r"     /       \     ",
    r"    |  () ()  |    ",
    r"     \   ^   /     ",
    r"      |||||||      ",
    r"      '-----'      ",
]

# Ojo hipnótico: otro tipo de villano
ARTE_OJO = [
    r"     .-~~~~~-.     ",
    r"    /  .---.  \    ",
    r"   |  ( (@) )  |   ",
    r"    \  '---'  /    ",
    r"     '-~~~~~-'     ",
]

# Planeta con anillo: para los viajes
ARTE_PLANETA = [
    r"           _____           ",
    r"        .-'     '-.        ",
    r"   ----/-----------\----   ",
    r"      |   o     .   |      ",
    r"   ----\-----------/----   ",
    r"        '-._____.-'        ",
]

# Ondas de sonido: para el destornillador sónico
ARTE_ONDAS = [
    r"  [=====]=====>  )   )    )     )  ",
    r"  [=====]=====>   )   )    )     ) ",
    r"  [=====]=====>  )   )    )     )  ",
]


# ==============================================================
#  PARTE 3: LAS CLASES (los moldes)
# ==============================================================

class Personaje:
    """CLASE PADRE: lo que TODOS los personajes tienen en común."""

    # __init__ se ejecuta automáticamente al CREAR un objeto.
    # Guarda las CARACTERÍSTICAS (atributos). "self" = "este objeto".
    def __init__(self, nombre, especie, planeta, arte, color):
        self.nombre = nombre
        self.especie = especie
        self.planeta = planeta
        self.arte = arte      # el dibujo también es una característica
        self.color = color    # y el color con el que se pinta

    def tipo(self):
        return "PERSONAJE"

    def datos(self):
        """Lista de características que se muestran en la ficha."""
        return [
            ("Nombre", self.nombre),
            ("Especie", self.especie),
            ("Planeta", self.planeta),
        ]

    def presentarse(self):
        escribir_lento(f"   Hola, soy {self.nombre}, de {self.planeta}.", self.color)

    def mostrar_ficha(self):
        """Dibuja una 'tarjeta' con el dibujo y los datos del personaje."""
        lineas = [centrar(pintar(linea, self.color), ANCHO - 4) for linea in self.arte]
        lineas.append("")
        for etiqueta, valor in self.datos():
            lineas.append(pintar(f"{etiqueta:<15}", Color.GRIS) + pintar(": ", Color.GRIS) + str(valor))
        caja(lineas, self.color, titulo=f"{self.tipo()}  ·  {self.nombre.upper()}")


class Doctor(Personaje):
    """CLASE HIJA de Personaje: el Doctor."""

    MAX_REGENERACIONES = 13

    def __init__(self, nombre, regeneracion, actor):
        # super() usa el molde del padre para rellenar lo común
        super().__init__(nombre, "Señor del Tiempo", "Gallifrey", ARTE_RELOJ, Color.AZUL)
        self.regeneracion = regeneracion   # atributo propio del Doctor
        self.actor = actor                 # atributo propio del Doctor

    def tipo(self):
        return "DOCTOR"

    def datos(self):
        # Coge los datos del padre y AÑADE los suyos
        return super().datos() + [
            ("Actor", self.actor),
            ("Regeneración", f"{barra(self.regeneracion, self.MAX_REGENERACIONES, Color.AMARILLO, 13)} "
                             f"{self.regeneracion}/{self.MAX_REGENERACIONES}"),
        ]

    def usar_destornillador(self):
        print()
        for linea in ARTE_ONDAS:
            print("   " + pintar(linea, Color.VERDE))
            time.sleep(0.25)
        escribir_lento(f"   {self.nombre} usa el destornillador sónico: ¡bzzzzzzz!", Color.VERDE)

    def regenerarse(self, nuevo_actor):
        if self.regeneracion >= self.MAX_REGENERACIONES:
            escribir_lento("   No quedan más regeneraciones...", Color.ROJO)
            return
        colores = [Color.AMARILLO, Color.ROJO, Color.BLANCO, Color.AMARILLO, Color.ROJO]
        for c in colores:   # efecto de "luz" de regeneración
            print(pintar("   " + "▓▒░ R E G E N E R A C I Ó N ░▒▓".center(50), Color.NEGRITA + c))
            time.sleep(0.3)
        self.regeneracion = self.regeneracion + 1
        self.actor = nuevo_actor
        self.nombre = f"El Doctor nº {self.regeneracion}"
        escribir_lento(f"\n   ¡Ahora soy {self.nombre}! (interpretado por {self.actor})", Color.AMARILLO)


class Acompanante(Personaje):
    """CLASE HIJA de Personaje: los acompañantes humanos."""

    def __init__(self, nombre, planeta, epoca):
        super().__init__(nombre, "Humana/o", planeta, ARTE_PERSONA, Color.VERDE)
        self.epoca = epoca   # de qué año viene

    def tipo(self):
        return "ACOMPAÑANTE"

    def datos(self):
        return super().datos() + [("Época", self.epoca)]

    def viajar_con(self, doctor):
        escribir_lento(f"   {self.nombre} (del año {self.epoca}) se une a {doctor.nombre}.", self.color)


class Villano(Personaje):
    """CLASE HIJA de Personaje: los villanos."""

    def __init__(self, nombre, especie, planeta, frase, peligro, arte):
        super().__init__(nombre, especie, planeta, arte, Color.ROJO)
        self.frase = frase       # su frase típica
        self.peligro = peligro   # del 1 al 10

    def tipo(self):
        return "VILLANO"

    def datos(self):
        return super().datos() + [
            ("Frase", f"«{self.frase}»"),
            ("Peligro", f"{barra(self.peligro, 10, Color.ROJO, 10)} {self.peligro}/10"),
        ]

    def amenazar(self):
        print()
        for linea in self.arte:
            print("   " + pintar(linea, self.color))
        escribir_lento(f"\n   {self.nombre}: «{self.frase}»", Color.NEGRITA + Color.ROJO, 0.05)


class Tardis:
    """Clase que NO hereda de Personaje: la nave del Doctor."""

    def __init__(self, forma, color):
        self.forma = forma
        self.color = color
        self.pasajeros = []   # lista donde guardamos objetos Personaje
        self.viajes = []      # lista de destinos visitados

    def subir(self, personaje):
        if personaje not in self.pasajeros:
            self.pasajeros.append(personaje)

    def mostrar_ficha(self):
        nombres = ", ".join(p.nombre for p in self.pasajeros) or "nadie"
        viajes = ", ".join(self.viajes) or "ninguno todavía"
        caja([
            pintar("Forma          : ", Color.GRIS) + self.forma,
            pintar("Color          : ", Color.GRIS) + self.color,
            pintar("A bordo        : ", Color.GRIS) + nombres,
            pintar("Viajes         : ", Color.GRIS) + viajes,
        ], Color.AZUL, titulo="NAVE  ·  LA TARDIS")

    def viajar(self, destino, anio):
        print()
        animacion_carga("Viajando por el vórtice", Color.CIAN)
        print()
        for linea in ARTE_PLANETA:
            print("            " + pintar(linea, Color.MAGENTA))
        self.viajes.append(f"{destino} ({anio})")
        escribir_lento(f"\n   La TARDIS aterriza en {destino}, año {anio}.", Color.CIAN)


# ==============================================================
#  PARTE 4: CREAMOS LOS OBJETOS (usamos los moldes)
# ==============================================================

doctor = Doctor("El Décimo Doctor", 10, "David Tennant")

acompanantes = [
    Acompanante("Rose Tyler", "Tierra", 2005),
    Acompanante("Martha Jones", "Tierra", 2007),
    Acompanante("Donna Noble", "Tierra", 2008),
]

villanos = [
    Villano("Dalek", "Dalek", "Skaro", "¡EXTERMINAR!", 10, ARTE_CALAVERA),
    Villano("Cyberman", "Cyberman", "Mondas", "¡Serás actualizado!", 8, ARTE_CALAVERA),
    Villano("El Amo", "Señor del Tiempo", "Gallifrey", "¡Arrodillaos ante el Amo!", 9, ARTE_OJO),
]

tardis = Tardis("cabina de policía", "azul")
tardis.subir(doctor)

DESTINOS = [
    ("Londres", 1941),
    ("Pompeya", 79),
    ("Nueva Nueva York", 5000000023),
    ("El fin del universo", 100000000000000),
]

ACTORES_FUTUROS = ["Matt Smith", "Peter Capaldi", "Jodie Whittaker", "Ncuti Gatwa"]


# ==============================================================
#  PARTE 5: LAS PANTALLAS DEL PROGRAMA
# ==============================================================

def pantalla_inicio():
    limpiar()
    print()
    for linea in ARTE_TITULO:
        print(centrar(pintar(linea, Color.NEGRITA + Color.AZUL), ANCHO))
    print(centrar(pintar("~ Clases y Objetos en Python ~", Color.AMARILLO), ANCHO))
    print()
    for linea in ARTE_VORTICE:
        print(centrar(pintar(linea, Color.CIAN), ANCHO))
        time.sleep(0.08)
    print()
    animacion_carga("Cargando el universo   ", Color.AZUL, 1.5)
    pausa()


def elegir(opciones, titulo, color):
    """Muestra una lista numerada y devuelve el elemento elegido."""
    caja([pintar(f"[{i}]", Color.AMARILLO) + f" {texto}" for i, texto in enumerate(opciones, 1)],
         color, titulo=titulo)
    while True:
        respuesta = input(pintar("   Elige un número: ", Color.AMARILLO)).strip()
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(opciones):
            return int(respuesta) - 1
        print(pintar("   Número no válido, prueba otra vez.", Color.ROJO))


def ver_personajes():
    todos = [doctor] + acompanantes + villanos
    for personaje in todos:
        limpiar()
        personaje.mostrar_ficha()
        personaje.presentarse()
        pausa()


def viajar():
    limpiar()
    opciones = [f"{lugar}  (año {anio})" for lugar, anio in DESTINOS]
    n = elegir(opciones, "¿A DÓNDE VIAJAMOS?", Color.CIAN)
    limpiar()
    i = elegir([a.nombre for a in acompanantes], "¿QUIÉN TE ACOMPAÑA?", Color.VERDE)
    acompanante = acompanantes[i]
    acompanante.viajar_con(doctor)
    tardis.subir(acompanante)
    lugar, anio = DESTINOS[n]
    tardis.viajar(lugar, anio)
    print()
    tardis.mostrar_ficha()
    pausa()


def enfrentarse():
    limpiar()
    n = elegir([v.nombre for v in villanos], "¿CONTRA QUIÉN LUCHAMOS?", Color.ROJO)
    villano = villanos[n]
    limpiar()
    villano.mostrar_ficha()
    villano.amenazar()
    time.sleep(0.5)
    doctor.usar_destornillador()
    print()
    caja([centrar(pintar(f"¡{villano.nombre} huye derrotado!", Color.VERDE), ANCHO - 4)],
         Color.VERDE, titulo="VICTORIA")
    pausa()


def regenerar():
    limpiar()
    doctor.mostrar_ficha()
    if doctor.regeneracion < Doctor.MAX_REGENERACIONES:
        posicion = (doctor.regeneracion - 10) % len(ACTORES_FUTUROS)
        nuevo_actor = ACTORES_FUTUROS[posicion]
        print()
        doctor.regenerarse(nuevo_actor)
        print()
        doctor.mostrar_ficha()
    else:
        doctor.regenerarse("")
    pausa()


def leccion():
    """Explica en pantalla cómo están organizadas las clases."""
    limpiar()
    A, V, R, G, C = Color.AZUL, Color.VERDE, Color.ROJO, Color.GRIS, Color.CIAN
    caja([
        pintar("CLASE", Color.AMARILLO) + "  = el molde       " + pintar("(Personaje)", G),
        pintar("OBJETO", Color.AMARILLO) + " = lo que sale del molde " + pintar("(doctor, rose...)", G),
        "",
        "                " + pintar("┌──────────────┐", C),
        "                " + pintar("│  Personaje   │", C) + pintar("  <- PADRE", G),
        "                " + pintar("└──────┬───────┘", C),
        "        " + pintar("┌──────────────┼──────────────┐", G),
        "  " + pintar("┌─────┴────┐", A) + "  " + pintar("┌──────┴─────┐", V) + "  " + pintar("┌─────┴────┐", R),
        "  " + pintar("│  Doctor  │", A) + "  " + pintar("│ Acompanante│", V) + "  " + pintar("│ Villano  │", R),
        "  " + pintar("└──────────┘", A) + "  " + pintar("└────────────┘", V) + "  " + pintar("└──────────┘", R),
        pintar("                     HIJAS (heredan)", G),
        "",
        pintar("Ejemplo:", Color.AMARILLO) + " Villano no escribe presentarse(),",
        "pero el Dalek puede presentarse porque lo HEREDA.",
        "",
        pintar("Atributo", Color.AMARILLO) + " = característica  -> doctor.actor",
        pintar("Método", Color.AMARILLO) + "   = acción          -> doctor.regenerarse()",
    ], Color.MAGENTA, titulo="LECCIÓN: ¿CÓMO FUNCIONA?")
    pausa()


def menu_principal():
    while True:
        limpiar()
        for linea in ARTE_TITULO:
            print(centrar(pintar(linea, Color.AZUL), ANCHO))
        print()
        caja([
            pintar("[1]", Color.AMARILLO) + " Ver las fichas de los personajes",
            pintar("[2]", Color.AMARILLO) + " Viajar en la TARDIS",
            pintar("[3]", Color.AMARILLO) + " Enfrentarse a un villano",
            pintar("[4]", Color.AMARILLO) + " Regenerar al Doctor",
            pintar("[5]", Color.AMARILLO) + " Ver la nave (TARDIS)",
            pintar("[6]", Color.AMARILLO) + " Lección: clases y objetos",
            "",
            pintar("[0]", Color.ROJO) + " Salir",
        ], Color.CIAN, titulo="MENÚ PRINCIPAL")

        opcion = input(pintar("   ¿Qué quieres hacer? ", Color.AMARILLO)).strip()

        if opcion == "1":
            ver_personajes()
        elif opcion == "2":
            viajar()
        elif opcion == "3":
            enfrentarse()
        elif opcion == "4":
            regenerar()
        elif opcion == "5":
            limpiar()
            tardis.mostrar_ficha()
            pausa()
        elif opcion == "6":
            leccion()
        elif opcion == "0":
            limpiar()
            escribir_lento("\n   ¡Allons-y! Hasta la próxima aventura.\n", Color.AZUL, 0.04)
            break


# ==============================================================
#  PARTE 6: ARRANCAR EL PROGRAMA
#  Esta línea significa: "si ejecuto ESTE archivo, empieza aquí"
# ==============================================================
if __name__ == "__main__":
    pantalla_inicio()
    menu_principal()
