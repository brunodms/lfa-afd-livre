from re import findall as find
from .helpers import *

def gerarAfndToken(afnd, token, alfabeto):
    if not afnd:
        afnd[0] = {}

    tokenInicial = True
    
    for tk in token:
        if tk not in alfabeto:
            alfabeto.append(tk)
            
        if tokenInicial:
            state = afnd[0]

            if tk in state.keys():
                state[tk].append(len(afnd)) # se já tem a letra no estado 0, adiciona mais um destino na lista
            else:
                state.update({tk: [len(afnd)]}) # se não tem, cria a transição pro próximo estado
            tokenInicial = False
        else:
            afnd[len(afnd)] = {tk: [len(afnd) + 1]} # cria o estado atual apontando pro próximo
            
    afnd[len(afnd)] = {'*': [1]} # cria o estado final da palavra


def gerarAfndGramatica(afnd, gramatica, alfabeto):
    if not afnd:
        afnd[0] = {}
    
    afndTemporario = {}
    mapaRegras = {}
    
    for regra in gramatica:
        regra_normalizada = regra.replace('ε', '&').replace('ɛ', '&')
        symbols = find(r'(\w*<\w+>|\w+|&)', regra_normalizada) # separa a regra (symbols[0]) das produções (symbols[1:])
        
        if symbols[0] in mapaRegras:
            rule_index = mapaRegras[symbols[0]]
        else:
            rule_index = len(afndTemporario)
            afndTemporario[rule_index] = {} # cria o estado
            mapaRegras[symbols[0]] = rule_index # registra o estado no mapa
        
        for symbol in symbols[1:]:
            terminal = find(r'^\w+', symbol)
            non_terminal = find(r'<\w+>', symbol)
            if terminal == []:    
                terminal = '&'
            else: 
                terminal = terminal[0]

            if terminal != '&' and terminal not in alfabeto:
                alfabeto.append(terminal)
            
            if non_terminal:
                non_terminal = non_terminal[0]

                if non_terminal in mapaRegras:
                    state = mapaRegras[non_terminal] # pega o número do estado destino
                else:
                    state = len(afndTemporario)
                    mapaRegras[non_terminal] = state # registra o estado destino no mapa
                    afndTemporario[state] = {}

                pointer = afndTemporario[rule_index]

                if terminal in pointer:
                    pointer[terminal].append(state) 
                else:
                    pointer.update({terminal: [state]}) # aponta pro estado do não-terminal
            else:
                state = afndTemporario[rule_index]

                if terminal in state:
                    state[terminal].append(len(afndTemporario)) 
                else:
                    state.update({terminal: [len(afndTemporario)]}) # aponta pro novo estado final criado abaixo
                
                afndTemporario[len(afndTemporario)] = {'*': [1]} # cria um estado final novo

    merge_automatons(afnd, afndTemporario)
