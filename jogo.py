from PPlay.window import Window
from PPlay.sprite import Sprite
import random

janela = Window(1280, 800)
janela.set_title("Jogo do Pong - Anna")

teclado = janela.get_keyboard()


# BOLA!!! ----------------------------------------------
bola = Sprite("bola.png")
bola.set_position(      #site do pplay ensina
    (1280 / 2) - (bola.width / 2),
    (800 / 2) - (bola.height / 2)
)

# estrutura do pad rosinha --------------------------------------
pad_esquerdo = Sprite("pad.png")  #player
pad_direito = Sprite("pad.png")   #IA

pad_esquerdo.set_position(
    20,
    (janela.height / 2) - (pad_esquerdo.height / 2)
)

pad_direito.set_position(
    janela.width - pad_direito.width - 20,
    (janela.height / 2) - (pad_direito.height / 2)
)

#velocidade da bolinha e dos pads -------------------------------
vel_inicial_x = 250
vel_inicial_y = 180

vel_bola_x = vel_inicial_x        #tive que colocar igual porque estava dando um erro de física, qdo a bolinha voltava a física meio q mudava e ficava mais lento e com o movimento feio
vel_bola_y = vel_inicial_y

vel_pad = 400
vel_ia = 300

aceleracao = 1.02
vel_max = 600

esperando = False

pontos_esquerda = 0
pontos_direita = 0

colidiu_esq = False
colidiu_dir = False

#loop ---------------------------------------

contador_evento = 0
evento_ativo = False

while True:
    
    janela.set_background_color((255, 160, 180))   #cor rosinha só p lembrar
    dt = janela.delta_time()

    if teclado.key_pressed("UP"):
        pad_esquerdo.y -= vel_pad * dt
    if teclado.key_pressed("DOWN"):
        pad_esquerdo.y += vel_pad * dt

#player --------------------------------------------------------

    if pad_esquerdo.y < 0:
        pad_esquerdo.y = 0
    if pad_esquerdo.y > janela.height - pad_esquerdo.height:
        pad_esquerdo.y = janela.height - pad_esquerdo.height


#pads (estava com erro) --------------------------------------------------------------
    centro_ia = pad_direito.y + pad_direito.height / 2

    erro = 20

    if bola.y > centro_ia + erro:
        pad_direito.y += vel_ia * dt
    elif bola.y < centro_ia - erro:
        pad_direito.y -= vel_ia * dt

    pad_direito.y = max(0, min(janela.height - pad_direito.height, pad_direito.y))

    
    if pad_direito.y < 0:
        pad_direito.y = 0
    if pad_direito.y > janela.height - pad_direito.height:
        pad_direito.y = janela.height - pad_direito.height

    # velocidade da bola no loop ------------------------------------------------

    if not esperando:
        bola.x += vel_bola_x * dt
        bola.y += vel_bola_y * dt

    # colisão topo/fundo ---------------------------------------------------
    if bola.y <= 0:
        bola.y = 0
        vel_bola_y *= -1

    if bola.y + bola.height >= janela.height:
        bola.y = janela.height - bola.height
        vel_bola_y *= -1

    # colisão pads --------------------------------------------------------

    #colisao pad esquerdo
    if bola.collided(pad_esquerdo):
        if not colidiu_esq:
            contador_evento += 1
        bola.x = pad_esquerdo.x + pad_esquerdo.width
        vel_bola_x *= -1

        vel_bola_x *= aceleracao
        vel_bola_y *= aceleracao

        colidiu_esq = True

    else:
        colidiu_esq = False
        
    #colisao pad direito
    if bola.collided(pad_direito):
        if not colidiu_dir:
           contador_evento += 1
           bola.x = pad_direito.x - bola.width
           vel_bola_x *= -1

           vel_bola_x *= aceleracao
           vel_bola_y *= aceleracao

           colidiu_dir = True
    else:
        colidiu_dir = False
       

    #qdo encosta na margem ------------------------------------------

    if bola.x < 0:
        pontos_direita += 1
        esperando = True

    elif bola.x > janela.width:
        pontos_esquerda += 1
        esperando = True


    if esperando:
        bola.set_position(
            (janela.width / 2) - (bola.width / 2),
            (janela.height / 2) - (bola.height / 2)
        )

        vel_bola_x = 0
        vel_bola_y = 0

        if esperando and teclado.key_pressed("SPACE"):
            esperando = False
            vel_bola_x = random.choice([-vel_inicial_x, vel_inicial_x])
            vel_bola_y = random.choice([-vel_inicial_y, vel_inicial_y])

#final (draw e tamanho da janela) -------------------------------

    janela.draw_text(
       f"{pontos_esquerda}  x  {pontos_direita}",
       janela.width / 2 - 50,
       50,
       size=40,
       color=(0, 0, 0)
    )
            
    bola.draw()
    pad_esquerdo.draw()
    pad_direito.draw()
    janela.update()    #no final, "swap buffer" como dito em aula


