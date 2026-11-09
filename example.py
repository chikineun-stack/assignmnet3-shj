import pygame
import sys

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Multiplication Visualizer")

# Fonts (Using English-safe standard fonts)
font_main = pygame.font.SysFont("consolas", 40)
font_small = pygame.font.SysFont("consolas", 25)
font_title = pygame.font.SysFont("consolas", 35, bold=True)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 100)
CYAN = (100, 255, 255)

# Matrix Data (5x5)
N = 5
A = [[1, 2, 3, 4, 5], 
     [6, 7, 8, 9, 10], 
     [11, 12, 13, 14, 15], 
     [16, 17, 18, 19, 20], 
     [21, 22, 23, 24, 25]]

I = [[1, 0, 0, 0, 0], 
     [0, 1, 0, 0, 0], 
     [0, 0, 1, 0, 0], 
     [0, 0, 0, 1, 0], 
     [0, 0, 0, 0, 1]]

result_matrix = [[None]*N for _ in range(N)]

# Animation Variables
cur_r = 0  
cur_c = 0  
i_y_pos = 350
speed = 5

def draw_text(text, x, y, color, font_type=font_main):
    img = font_type.render(str(text), True, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Top Center Title
    draw_text("I = Identity Matrix", WIDTH // 2, 40, WHITE, font_title)

    # Right Side: Static Matrix A
    static_start_x = 850
    static_a_y = 150
    spacing_small = 60
    draw_text("[ Matrix A ]", static_start_x + 120, static_a_y - 50, WHITE, font_title)
    for r in range(N):
        for c in range(N):
            draw_text(A[r][c], static_start_x + c * spacing_small, static_a_y + r * spacing_small, WHITE, font_small)

    if cur_r < N:
        base_y = HEIGHT // 2
        a_field_start_x = 200
        spacing = 90
        
        # Draw Row Label for A Field
        draw_text(f"Row {cur_r + 1}", a_field_start_x - 100, base_y, YELLOW, font_small)

        # 1. Draw A Field
        for col in range(N):
            x_pos = a_field_start_x + col * spacing
            draw_text(A[cur_r][col], x_pos, base_y, WHITE)

        # 2. Update I Field Position
        i_y_pos -= speed
        is_overlapping = abs(i_y_pos) < 30
        
        # Immediate calculation during overlap
        if is_overlapping:
            dot_product = sum(A[cur_r][k] * I[k][cur_c] for k in range(N))
            result_matrix[cur_r][cur_c] = dot_product

        # Draw Column Label for I Field (Moves with I Field)
        draw_text(f"Col {cur_c + 1}", a_field_start_x - 100, base_y + i_y_pos, CYAN, font_small)

        # Draw I Field
        for row in range(N):
            x_pos = a_field_start_x + row * spacing
            val = I[row][cur_c]
            
            text_color = WHITE
            if is_overlapping:
                product = A[cur_r][row] * val
                if product != 0:
                    # Draw Green Circle behind the text
                    pygame.draw.circle(screen, GREEN, (x_pos, base_y + i_y_pos), 35)
                    text_color = BLACK
                else:
                    text_color = GRAY
                    
            draw_text(val, x_pos, base_y + i_y_pos, text_color)

        # 3. I Field has completely passed
        if i_y_pos < -350:
            cur_c += 1
            if cur_c >= N:
                cur_c = 0
                cur_r += 1 
            i_y_pos = 350 

    # 4. Right Side: Result Matrix
    res_start_y = 500
    draw_text("[ Result Matrix ]", static_start_x + 120, res_start_y - 50, GREEN, font_title)
    
    for r in range(N):
        for c in range(N):
            val = result_matrix[r][c]
            text_val = val if val is not None else "-"
            
            # Highlight recently added value
            color = GREEN if (val is not None and r == cur_r and c == cur_c) else WHITE
            if cur_r >= N and val is not None:
                color = WHITE # All finished
                
            draw_text(text_val, static_start_x + c * spacing_small, res_start_y + r * spacing_small, color, font_small)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()