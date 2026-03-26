from PPlay.window import Window
from PPlay.sprite import Sprite

janela = Window(800, 800)
janela.set_title("Jogo do Pong - Anna")

bola = Sprite("bola.png")
bola.set_position(      #site do pplay ensina
    (800 / 2) - (bola.width / 2),
    (800 / 2) - (bola.height / 2)
)

while True:
    janela.set_background_color((255, 160, 180))   #cor rosinha só p lembrar
    bola.draw()
    janela.update()


