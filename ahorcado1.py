import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

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

def draw_circle(x, y, r, filled=False):
    segments = 50
    if filled:
        glBegin(GL_POLYGON)
    else:
        glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        dx = r * math.cos(theta)
        dy = r * math.sin(theta)
        glVertex2f(x + dx, y + dy)
    glEnd()

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_ahorcado(intentos_incorrectos):
    glColor3f(0.3, 0.2, 0.1)
    
    # Base
    draw_line(100, 150, 250, 150)
    # Poste vertical
    draw_line(150, 150, 150, 450)
    # Poste horizontal
    draw_line(150, 450, 300, 450)
    # Cuerda
    draw_line(300, 450, 300, 400)
    
    glColor3f(0.0, 0.0, 0.0)
    
    # Partes del cuerpo según intentos incorrectos
    if intentos_incorrectos >= 1:
        # Cabeza
        draw_circle(300, 370, 30)
    
    if intentos_incorrectos >= 2:
        # Cuerpo
        draw_line(300, 340, 300, 260)
    
    if intentos_incorrectos >= 3:
        # Brazo izquierdo
        draw_line(300, 320, 260, 280)
    
    if intentos_incorrectos >= 4:
        # Brazo derecho
        draw_line(300, 320, 340, 280)
    
    if intentos_incorrectos >= 5:
        # Pierna izquierda
        draw_line(300, 260, 270, 200)
    
    if intentos_incorrectos >= 6:
        # Pierna derecha
        draw_line(300, 260, 330, 200)

def draw_text(x, y, text, size=24):
    """Dibuja texto usando Pygame en lugar de GLUT"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glRasterPos2f(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    glDisable(GL_BLEND)

def draw_palabra(game):
    x_start = 400
    y_pos = 350
    spacing = 40
    
    glColor3f(0.0, 0.0, 0.0)
    for i, letra in enumerate(game.palabra_actual):
        x = x_start + i * spacing
        
        # Línea base
        draw_line(x, y_pos - 10, x + 30, y_pos - 10)
        
        # Letra si fue adivinada
        if letra in game.letras_adivinadas:
            draw_text(x + 5, y_pos, letra, 32)

def draw_letras_usadas(game):
    glColor3f(0.5, 0.0, 0.0)
    draw_text(400, 280, "INCORRECTAS:", 20)
    
    x_pos = 400
    y_pos = 250
    for letra in sorted(game.letras_incorrectas):
        draw_text(x_pos, y_pos, letra, 24)
        x_pos += 30

def draw_teclado(game, mouse_x, mouse_y):
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    x_start = 100
    y_start = 120
    btn_width = 40
    btn_height = 40
    spacing = 5
    por_fila = 13
    
    for i, letra in enumerate(letras):
        fila = i // por_fila
        columna = i % por_fila
        
        x = x_start + columna * (btn_width + spacing)
        y = y_start - fila * (btn_height + spacing)
        
        # Color del botón
        if letra in game.letras_adivinadas:
            if letra in game.letras_incorrectas:
                glColor3f(0.8, 0.2, 0.2)
            else:
                glColor3f(0.2, 0.8, 0.2)
        elif (x <= mouse_x <= x + btn_width and 
              y - btn_height <= mouse_y <= y):
            glColor3f(0.7, 0.7, 0.9)
        else:
            glColor3f(0.5, 0.5, 0.7)
        
        # Dibujar botón
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + btn_width, y)
        glVertex2f(x + btn_width, y - btn_height)
        glVertex2f(x, y - btn_height)
        glEnd()
        
        # Borde
        glColor3f(0.2, 0.2, 0.3)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + btn_width, y)
        glVertex2f(x + btn_width, y - btn_height)
        glVertex2f(x, y - btn_height)
        glEnd()
        
        # Letra
        glColor3f(1.0, 1.0, 1.0)
        draw_text(x + 10, y - 28, letra, 24)

def get_clicked_letter(mouse_x, mouse_y):
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    x_start = 100
    y_start = 120
    btn_width = 40
    btn_height = 40
    spacing = 5
    por_fila = 13
    
    for i, letra in enumerate(letras):
        fila = i // por_fila
        columna = i % por_fila
        
        x = x_start + columna * (btn_width + spacing)
        y = y_start - fila * (btn_height + spacing)
        
        if (x <= mouse_x <= x + btn_width and 
            y - btn_height <= mouse_y <= y):
            return letra
    return None

def draw_game_over(game):
    if game.ganado:
        glColor3f(0.0, 0.6, 0.0)
        draw_text(400, 450, "¡GANASTE!", 48)
    else:
        glColor3f(0.8, 0.0, 0.0)
        draw_text(400, 450, "¡PERDISTE!", 48)
        glColor3f(0.0, 0.0, 0.0)
        draw_text(400, 420, f"Palabra: {game.palabra_actual}", 24)
    
    glColor3f(0.0, 0.0, 0.5)
    draw_text(350, 200, "Presiona R para reiniciar", 20)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Ahorcado - OpenGL")
    
    init_gl()
    game = AhorcadoGame()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Invertir Y para OpenGL
        mouse_y = display[1] - mouse_y
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game.juego_terminado:
                    letra = get_clicked_letter(mouse_x, mouse_y)
                    if letra:
                        game.adivinar_letra(letra)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reiniciar()
                elif event.key >= pygame.K_a and event.key <= pygame.K_z and not game.juego_terminado:
                    letra = chr(event.key).upper()
                    game.adivinar_letra(letra)
        
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        # Dibujar elementos del juego
        draw_ahorcado(len(game.letras_incorrectas))
        draw_palabra(game)
        draw_letras_usadas(game)
        draw_teclado(game, mouse_x, mouse_y)
        
        # Título
        glColor3f(0.2, 0.2, 0.5)
        draw_text(300, 550, "JUEGO DEL AHORCADO", 36)
        
        # Contador de intentos
        glColor3f(0.0, 0.0, 0.0)
        draw_text(400, 180, f"Intentos: {len(game.letras_incorrectas)}/{game.max_intentos}", 20)
        
        if game.juego_terminado:
            draw_game_over(game)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()