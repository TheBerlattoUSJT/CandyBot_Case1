import pygame
import os
from machine import CandyMachine

pygame.init()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Vending Machine")

# Função para carregar imagens
def load_image(file_name):
    if os.path.exists(file_name):
        return pygame.transform.scale(pygame.image.load(file_name), (WIDTH, HEIGHT))
    else:
        print(f"Erro: Imagem '{file_name}' não encontrada!")
        return None

# Carregando imagens de fundo
backgrounds = {
    "default": load_image("30751.jpg"),  # Imagem original
    "A": load_image("DOCE_Ai.jpg"),  # Máquina doce  A, doce fora da maquina
    "B": load_image("DOCE_Bi.jpg"),  # Máquina doce  B, mesma coisa, doce fora da maquina
    "C": load_image("DOCE_Ci.jpg"),  # Máquina doce  C, doce fora da maquina
}

# Verifica se alguma imagem não foi carregada corretamente
if None in backgrounds.values():
    print("Erro: Certifique-se de que todas as imagens estão na pasta correta e com os nomes exatos!")

current_background = backgrounds["default"]  # Começa com a imagem original

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 100)
RED = (200, 50, 50)

font = pygame.font.Font(None, 36)

machine = CandyMachine()
selected_candy = None  # Doce atualmente comprado

# Criando botões
buttons = {
    "R$1": pygame.Rect(700, 150, 100, 40),
    "R$2": pygame.Rect(700, 200, 100, 40),
    "R$5": pygame.Rect(700, 250, 100, 40),
    "A": pygame.Rect(700, 350, 50, 50),
    "B": pygame.Rect(750, 350, 50, 50),
    "C": pygame.Rect(700, 410, 50, 50)
}

running = True
while running:
    screen.fill(WHITE)
    screen.blit(current_background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            clicked_button = False  # Verifica se um botão foi pressionado

            # Verifica se algum botão foi pressionado
            for key, rect in buttons.items():
                if rect.collidepoint(x, y):
                    clicked_button = True
                    print(f"Botão '{key}' pressionado.")  # Depuração

                    if key in ["R$1", "R$2", "R$5"]:
                        machine.insert_money(int(key[2:]))
                        print(f"Saldo atualizado: R$ {machine.balance}")  # Depuração

                    elif key in machine.candies:
                        machine.select_candy(key)

                        # Atualiza o fundo imediatamente ao comprar um doce
                        if key in backgrounds:
                            print(f"Alterando fundo para '{key}'")  # Depuração, pois não estava carregando as imagens
                            current_background = backgrounds[key]   # Escolhe a imagem de fundo com base key do doce selecionado

            # Se o clique foi fora dos botões, volta ao fundo original
            if not clicked_button:
                print("Clique fora dos botões. Voltando ao fundo original.")  # Depuração
                current_background = backgrounds["default"] # Retorna a imagem de fundo original
                selected_candy = None

    # Exibir saldo
    balanceText = font.render(f"Saldo: R$ {machine.balance}", True, BLACK)
    screen.blit(balanceText, (500, 600))

    # Exibir troco (se houver)
    if machine.returnChangeBalance != 0:
        returnChange = font.render(f"Troco: R$ {machine.returnChangeBalance}", True, BLACK)
        screen.blit(returnChange, (700, 650))

    # Exibir doce comprado
    if selected_candy:
        candy_text = font.render(f"Comprado: {selected_candy}", True, RED)
        screen.blit(candy_text, (700, 700))

    # Desenhando botões
    for key, rect in buttons.items():
        pygame.draw.rect(screen, GREEN, rect)
        text = font.render(key, True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect.topleft)

    pygame.display.flip()

pygame.quit()