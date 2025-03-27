import pygame
from machine import CandyMachine

pygame.init()

WIDTH, HEIGHT = 850, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Vending Machine")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 100)
RED = (200, 50, 50)

font = pygame.font.Font(None, 36)

machine = CandyMachine()
purchased_candy = None
change = 0

buttons = {
    "R$1": pygame.Rect(450, 50, 80, 50),
    "R$2": pygame.Rect(550, 50, 80, 50),
    "R$5": pygame.Rect(650, 50, 80, 50),
    "A": pygame.Rect(450, 180, 50, 50),
    "B": pygame.Rect(550, 180, 50, 50),
    "C": pygame.Rect(650, 180, 50, 50),
}

running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for key, rect in buttons.items():
                if rect.collidepoint(x, y):
                    if key in ["R$1", "R$2", "R$5"]:
                        machine.insert_money(int(key[2:]))
                    elif key in machine.candies:
                        machine.select_candy(key)
                        purchased_candy = key if machine.current_state == "Dispensing" else None
                        change = machine.balance if machine.current_state == "Returning Change" else 0
                        if machine.current_state == "Waiting":
                            purchased_candy = None
                            change = 0
    
    pygame.draw.rect(screen, BLACK, (0, 0, 400, 400), 3)
    text = font.render("Candy Machine", True, BLACK)
    screen.blit(text, (150, 60))
    
    for key, rect in buttons.items():
        pygame.draw.rect(screen, BLUE if key in ["A", "B", "C"] and machine.balance >= machine.candies[key]["price"] else GREEN, rect)
        text = font.render(key, True, WHITE)
        screen.blit(text, (rect.x + 15, rect.y + 10))
    
    # foco em front + animcao
    # logica ok

    balanceText = font.render(f"Balance: R$ {machine.balance}", True, BLACK)
    screen.blit(balanceText, (450, 375))

    candyTypeLabel = font.render(f"Tipos de doce:", True, BLACK)
    screen.blit(candyTypeLabel, (450, 150))

    validMoneyLabel = font.render(f"Valores válidos:", True, BLACK)
    screen.blit(validMoneyLabel, (450, 20))

    if machine.returnChangeBalance != 0:
        returnChange = font.render(f"Troco: R$ {machine.returnChangeBalance}", True, BLACK)
        screen.blit(returnChange, (650, 375))
    
    if purchased_candy:
        candy_text = font.render(f"Purchased: Candy {purchased_candy}", True, RED)
        screen.blit(candy_text, (450, 180))
        change_text = font.render(f"Change: R$ {change}", True, BLACK)
        screen.blit(change_text, (450, 210))
    
    pygame.display.flip()

pygame.quit()
