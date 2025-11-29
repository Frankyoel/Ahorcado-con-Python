import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import os

class AhorcadoGame:
    def __init__(self):
        self.palabras = ['PYTHON', 'OPENGL', 'PROGRAMA', 'JUEGO', 'GRAFICO', 
                        'COMPUTADORA', 'TECLADO', 'PANTALLA', 'CODIGO', 'DESARROLLO']
        self.palabra_actual = random.choice(self.palabras)
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.max_intentos = 6
        self.juego_terminado = False
        self.ganado = False
        self.muneco_rotacion_x = 0  # Rotación vertical 
        self.muneco_rotacion_y = 0  # Rotación horizontal 
        self.muneco_auto_rotacion = 0  # Rotación automática continua
        
    def adivinar_letra(self, letra):
        if self.juego_terminado or letra in self.letras_adivinadas:
            return
        
        self.letras_adivinadas.add(letra)
        
        if letra not in self.palabra_actual:
            self.letras_incorrectas.add(letra)
            
        if len(self.letras_incorrectas) >= self.max_intentos:
            self.juego_terminado = True
            self.ganado = False
        elif all(letra in self.letras_adivinadas for letra in self.palabra_actual):
            self.juego_terminado = True
            self.ganado = True
    
    def reiniciar(self):
        self.palabra_actual = random.choice(self.palabras)
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.juego_terminado = False
        self.ganado = False

def init_gl():
    glClearColor(0.95, 0.95, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glLineWidth(2.0)
    glEnable(GL_DEPTH_TEST)

def cargar_textura(ruta):
    """Carga una imagen y la convierte en textura OpenGL"""
    try:
        imagen = pygame.image.load(ruta)
        ancho = imagen.get_width()
        alto = imagen.get_height()
        
        # Convertir imagen a string buffer
        datos_imagen = pygame.image.tostring(imagen, "RGBA", 1)
        
        # Generar ID de textura
        textura_id = glGenTextures(1)
        
        # Vincular y configurar textura
        glBindTexture(GL_TEXTURE_2D, textura_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        # Cargar datos de la imagen
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0, GL_RGBA, GL_UNSIGNED_BYTE, datos_imagen)
        
        return textura_id
    except Exception as e:
        print(f"Error cargando textura: {e}")
        return None

def dibujar_fondo(textura_id):
    """Dibuja el fondo usando la textura cargada"""
    if not textura_id:
        return
    
    # Deshabilitar depth test para el fondo
    glDisable(GL_DEPTH_TEST)  
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Habilitar texturas
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(1, 1, 1)
    
    # Dibujar el fondo
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(800, 0)
    glTexCoord2f(1, 1); glVertex2f(800, 600)
    glTexCoord2f(0, 1); glVertex2f(0, 600)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)
    
    # Restaurar estado 2D
    glPopMatrix() 
    glMatrixMode(GL_PROJECTION)
    glPopMatrix() 
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def dibujar_esfera_3d(radio=0.5, rodajas=20, pilas=20):
    """Dibuja una esfera 3D"""
    
    for i in range(pilas):
        lat0 = math.pi * (-0.5 + float(i) / pilas)
        z0 = math.sin(lat0) * radio
        zr0 = math.cos(lat0) * radio

        lat1 = math.pi * (-0.5 + float(i + 1) / pilas)
        z1 = math.sin(lat1) * radio
        zr1 = math.cos(lat1) * radio

        glBegin(GL_QUAD_STRIP)
        for j in range(rodajas + 1):
            lng = 2 * math.pi * float(j) / rodajas
            x = math.cos(lng)
            y = math.sin(lng)

            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def dibujar_cubo_3d(tamano=1.0):
    """Dibuja un cubo 3D"""
    s = tamano / 2.0
    glBegin(GL_QUADS)
    
    # Frente
    glVertex3f(-s, -s, s)
    glVertex3f(s, -s, s)
    glVertex3f(s, s, s)
    glVertex3f(-s, s, s)
    
    # Atrás
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, s, -s)
    glVertex3f(s, s, -s)
    glVertex3f(s, -s, -s)
    
    # Arriba
    glVertex3f(-s, s, -s)
    glVertex3f(-s, s, s)
    glVertex3f(s, s, s)
    glVertex3f(s, s, -s)
    
    # Abajo
    glVertex3f(-s, -s, -s)
    glVertex3f(s, -s, -s)
    glVertex3f(s, -s, s)
    glVertex3f(-s, -s, s)
    
    # Derecha
    glVertex3f(s, -s, -s)
    glVertex3f(s, s, -s)
    glVertex3f(s, s, s)
    glVertex3f(s, -s, s)
    
    # Izquierda
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, -s, s)
    glVertex3f(-s, s, s)
    glVertex3f(-s, s, -s)

    glEnd()

def dibujar_linea(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def dibujar_horca_3d(intentos_incorrectos):
    """Dibuja la estructura de la horca en 3D (base, poste vertical, horizontal y soga)"""
    # Color marrón para la madera
    glColor3f(0.4, 0.25, 0.1)
    
    # Base horizontal
    glPushMatrix()
    glTranslatef(0.0, -1.5, 0.0)
    glScalef(3.0, 0.1, 0.5)
    dibujar_cubo_3d()
    glPopMatrix()
    
    # Poste vertical
    glPushMatrix()
    glTranslatef(-0.8, 0.0, 0.0)
    glScalef(0.15, 3.0, 0.15)
    dibujar_cubo_3d()
    glPopMatrix()
    
    # Poste horizontal (viga superior)
    glPushMatrix()
    glTranslatef(-0.1, 1.5, 0.0)
    glScalef(1.5, 0.1, 0.15)
    dibujar_cubo_3d()
    glPopMatrix()
    
    # Soga - color beige/cuerda
    if intentos_incorrectos >= 6:
        glColor3f(0.8, 0.7, 0.5)
        glPushMatrix()
        glTranslatef(0.6, 1.225, 0.0)
        glScalef(0.08, 0.45, 0.08)
        dibujar_cubo_3d()
        glPopMatrix()

def dibujar_persona_3d(intentos_incorrectos):
    """Dibuja una persona 3D con cubos y esferas de colores vibrantes"""
    
    if intentos_incorrectos >= 1:
        # Dibujar cabeza 
        glPushMatrix()
        glColor3f(1.0, 0.8, 0.7)  # Rosa piel
        glTranslatef(0.0, 0.75, 0.0)
        dibujar_esfera_3d(0.25)
        glPopMatrix()
    
    if intentos_incorrectos >= 2:
        # Dibujar cuerpo 
        glPushMatrix()
        glColor3f(0.2, 0.5, 1.0)  # Azul
        glScalef(0.30, 1.0, 0.25)
        dibujar_cubo_3d()
        glPopMatrix()
    
    if intentos_incorrectos >= 3:
        # Dibujar brazo izquierdo 
        glColor3f(0.2, 0.8, 0.3)  # Verde
        glPushMatrix()
        glTranslatef(-0.22, 0.25, 0.0)
        glRotatef(-15, 0, 0, 1)
        glScalef(0.15, 0.6, 0.15)
        dibujar_cubo_3d()
        glPopMatrix()
    
    if intentos_incorrectos >= 4:
        # Dibujar brazo derecho 
        glColor3f(0.2, 0.8, 0.3)  # Verde
        glPushMatrix()
        glTranslatef(0.22, 0.25, 0.0)
        glRotatef(15, 0, 0, 1)
        glScalef(0.15, 0.6, 0.15)
        dibujar_cubo_3d()
        glPopMatrix()
    
    if intentos_incorrectos >= 5:
        # Dibujar AMBAS piernas 
        glColor3f(1.0, 0.5, 0.0)  # Naranja
        
        # Pierna izquierda
        glPushMatrix()
        glTranslatef(-0.10, -0.75, 0.0)
        glScalef(0.15, 0.5, 0.15)
        dibujar_cubo_3d()
        glPopMatrix()
        
        # Pierna derecha
        glPushMatrix()
        glTranslatef(0.10, -0.75, 0.0)
        glScalef(0.15, 0.5, 0.15)
        dibujar_cubo_3d()
        glPopMatrix()

def dibujar_ahorcado_3d(intentos_incorrectos, rotacion_x=0, rotacion_y=0, auto_rotacion=0):
    """Dibuja el muñeco del ahorcado con su estructura completa en 3D del lado izquierdo"""
    # Guardar estado 2D
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)
    
    # Guardar estado 3D
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Configurar cámara 3D 
    gluLookAt(1.0, 0.5, 4.5, 1.0, 0, 0, 0, 1, 0)
    
    # Aplicar rotaciones
    glRotatef(rotacion_x, 1, 0, 0)
    glRotatef(rotacion_y, 0, 1, 0)
    
    # Escalar todo el conjunto
    glScalef(0.6, 0.6, 0.6)
    
    # Habilitar depth test
    glEnable(GL_DEPTH_TEST)
    glClear(GL_DEPTH_BUFFER_BIT)
    
    # Dibujar la estructura de la horca
    dibujar_horca_3d(intentos_incorrectos)
    
    # Dibujar la persona 3D colgando de la soga con rotación automática
    glPushMatrix()
    glTranslatef(0.6, 0.0, 0.0)  # Posicionar al muñeco en la soga
    glRotatef(auto_rotacion, 0, 1, 0)  # Rotación automática en el eje Y
    dibujar_persona_3d(intentos_incorrectos)
    glPopMatrix()
    
    # Deshabilitar depth test
    glDisable(GL_DEPTH_TEST)
    
    # Restaurar estado 2D
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def dibujar_texto(x, y, texto, tamano=24, color=(255, 255, 255)):
    """Dibuja texto usando Pygame en lugar de GLUT"""
    
    fuente = pygame.font.Font(None, tamano)
    superficie_texto = fuente.render(texto, True, color)
    datos_texto = pygame.image.tostring(superficie_texto, "RGBA", True)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glRasterPos2f(x, y)
    glDrawPixels(superficie_texto.get_width(), superficie_texto.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, datos_texto)
    
    glDisable(GL_BLEND)

def dibujar_palabra(juego):
    x_inicio = 400
    y_pos = 350
    espaciado = 40
    
    glColor3f(0.0, 0.0, 0.0)
    for i, letra in enumerate(juego.palabra_actual):
        x = x_inicio + i * espaciado
        
        # Línea base
        dibujar_linea(x, y_pos - 10, x + 30, y_pos - 10)
        
        # Letra si fue adivinada
        if letra in juego.letras_adivinadas:
            dibujar_texto(x + 5, y_pos, letra, 32)

def dibujar_letras_usadas(juego):

    glColor3f(0.5, 0.0, 0.0)
    dibujar_texto(400, 280, "INCORRECTAS:", 20)
    
    x_pos = 400
    y_pos = 250

    # Letras incorrectas
    for letra in sorted(juego.letras_incorrectas):
        dibujar_texto(x_pos, y_pos, letra, 24)
        x_pos += 30

def dibujar_teclado(juego, raton_x, raton_y):
    # Dibuja un teclado con botones para las letras
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    x_inicio = 100
    y_inicio = 120
    ancho_btn = 40
    alto_btn = 40
    espaciado = 5
    por_fila = 13
    
    for i, letra in enumerate(letras):
        fila = i // por_fila
        columna = i % por_fila
        
        x = x_inicio + columna * (ancho_btn + espaciado)
        y = y_inicio - fila * (alto_btn + espaciado)
        
        # Color del botón
        if letra in juego.letras_adivinadas:
            if letra in juego.letras_incorrectas:
                glColor3f(0.8, 0.2, 0.2)
            else:
                glColor3f(0.2, 0.8, 0.2)
        elif (x <= raton_x <= x + ancho_btn and 
              y - alto_btn <= raton_y <= y):
            glColor3f(0.7, 0.7, 0.9)
        else:
            glColor3f(0.5, 0.5, 0.7)
        
        # Dibujar botón
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + ancho_btn, y)
        glVertex2f(x + ancho_btn, y - alto_btn)
        glVertex2f(x, y - alto_btn)
        glEnd()
        
        # Borde
        glColor3f(0.2, 0.2, 0.3)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + ancho_btn, y)
        glVertex2f(x + ancho_btn, y - alto_btn)
        glVertex2f(x, y - alto_btn)
        glEnd()
        
        # Letra
        glColor3f(1.0, 1.0, 1.0)
        dibujar_texto(x + 10, y - 28, letra, 24)

def obtener_letra_clic(raton_x, raton_y):
    # Obtiene la letra
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    x_inicio = 100
    y_inicio = 120
    ancho_btn = 40
    alto_btn = 40
    espaciado = 5
    por_fila = 13
    
    for i, letra in enumerate(letras):
        fila = i // por_fila
        columna = i % por_fila
        
        x = x_inicio + columna * (ancho_btn + espaciado)
        y = y_inicio - fila * (alto_btn + espaciado)
        
        if (x <= raton_x <= x + ancho_btn and 
            y - alto_btn <= raton_y <= y):
            return letra
    return None

def dibujar_fin_juego(juego):
    # Dibuja el mensaje de fin de juego
    if juego.ganado:
        glColor3f(0.0, 0.6, 0.0)
        dibujar_texto(400, 450, "¡GANASTE!", 48)
    else:
        glColor3f(0.8, 0.0, 0.0)
        dibujar_texto(400, 450, "¡PERDISTE!", 48)
        glColor3f(0.0, 0.0, 0.0)
        dibujar_texto(400, 420, f"Palabra: {juego.palabra_actual}", 24)
    
    glColor3f(0.0, 0.0, 0.5)
    dibujar_texto(350, 200, "Presiona R para reiniciar", 20)

def main():

    pygame.init()
    pantalla = (800, 600)
    pygame.display.set_mode(pantalla, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Ahorcado - OpenGL 3D")
    
    init_gl()
    
    # Cargar fondo
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_fondo = os.path.join(base_dir, "images", "fondo.png")
    textura_fondo = cargar_textura(ruta_fondo)
    
    juego = AhorcadoGame()
    reloj = pygame.time.Clock()
    
    ejecutando = True

    # Bucle principal
    while ejecutando:
        raton_x, raton_y = pygame.mouse.get_pos()
        raton_y = pantalla[1] - raton_y
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if not juego.juego_terminado:
                    letra = obtener_letra_clic(raton_x, raton_y)
                    if letra:
                        juego.adivinar_letra(letra)
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r and juego.juego_terminado:
                    juego.reiniciar()
                elif evento.key == pygame.K_UP:
                    juego.muneco_rotacion_x = min(juego.muneco_rotacion_x + 5, 45)
                elif evento.key == pygame.K_DOWN:
                    juego.muneco_rotacion_x = max(juego.muneco_rotacion_x - 5, -45)
                elif evento.key == pygame.K_LEFT:
                    juego.muneco_rotacion_y = (juego.muneco_rotacion_y - 5) % 360
                elif evento.key == pygame.K_RIGHT:
                    juego.muneco_rotacion_y = (juego.muneco_rotacion_y + 5) % 360
                elif evento.key >= pygame.K_a and evento.key <= pygame.K_z and not juego.juego_terminado:
                    letra = chr(evento.key).upper()
                    juego.adivinar_letra(letra)
        
        # Rotación del muñeco
        juego.muneco_auto_rotacion = (juego.muneco_auto_rotacion + 1) % 360
        
        # Limpieza de la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Dibujar fondo primero
        dibujar_fondo(textura_fondo)
        
        # Dibujar elementos del juego
        dibujar_ahorcado_3d(len(juego.letras_incorrectas), juego.muneco_rotacion_x, juego.muneco_rotacion_y, juego.muneco_auto_rotacion)
        
        # Restaurar proyección 2D después de dibujar 3D
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 600)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Dibujar elementos del juego
        dibujar_palabra(juego)
        dibujar_letras_usadas(juego)
        dibujar_teclado(juego, raton_x, raton_y)
        
        # Título
        glColor3f(0.2, 0.2, 0.5)
        dibujar_texto(300, 550, "JUEGO DEL AHORCADO", 36)
        
        # Contador de intentos
        glColor3f(0.0, 0.0, 0.0)
        dibujar_texto(400, 180, f"Intentos: {len(juego.letras_incorrectas)}/{juego.max_intentos}", 20)
        
        if juego.juego_terminado:
            dibujar_fin_juego(juego)
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()