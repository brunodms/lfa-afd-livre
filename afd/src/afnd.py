from re import findall as find
from .helpers import *

def gerarAfndToken(afnd, token, alfabeto):
    if not afnd:
        afnd[0] = {}  # Cria o estado inicial do AFND caso não exista

    tokenInicial = True  # Flag para identificar o primeiro caractere
    
    for tk in token:
        if tk not in alfabeto:
            alfabeto.append(tk)  # Adiciona o caractere do token ao alfabeto caso não esteja presente
            
        if tokenInicial:
            state = afnd[0]  # Ponteiro para o estado inicial

            if tk in state.keys():
                state[tk].append(len(afnd))  # Adiciona uma transição para um novo estado caso a regra já exista
            else:
                state.update({tk: [len(afnd)]})
            tokenInicial = False
        else:
            afnd[len(afnd)] = {tk: [len(afnd) + 1]}  # Cria um novo estado para transitar para o próximo caractere
            
    afnd[len(afnd)] = {'*': [1]}  # Estado final ao chegar ao fim do token


def gerarAfndGramatica(afnd, gramatica, alfabeto):
    if not afnd:
        afnd[0] = {}  # Cria o estado inicial do AFND caso não exista
    
    afndTemporario = {}
    mapaRegras = {}
    
    for regra in gramatica:
        regra_normalizada = regra.replace('ε', '&').replace('ɛ', '&')
        symbols = find(r'(\w*<\w+>|\w+|&)', regra_normalizada)  # Separa a regra e suas produções
        
        # Identifica ou cria uma regra no autômato temporário
        if symbols[0] in mapaRegras:
            rule_index = mapaRegras[symbols[0]]
        else:
            rule_index = len(afndTemporario)
            afndTemporario[rule_index] = {}
            mapaRegras[symbols[0]] = rule_index
        
        for symbol in symbols[1:]:
            terminal = find(r'^\w+', symbol)
            non_terminal = find(r'<\w+>', symbol)
            terminal = '&' if not terminal else terminal[0]

            if terminal != '&' and terminal not in alfabeto:
                alfabeto.append(terminal)
            
            if not non_terminal:
                state = afndTemporario[rule_index]

                if terminal in state:
                    state[terminal].append(len(afndTemporario))
                else:
                    state.update({terminal: [len(afndTemporario)]})
                
                afndTemporario[len(afndTemporario)] = {'*': [1]}
            else:
                non_terminal = non_terminal[0]

                if non_terminal in mapaRegras:
                    state = mapaRegras[non_terminal]
                else:
                    state = len(afndTemporario)
                    mapaRegras[non_terminal] = state
                    afndTemporario[state] = {}

                pointer = afndTemporario[rule_index]

                if terminal in pointer:
                    pointer[terminal].append(state)
                else:
                    pointer.update({terminal: [state]})

    merge_automatons(afnd, afndTemporario)
