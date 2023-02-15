import os
import random
import pygame



TELA_LARGURA = 500  
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEN_BACK = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGEMS_PARDAL = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
    ]
pygame.font.init()
FONTE_PONTUACAO = pygame.font.SysFont('verdana', 50)


class Pardal:
    IMGS = IMAGEMS_PARDAL
    # Definindo animações do padarl em parábola com concavidade para cima
    Rotacao_Max = 25
    SPEED_ROT = 20
    TEMPO_ANIME = 5
    # Informaçoes do pardal

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_img = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        self.y += deslocamento

        # Angulo do pardal
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.Rotacao_Max:
                self.angulo = self.Rotacao_Max
        else:
            if self.angulo > -90:
                self.angulo -= self.SPEED_ROT

    def desenhar(self, tela):
        # Definir a imagem do pardal que vai ser utilizada
        self.contagem_img += 1
        if self.contagem_img < self.TEMPO_ANIME:
            self.imagem = self.IMGS[0]
        elif self.contagem_img < self.TEMPO_ANIME*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_img < self.TEMPO_ANIME*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_img < self.TEMPO_ANIME*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_img >= self.TEMPO_ANIME*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_img = 0

        # Se o pardal estiver a cair as assas não se mechem
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_img = self.TEMPO_ANIME*2

        # Desenhando a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicao_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro_img)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Canos:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA


    def mover_cano(self):
        self.x -= self.VELOCIDADE

    def desenhar_cano(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, pardal):
        pardal_mask = pardal.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        # Calculando a distância dos canos da base e do topo em relação ao pardal
        distancia_topo = (self.x - pardal.x, self.pos_topo - round(pardal.y))
        distancia_base = (self.x - pardal.x, self.pos_base - round(pardal.y))
        topo_ponto = pardal_mask.overlap(topo_mask, distancia_topo)
        base_ponto = pardal_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Terra:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


# Desenhando a tela do jogo


def desenhar_tela(tela, pardals, canos, chao, pontos):
    tela.blit(IMAGEN_BACK, (0, 0))
    for pardal in pardals:
        pardal.desenhar(tela)
    for cano in canos:
        cano.desenhar_cano(tela)

    texto = FONTE_PONTUACAO.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def main():
    pardals = [Pardal(230, 350)]
    chao = Terra(730)
    canos = [Canos(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    # Música do jogo
    pygame.init()
    # inicializar o mixer do Pygame
    pygame.mixer.init()
    # carregar a música
    musica = pygame.mixer.Sound\
        (r'C:\Users\vidal\Downloads\Sweet Dreams (SrSider FUNK REMIX).mp3') # Mude a música  indicando seu diretório.

    # iniciar a reprodução da música em loop infinito
    musica.play(-1)
    volume = 0.5

    while rodando:
        relogio.tick(30)  # Framerate, acima deste valor fica muito rápido.

        # Interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for pardal in pardals:
                        pardal.pular()
                if evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:
                    volume = min(volume + 0.1, 1.0)
                    musica.set_volume(volume)
                elif evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                    volume = max(volume - 0.1, 0.0)
                    musica.set_volume(volume)

        # Movendo os Objetos
        for pardal in pardals:
            pardal.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, pardal in enumerate(pardals):
                if cano.colidir(pardal):
                    pardals.pop(i)
                if not cano.passou and pardal.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover_cano()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        if adicionar_cano:
            pontos += 1
            canos.append(Canos(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, pardal in enumerate(pardals):
            if(pardal.y + pardal.imagem.get_height()) > chao.y or pardal.y < 0:
                pardals.pop(i)

        desenhar_tela(tela, pardals, canos, chao, pontos)


if __name__ == '__main__':
    main()
