import pygame
import random 

LARGURA, ALTURA = 300, 600
TAMANHO = 30 
COLUNAS, LINHAS = LARGURA // TAMANHO , ALTURA // TAMANHO

CORES = [
    (0,0,0),
    (0,240,240),
    (0,0,240),
    (240,160,0),
    (240,240,0),
    (0,240,0),
    (160,0,240),
    (240,0,0),
]

PECAS = [
        [[1, 1, 1, 1]],  
    [[2, 0, 0],
     [2, 2, 2]],     
    [[0, 0, 3],
     [3, 3, 3]],     
    [[4, 4],
     [4, 4]],        
    [[0, 5, 5],
     [5, 5, 0]],     
    [[0, 6, 0],
     [6, 6, 6]],     
    [[7, 7, 0],
     [0, 7, 7]] 
]

def nova_peca():
        return peca(random.choice(PECAS))    

def colide(tabuleiro, peca):
        for y, linha in enumerate(peca.matriz):
            for x, val in enumerate(linha):
                if val:
                    nx, ny = peca.x + x, peca.y + y
                    if nx < 0 or nx >= COLUNAS or ny >= LINHAS:
                        return True
                    if ny >= 0 and tabuleiro[ny][nx]:
                        return True
        return False        

def calcular_pontos(linhas):
    if linhas == 1:
       return 100
    elif linhas == 2:
       return 300
    elif linhas == 3:
       return 500
    elif linhas == 4:
       return 800
    return 0

class peca:
    def __init__(self, matriz):
        self.x = COLUNAS // 2 - len(matriz[0]) // 2
        self.y = 0
        self.matriz = [linha[:] for linha in matriz]

    def rotacionar(self):
        self.matriz = [list(linha) for linha in zip(*self.matriz[::-1])]


def mesclar(tabuleiro, peca):
    for y, linha in enumerate(peca.matriz):
        for x, val in enumerate(linha):
            if val:
                tabuleiro[peca.y + y][peca.x + x]= val

def limpar_linhas(tabuleiro):
    removidas = 0
    for y in range(LINHAS -1, -1, -1):
        if all(tabuleiro[y]):
            del tabuleiro[y]
            tabuleiro.insert(0,[0] * COLUNAS)
            removidas += 1
    return removidas

def desenhar_tabuleiro(screen, tabuleiro):
    for y in range(LINHAS):
        for x in range(COLUNAS):
            val = tabuleiro[y][x]
            cor = CORES[val]
            pygame.draw.rect(screen, cor, (x * TAMANHO, y * TAMANHO, TAMANHO -1, TAMANHO -1))

def desenhar_peca(screen, peca):
    for y, linha in enumerate(peca.matriz):
        for x, val in enumerate(linha):
            if val:
                cor= CORES[val]
                pygame.draw.rect(screen, cor, ((peca.x+x)*TAMANHO, (peca.y+y)*TAMANHO, TAMANHO-1, TAMANHO-1))

def desenhar_score(screen, fonte, score):
    texto = fonte.render(f"Score: {score}", True, (255,255,255))
    screen.blit(texto,(10,10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Arial", 24)

    tabuleiro = [[0] * COLUNAS for _ in range(LINHAS)]
    peca_atual = nova_peca()
    queda_tempo = 0
    velocidade_queda = 500
    rodando = True
    score = 0
    
    while rodando:
        delta = clock.tick()
        queda_tempo += delta

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    peca_atual.x -= 1
                    if colide(tabuleiro, peca_atual): peca_atual.x += 1
                elif evento.key == pygame.K_RIGHT:
                    peca_atual.x += 1
                    if colide(tabuleiro, peca_atual): peca_atual.x -= 1
                elif evento.key == pygame.K_DOWN:
                    peca_atual.y += 1
                    if colide(tabuleiro, peca_atual): peca_atual.y -= 1
                elif evento.key == pygame.K_UP:
                    peca_atual.rotacionar()
                    if colide(tabuleiro, peca_atual):
                     for _ in range(3): peca_atual.rotacionar()
                elif evento.key == pygame.K_SPACE:
                    while not colide(tabuleiro,peca):
                      peca_atual.y +=1
                    peca_atual.y -=1
                    mesclar(tabuleiro, peca_atual)
                    peca_atual = nova_peca()

        if queda_tempo > velocidade_queda:
         peca_atual.y += 1
         if colide(tabuleiro, peca_atual):
            peca_atual.y -=1
            mesclar(tabuleiro, peca_atual)
            limpar_linhas(tabuleiro)
            peca_atual = nova_peca()
            if colide(tabuleiro, peca_atual):
             rodando = False
         queda_tempo = 0

        screen.fill((0,0,0))
        desenhar_tabuleiro(screen, tabuleiro)
        desenhar_peca(screen, peca_atual)
        desenhar_score(screen,fonte,score)
        pygame.display.flip()

    pygame.quit()
   
if __name__ == "__main__":
    main()
