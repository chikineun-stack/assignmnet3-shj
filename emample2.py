import pygame
import sys
import math

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Multiplication Visualizer - Math Metaphor")

# Fonts
font_main = pygame.font.SysFont("consolas", 40)
font_small = pygame.font.SysFont("consolas", 25)
font_title = pygame.font.SysFont("consolas", 35, bold=True)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 100)
CYAN = (100, 255, 255)
GREEN = (50, 255, 50)

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

# Coordinates
base_y = HEIGHT // 2
a_field_start_x = 200
spacing = 90
static_start_x = 850
res_start_y = 500
spacing_small = 60

# 3번째 원소(인덱스 2)의 위치 계산
center_x = a_field_start_x + 2 * spacing
merge_y = base_y - 80  # 3번째 원소 위쪽으로 병합될 y좌표

# Animation State Variables
cur_r = 0  
cur_c = 0  
phase = "RISE"
speed = 8

i_elements = []

def init_i_elements():
    global i_elements, phase
    i_elements = []
    for k in range(N):
        i_elements.append({
            'x': a_field_start_x + k * spacing,
            'y': base_y + 350,
            'val': I[k][cur_c],
            'product': A[cur_r][k] * I[k][cur_c],
            'hit': False
        })
    phase = "RISE"

init_i_elements()

def draw_text(text, x, y, color, font_type=font_main):
    img = font_type.render(str(text), True, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)

clock = pygame.time.Clock()
running = True

merged_obj = {'x': 0, 'y': 0, 'val': 0}

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Title & Static A Matrix
    draw_text("I = Identity Matrix", WIDTH // 2, 40, WHITE, font_title)
    static_a_y = 150
    draw_text("[ Matrix A ]", static_start_x + 120, static_a_y - 50, WHITE, font_title)
    for r in range(N):
        for c in range(N):
            draw_text(A[r][c], static_start_x + c * spacing_small, static_a_y + r * spacing_small, WHITE, font_small)

    if cur_r < N:
        draw_text(f"Row {cur_r + 1}", a_field_start_x - 100, base_y, YELLOW, font_small)
        
        if phase != "FLY":
            min_y = min([el['y'] for el in i_elements]) if i_elements else base_y
            draw_text(f"Col {cur_c + 1}", a_field_start_x - 100, min_y, CYAN, font_small)

        # Draw A Field (Background)
        for col in range(N):
            x_pos = a_field_start_x + col * spacing
            draw_text(A[cur_r][col], x_pos, base_y, WHITE)

        # STATE MACHINE LOGIC
        if phase == "RISE":
            all_hit = True
            for el in i_elements:
                if el['y'] > base_y:
                    el['y'] -= speed
                    all_hit = False
                else:
                    el['y'] = base_y
                    if not el['hit']:
                        el['hit'] = True
                        # 접촉 즉시 값을 곱의 결과로 변경 (초록 원 제거)
                        el['val'] = el['product']
                            
                # 곱이 0이면 회색, 아니면 흰색 
                text_color = WHITE if el['val'] != 0 else GRAY
                draw_text(el['val'], el['x'], el['y'], text_color)
                    
            if all_hit:
                phase = "MERGE"
                
        elif phase == "MERGE":
            all_merged = True
            
            for el in i_elements:
                # 3번째 원소 위쪽(center_x, merge_y)을 향해 이동
                dx = center_x - el['x']
                dy = merge_y - el['y']
                dist = math.hypot(dx, dy)
                
                if dist > speed:
                    el['x'] += (dx / dist) * speed
                    el['y'] += (dy / dist) * speed
                    all_merged = False
                else:
                    el['x'] = center_x
                    el['y'] = merge_y
                
                text_color = WHITE if el['val'] != 0 else GRAY
                draw_text(el['val'], el['x'], el['y'], text_color)
                    
            if all_merged:
                # 하나로 뭉칠 때 덧셈 수행 (노란색 텍스트로 합쳐짐을 강조)
                dot_product = sum(A[cur_r][k] * I[k][cur_c] for k in range(N))
                merged_obj = {'x': center_x, 'y': merge_y, 'val': dot_product}
                phase = "FLY"
                
        elif phase == "FLY":
            target_x = static_start_x + cur_c * spacing_small
            target_y = res_start_y + cur_r * spacing_small
            
            dx = target_x - merged_obj['x']
            dy = target_y - merged_obj['y']
            dist = math.hypot(dx, dy)
            fly_speed = 15
            
            if dist < fly_speed:
                result_matrix[cur_r][cur_c] = merged_obj['val']
                cur_c += 1
                if cur_c >= N:
                    cur_c = 0
                    cur_r += 1
                if cur_r < N:
                    init_i_elements() 
            else:
                merged_obj['x'] += (dx / dist) * fly_speed
                merged_obj['y'] += (dy / dist) * fly_speed
                
            draw_text(merged_obj['val'], int(merged_obj['x']), int(merged_obj['y']), YELLOW)

    # Result Matrix
    draw_text("[ Result Matrix ]", static_start_x + 120, res_start_y - 50, GREEN, font_title)
    
    for r in range(N):
        for c in range(N):
            val = result_matrix[r][c]
            text_val = val if val is not None else "-"
            color = GREEN if (val is not None and r == cur_r and c == cur_c - 1) else WHITE
            if cur_r >= N and val is not None:
                color = WHITE 
            draw_text(text_val, static_start_x + c * spacing_small, res_start_y + r * spacing_small, color, font_small)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()