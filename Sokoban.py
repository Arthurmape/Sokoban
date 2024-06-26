# -*- coding: utf-8 -*-

"""
    Sokoban desenvolvido pelo Arthur M. P. no primeiro semestre de Estatística na USP.
"""

#-------------------------------------------------------------------------------
# DEFINIÇÃO DE ALGUMAS 'CONSTANTES' DO PROGRAMA
#-------------------------------------------------------------------------------

# CARACTERES USADOS NO MAPA DO JOGO
PAREDE           = '#'
PISO_VAZIO       = ' '
MARCA_VAZIA      = '.'    
CAIXA_NO_PISO    = '$'
CAIXA_NA_MARCA   = '*'
JOGADOR_NO_PISO  = '@'
JOGADOR_NA_MARCA = '+'

# CARACTERES USADOS PARA ESCOLHER E INDICAR UM MOVIMENTO DO JOGADOR
CIMA     = 'w'
BAIXO    = 's'
ESQUERDA = 'a'
DIREITA  = 'd'
FINALIZA = 'f'

#  CARACTERES USADOS PARA INDICAR UM MOVIMENTO DO JOGADOR QUANDO UMA CAIXA
CIMA_CX     = 'W'
BAIXO_CX    = 'S'
ESQUERDA_CX = 'A'
DIREITA_CX  = 'D'

DirMovJog = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}

#-------------------------------------------------------------------------------

def main():
    ''' ( ) --> NoneType
    ... complete ...
    '''

    mapa = le_arquivo_cria_mapa_jogo()

    historico_movimentos = ""
    movimentos_rodada = ""

    jogo_continua = True 
    
    while jogo_continua:
        imprime_mapa_jogo_emoldurado(mapa)

        escolha = input(" Digite os movimentos que deseja para o jogador, "
                        "escolhendo entre\n| w | s | a | d | f | "
                        "(cima, baixo, esq, dir, finaliza): ").lower()
        
        n = len(escolha)        
        i = 0

        while i < n and jogo_continua:
            
            caractere = escolha[i]
            i = i+1

            if caractere in ("w", "a", "s", "d"):
                teste1 = tenta_movimentar_jogador(mapa, caractere)
                
                if teste1 == (True, True):
                    movimentos_rodada += caractere.upper()
                    historico_movimentos += caractere.upper()
                    
                elif teste1 == (True, False):
                    movimentos_rodada += caractere.lower()
                    historico_movimentos += caractere.lower()
                continue
                    
            if caractere == "f":
                print("Você pressionou o botão para finalizar o jogo, jogo terminado.")
                jogo_continua = False
                break
                
            else:
                print("Código de movimentação inválido")
                jogo_continua = False
                print(movimentos_rodada)
                movimentos_rodada = ""
                break

        print("movimentos da rodada: " + movimentos_rodada)
        movimentos_rodada = ""
        print("\n"+"-" * 80)
        if todas_caixas_posicionadas(mapa):
            imprime_mapa_jogo_emoldurado(mapa)
            print(f"Parabéns, você ganhou o jogo!\nVocê usou a seguinte sequência de movimentos: {historico_movimentos}, usando {len(historico_movimentos)} de teclas.")
            jogo_continua = False
      
def le_arquivo_cria_mapa_jogo():
    ''' ( ) --> matriz 

    Lê o nome de um arquivo contendo um mapa de um jogo de Sokoban.
    Abre esse arquivo, lê uma representação de um mapa de jogo de
    Sokoban, cria uma matriz com esse mapa e retorna a matriz criada.
    
    Exemplo:
    Para o arquivo de entrada "sokoban00.txt" com o mapa abaixo:
    #####
    #@$. #
    #####

    a seguinte lista de listas é retornada:
    [['#', '#', '#', '#', '#'], ['#', '@', '$', '.', ' ', '#'], 
                                     ['#', '#', '#', '#', '#']]
    '''
  
    
  
    nomeArq = input("Digite o nome de um arquivo com um mapa do jogo sokoban: ")

    with open(nomeArq, 'r', encoding='utf-8') as arqEntra:
        mapa = []
        for linha in arqEntra:
            mapa.append(list(linha.rstrip()))
            
    return mapa  
     
#-------------------------------------------------------------------------------
    
def imprime_mapa_jogo(mapa):
    ''' (matriz) --> NoneType

    Recebe uma matriz representando um mapa de um jogo de Sokoban
    e imprime esse mapa.

    Exemplo: Se mapa referencia a seguinte lista de listas:
    [['#', '#', '#', '#', '#'], ['#', '@', '$', '.', ' ', '#'], 
                                     ['#', '#', '#', '#', '#']]
    a função deve imprimir:
    
      Mapa de um jogo:

      #####
      #@$. #
      #####

    '''
  
    print("\n Mapa de um jogo \n")        
    for linha in mapa:
        print(f"{''.join(linha)}")
    print()
            
#-------------------------------------------------------------------------------

def imprime_mapa_jogo_emoldurado(mapa):
    ''' (matriz) --> NoneType

    Recebe uma matriz representando um mapa de um jogo de Sokoban
    e imprime esse mapa totalmente "emoldurado" e com as linhas e
    colunas numeradas para facilitar a visualização do usuário.

    '''

    maxcol = 0
    for linha in mapa:
        if len(linha) > maxcol:
            maxcol = len(linha)
    
    print("\n") 
    s = ' '*7
    for i in range(maxcol):
        s += f"{i:^5} "
    print(f"{s}")
    
    molda_linha = (' '*6) + ('+-----' * maxcol) + '+'
    print(f"{molda_linha}")
    
    nlin = len(mapa)
    for i in range(nlin):
        ncol = len(mapa[i])
        s = f"{i:5} "
        for j in range(ncol):
            s+= f"|{mapa[i][j]:^5}"
        for k in range(ncol, maxcol):
            s+= f"|{' '*5}"
        s+='|'
        print(f"{s}")
        print(f"{molda_linha}")
    print()  
        
#-------------------------------------------------------------------------------

def posicao_jogador(mapa):
    ''' (matriz) --> (int, int) ou (NoneType, NoneType)

    Recebe uma matriz representando um mapa de um jogo de Sokoban.
    Retorna os índices de linha e de coluna da posição do jogador
    na matriz mapa.
    Caso o jogador não seja encontrado, deve retornar (None, None).

    Exemplo: No mapa abaixo, o jogador está na posição (2, 3).
    
    #######
    #     #
    # $+$ #
    #.*#*.#
    # $.$ #
    #     #
    #######

    ''' 
    
    pos_jogador = 0
    
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == JOGADOR_NO_PISO or mapa[i][j] == JOGADOR_NA_MARCA:
                pos1, pos2 = i,j
                pos_jogador += 1
                
    if pos_jogador == 1:
        return pos1, pos2
    else:
        print("Jogador não encontrado ou diversos jogadores encontrados.")
        return None, None
    
#-------------------------------------------------------------------------------

def tenta_movimentar_jogador(mapa, caracMov):
    ''' (matriz, str) --> (bool, bool)

    Recebe uma matriz representando um mapa de um jogo de Sokoban e 
    um caractere caracMov que representa uma das direções possíveis 
    (CIMA, BAIXO, ESQUERDA ou DIREITA) para um movimento do jogador.
    Se possível, a função realiza o movimento dado por caracMov e 
    atualiza a matriz mapa. 
    A função retorna dois valores booleanos:
    - O primeiro indica se o movimento é válido (True) ou não (False).
    - O segundo indica se uma caixa foi empurrada (True) ou não (False)
    pelo movimento do jogador.
    OBS: 1) O segundo valor deve ser sempre False se o primeiro for False.
    2) Quando o movimento não é válido (ou porque o jogador vai bater na
    parede ou porque a caixa que seria empurrada pelo jogador está presa),
    a função escreve uma mensagem na tela relatando uma das duas situações.
    '''

    jogador_antes = posicao_jogador(mapa)
    
    movimento = DirMovJog.get(caracMov)
    
    jogador_depois = jogador_antes[0] + movimento[0], jogador_antes[1] + movimento[1]
    
    mov_apos = jogador_depois[0] + movimento[0], jogador_depois[1] + movimento[1]
    
    if mapa[jogador_depois[0]][jogador_depois[1]] == PAREDE:
        print("\nMovimento inválido, você bateu em uma parede!")
        
        return(False, False)
    
    elif mapa[jogador_depois[0]][jogador_depois[1]] == PISO_VAZIO: #JOGADOR INDO PARA UM PISO VAZIO
        mapa[jogador_depois[0]][jogador_depois[1]] = JOGADOR_NO_PISO
        
        if mapa[jogador_antes[0]][jogador_antes[1]] == JOGADOR_NA_MARCA:
            mapa[jogador_antes[0]][jogador_antes[1]] = MARCA_VAZIA
            
        else:
            mapa[jogador_antes[0]][jogador_antes[1]] = PISO_VAZIO
            
        return(True, False)
    
    elif mapa[jogador_depois[0]][jogador_depois[1]] == MARCA_VAZIA: #JOGADOR INDO PARA UMA MARCA
        mapa[jogador_depois[0]][jogador_depois[1]] = JOGADOR_NA_MARCA
        
        if mapa[jogador_antes[0]][jogador_antes[1]] == JOGADOR_NA_MARCA:
            mapa[jogador_antes[0]][jogador_antes[1]] = MARCA_VAZIA
            
        else:
            mapa[jogador_antes[0]][jogador_antes[1]] = PISO_VAZIO
        
        return(True, False)
    
    elif (mapa[jogador_depois[0]][jogador_depois[1]] in (CAIXA_NO_PISO, CAIXA_NA_MARCA) and 
          mapa[mov_apos[0]][mov_apos[1]] in (PISO_VAZIO, MARCA_VAZIA)):
        if mapa[jogador_depois[0]][jogador_depois[1]] == CAIXA_NA_MARCA:
            mapa[jogador_depois[0]][jogador_depois[1]] = JOGADOR_NA_MARCA
        else:
            mapa[jogador_depois[0]][jogador_depois[1]] = JOGADOR_NO_PISO
        
        if mapa[mov_apos[0]][mov_apos[1]] == PISO_VAZIO:
            mapa[mov_apos[0]][mov_apos[1]] = CAIXA_NO_PISO
        elif mapa[mov_apos[0]][mov_apos[1]] == MARCA_VAZIA:
            mapa[mov_apos[0]][mov_apos[1]] = CAIXA_NA_MARCA
        
        if mapa[jogador_antes[0]][jogador_antes[1]] == JOGADOR_NA_MARCA:
            mapa[jogador_antes[0]][jogador_antes[1]] = MARCA_VAZIA
        else:
            mapa[jogador_antes[0]][jogador_antes[1]] = PISO_VAZIO

        return(True, True)
    
    elif (mapa[jogador_depois[0]][jogador_depois[1]] in (CAIXA_NO_PISO, CAIXA_NA_MARCA) and 
          mapa[mov_apos[0]][mov_apos[1]] in (PAREDE, CAIXA_NA_MARCA, CAIXA_NO_PISO)):
        print("\nMovimento inválido, a caixa que você empurrou está presa!")

        return(False, False)
    
    else:
        return(False, False)

#-------------------------------------------------------------------------------
 
def todas_caixas_posicionadas(mapa):
    ''' (matriz) --> bool

    Recebe uma matriz representando um mapa de um jogo de Sokoban e
    verifica se todas as caixas estão posicionadas nas marcas. 
    Se estiverem, a função retorna True; em caso contrário, retorna False.
    '''
    
    caixas = 0
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "$":
                caixas += 1
                
    if caixas >= 1:
        return False
    else:
        return True
     
#-------------------------------------------------------------------------------
main()
