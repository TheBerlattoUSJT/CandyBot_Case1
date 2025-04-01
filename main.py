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
GREY = (191, 191, 189)

font = pygame.font.Font(None, 24)

machine = CandyMachine()
purchased_candy = None
change = 0
drop_animation = None #TODO: Implementar animação de queda de doce

# Criando botões na área preta da máquina
buttons = {
    "R$1": pygame.Rect(549, 160, 90, 35),
    "R$2": pygame.Rect(549, 196, 90, 35),
    "R$5": pygame.Rect(549, 232, 90, 35),
    "A": pygame.Rect(545, 292, 50, 50),
    "B": pygame.Rect(596, 292, 50, 50),
    "C": pygame.Rect(545, 343, 100, 50)
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
    balanceText1 = font.render(f"Saldo:", True, BLACK)
    balanceText2 = font.render(f"R$ {machine.balance}", True, BLACK)

    # Obtendo as larguras dos textos para centralizar da melhor forma
    balance_text_width1, balance_text_height1 = balanceText1.get_size()
    balance_text_width2, balance_text_height2 = balanceText2.get_size()

    # Colocando o texto no automato
    x_text = 565  
    y_text = 118

    # Concatenando os textos verticalmente
    screen.blit(balanceText1, (x_text, y_text))  
    screen.blit(balanceText2, (x_text, y_text + 20))

    # Exibir tipos de doces
    candyTypeLabel = font.render("Tipo de doce:", True, BLACK)
    screen.blit(candyTypeLabel, (542, 273))

    # Exibir troco (se houver)
    if machine.returnChangeBalance != 0:
        returnChange = font.render(f"Troco: R$ {machine.returnChangeBalance}", True, BLACK)
        screen.blit(returnChange, (544, 410))

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
        pygame.draw.rect(screen, GREY, rect)
        text = font.render(key, True, WHITE)

        # Centraliza o texto dentro do botão
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect.topleft)    
    
    pygame.display.flip()

pygame.quit()
