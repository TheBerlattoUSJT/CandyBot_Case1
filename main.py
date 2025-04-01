import pygame
from machine import CandyMachine

pygame.init()

WIDTH, HEIGHT = 800, 700 # Ajustando a janela para o tamanho da imagem
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Vending Machine")

# Carregando imagem da máquina
machine_image = pygame.image.load("30751.jpg")
machine_image = pygame.transform.scale(machine_image, (WIDTH, HEIGHT))

# Ajustando cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 100)
RED = (200, 50, 50)

font = pygame.font.Font(None, 24)

machine = CandyMachine()
purchased_candy = None
change = 0
drop_animation = None #TODO: Implementar animação de queda de doce

# Criando botões na área preta da máquina
buttons = {
    "R$1": pygame.Rect(675, 150, 100, 40),
    "R$2": pygame.Rect(675, 200, 100, 40),
    "R$5": pygame.Rect(675, 250, 100, 40),
    "A": pygame.Rect(675, 350, 50, 50),
    "B": pygame.Rect(730, 350, 50, 50),
    "C": pygame.Rect(700, 410, 50, 50)
}


running = True
while running:
    screen.fill(WHITE)
    screen.blit(machine_image, (0, 0))  # Definindo a imagem de fundo
    
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
                        if machine.current_state == "Dispensing":
                            purchased_candy = key
                            drop_animation = [350, 100] # Posição inicial do doce caindo
                        change = machine.balance if machine.current_state == "Returning Change" else 0
                        if machine.current_state == "Waiting":
                            purchased_candy = None
                            change = 0

    # Exibir saldo
    balanceText = font.render(f"Saldo: R$ {machine.balance}", True, BLACK)
    screen.blit(balanceText, (500, 600))

    # Exibindo valores válidos
    validMoneyLabel1 = font.render("Valores", True, WHITE)
    validMoneyLabel2 = font.render("válidos:", True, WHITE)

    # Obtendo as larguras dos textos para centralizar da melhor forma
    text_width1, text_height1 = validMoneyLabel1.get_size()
    text_width2, text_height2 = validMoneyLabel2.get_size()
    
    # Colocando o texto no automato
    x_text = 565  
    y_text = 117  

    # Concatenando os textos verticalmente
    screen.blit(validMoneyLabel1, (x_text, y_text))  
    screen.blit(validMoneyLabel2, (x_text, y_text + 20))

    # Exibir tipos de doces
    candyTypeLabel = font.render("Tipos de doce:", True, BLACK)
    screen.blit(candyTypeLabel, (700, 320))

    # Exibir troco (se houver)
    if machine.returnChangeBalance != 0:
        returnChange = font.render(f"Troco: R$ {machine.returnChangeBalance}", True, BLACK)
        screen.blit(returnChange, (700, 650))

    if purchased_candy:
        candy_text = font.render(f"Comprado: {purchased_candy}", True, RED)
        screen.blit(candy_text, (700, 700))
    
    # Animação da entrega do doce
    if drop_animation:
        pygame.draw.circle(screen, RED, (drop_animation[0], drop_animation[1]), 20)
        drop_animation[1] += 5  # Move o doce para baixo
        if drop_animation[1] >= 500:  # Ponto final da queda
            drop_animation = None

    # Desenhando botões
    for key, rect in buttons.items():
        pygame.draw.rect(screen, GREEN, rect)
        text = font.render(key, True, WHITE)

        # Centraliza o texto dentro do botão
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect.topleft)    
    
    pygame.display.flip()

pygame.quit()
