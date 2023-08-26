import pygame
import random

# 初始化游戏
pygame.init()

# 设置游戏窗口尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("俄罗斯方块")

# 定义方块大小和颜色
block_size = 30
block_colors = [
    (0, 0, 0),  # 黑色，表示空方格
    (255, 0, 0),  # 红色
    (0, 255, 0),  # 绿色
    (0, 0, 255),  # 蓝色
    (255, 255, 0),  # 黄色
    (255, 165, 0),  # 橙色
    (0, 255, 255),  # 青色
    (128, 0, 128)  # 紫色
]

# 定义方块的形状
tetrominoes = [
    [[1, 1, 1, 1]],  # I型方块
    [[1, 1], [1, 1]],  # O型方块
    [[1, 1, 0], [0, 1, 1]],  # Z型方块
    [[0, 1, 1], [1, 1, 0]],  # S型方块
    [[1, 1, 1], [0, 1, 0]],  # T型方块
    [[1, 1, 1], [0, 0, 1]],  # L型方块
    [[1, 1, 1], [1, 0, 0]]  # J型方块
]


def draw_grid():
    for x in range(0, screen_width, block_size):
        pygame.draw.line(screen, (128, 128, 128), (x, 0), (x, screen_height))
    for y in range(0, screen_height, block_size):
        pygame.draw.line(screen, (128, 128, 128), (0, y), (screen_width, y))


def draw_tetromino(tetromino, x, y, color):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col] == 1:
                pygame.draw.rect(screen, color, (x + col * block_size, y + row * block_size, block_size, block_size))


def is_collision(tetromino, x, y, board):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col] == 1:
                if y + row >= len(board) or x + col < 0 or x + col >= len(board[0]) or board[y + row][x + col] != 0:
                    return True
    return False


def merge_tetromino(tetromino, x, y, board):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[row])):
            if tetromino[row][col] == 1:
                board[y + row][x + col] = tetromino[row][col]


def check_full_row(board):
    full_rows = []
    for row in range(len(board)):
        if all(block != 0 for block in board[row]):
            full_rows.append(row)
    return full_rows


def remove_full_rows(board, rows):
    for row in rows:
        board.pop(row)
        board.insert(0, [0] * 10)


def game_over_animation():
    for i in range(10):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 60)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(300)


def run_game():
    clock = pygame.time.Clock()

    # 初始化游戏状态
    board = [[0] * 10 for _ in range(20)]
    current_tetromino = random.choice(tetrominoes)
    current_tetromino_color = random.randint(1, len(block_colors) - 1)
    current_x = 3
    current_y = 0
    score = 0

    # 游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not is_collision(current_tetromino, current_x - 1, current_y, board):
                        current_x -= 1
                if event.key == pygame.K_RIGHT:
                    if not is_collision(current_tetromino, current_x + 1, current_y, board):
                        current_x += 1
                if event.key == pygame.K_DOWN:
                    if not is_collision(current_tetromino, current_x, current_y + 1, board):
                        current_y += 1
                if event.key == pygame.K_UP:
                    rotated_tetromino = list(zip(*reversed(current_tetromino)))
                    if not is_collision(rotated_tetromino, current_x, current_y, board):
                        current_tetromino = rotated_tetromino

        if not is_collision(current_tetromino, current_x, current_y + 1, board):
            current_y += 1
        else:
            merge_tetromino(current_tetromino, current_x, current_y, board)
            full_rows = check_full_row(board)
            if full_rows:
                remove_full_rows(board, full_rows)
                score += len(full_rows) * 10

            current_tetromino = random.choice(tetrominoes)
            current_tetromino_color = random.randint(1, len(block_colors) - 1)
            current_x = 3
            current_y = 0

            if is_collision(current_tetromino, current_x, current_y, board):
                game_over_animation()
                return

        screen.fill((0, 0, 0))
        draw_grid()

        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] != 0:
                    pygame.draw.rect(screen, block_colors[board[row][col]], (col * block_size, row * block_size, block_size, block_size))

        draw_tetromino(current_tetromino, current_x * block_size, current_y * block_size, block_colors[current_tetromino_color])

        font = pygame.font.Font(None, 40)
        score_text = font.render("分数: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        pygame.display.update()
        clock.tick(10)


# 运行游戏
run_game()