# Caboclinho, o guerreiro de lança
Jogo 2D de visão top-down desenvolvido utilizando a biblioteca Pygame, inspirado no jogo "Vampire survivor" (personagem principal que tem inimigos e tem que lutar para sobreviver). O nosso héroi, caboclinho, se vê desamparado numa noite no recife antigo, mais especificamente no marco zero, contra inimigos ferozes que, sem motivação aparente. querem matá-lo. Para se defender, nosso protagonista dispõe de uma -colocar a arma- e, com muita sorte, os inimigos carregam com eles alguns itens que o ajudam na sua noitada. A galega do santo amaro quando derrotada, deixa cair uma maçã que recupera um pouco a energia do nosso herói, Boca D'ouro, por sua vez, quando derrotado deixa cair um punhado de confete (que serve pra recarregar a lança de confetes - que, por sorte, serve como munição para lança de confetes), lobisomem e perna fazem o nosso protagonista perceber o tempo passando.

# Integrantes da equipe
- [Jean Lucas de Barros Dias (jlbd)] (https://github.com/JBDhh): implementação dos sprites, implementação da animação, mapa, campo de visão, morte dos monstros, drop dos coletáveis
- [Leandro Jr. Marques Dos Santos (ljms)](https://github.com/LeandroJrMarques): animação do personagem, design, musicas, historia e organização do projeto
-[Pablo Richard (prsn)] (https://github.com/pablorixardsm): implementação da arma e projétil, correção de colisão, correção da inicialização dos monstros
-[Maria Eduarda Veloso Vieira <mevv>)] (https://github.com/Duda-Veloso): código de implementação dos monstros, correção de colisão, correção da inicialização dos monstros e idealização do Chico
-[Lucas Duarte. (ldbo)] (https://github.com/Duartebraz): criação do código base, criação de classes, funções e grupos iniciais, configurações iniciais de tela, configurações iniciais do personagem, movimentação do personagem, movimentação da câmera seguindo personagem, configurações iniciais de colisão, base da arma sem impletação.
-[Mairon Rodrigues Nunes (mrn)] (https://github.com/Mairon-Nunes):
criação de classes, criação de mecânicas, alterações visuais, configuração de funções, configuração de tela.

# Estruturação do código
import biblioteca pygame para ambientar o game,os.path join para upar os sprites,(spritesheet),(arquivos de audio),
para criação de tela foram divididas inicialmente 3 principais classes, as configurações onde ficariam os imports gerais
como o pygame, a largura a altura e caso fosse necessario o tamanho da tela, depois dela vem a main que importa da
classe configurações e da classe personagens, lá é onde usando de refencia configurações, é gerado a tela, nome do game
tamanho do player,uma parte da velocidade do personagem  e o loop ao qual roda o game, e por fim a classe player,
que coloca o personagem em certa posição pre-defina, onde rebece as entradas, no caso as teclas que vão movimentar 
o personagem, a hit box do personagem, os sprite iniciais dele,a velocidade que o personagem vai se movimentar e 
as configurações de camera que segue o personagem conforme a direção que ele vai

funcoes:

main{

def __init__(self): função onde esta contida a tela, titulo, o relogio(que é responsavel também pela velocidade
do personagem), os grupos como colisão e spites, o tamanho do player e os sprites de algumas colisões


def rodar(self): função onde vai ter o dt que é responvel por uma parte da velocidade, na função também
ira passar o loop que ocorre o game e tambem ira passar as atualizações de frames 
}

player{

def __init__(self, pos, grupos,colisao_sprites): função com sprite do player, posição, hitbox, direcao da movimentação,
velocidade, colisão do player.

def entradas(self): configurações das teclas e qual vai ser usada para oque

def movimentacao(self,dt): movimentação final do personagem juntando a velocidade o eixo que ele vai se locomover e a
direção

def colisao (self, direcao):parte responsavel por fazer a camera seguir o personagem
}

grupos{
 super().__init__(): grupo de telas seta o display/tela do game para receber o get_suface da pygame

 def draw(self,encontra_pos): controla onde a camera que segue o personagem vai surgir inicialmente

# Desafios e aprendizados
Como desafios, podemos destacar a gestão de tempo, tendo em vista o tempo limitado e a atenção que outras disciplinas exigiram paralelamente; a coordenação e divisão de tarefas, visto que todos não estavam habituados com a gestão de projetos; a manutenção de um código limpo e organizado, o que foi solucionado com uma quantidade satisfatória de comentários; a utilização do GitHub de maneira colaborativa.
Como aprendizados, observamos uma boa redistribuição de tarefas, quando necessário; e a exploração da biblioteca pygame;

# imagem do Jogo

![Jogo](https://github.com/Duartebraz/projeto_ip/blob/main/images/telas/jogo_rodando.png)