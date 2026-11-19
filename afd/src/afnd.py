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
                state[tk].append(len(afnd))
            else:
                state.update({tk: [len(afnd)]})
            tokenInicial = False
        else:
            # Aponta para o próximo índice sequencial (criado na iteração seguinte ou como estado final)
            afnd[len(afnd)] = {tk: [len(afnd) + 1]}
            
    afnd[len(afnd)] = {'*': [1]}  # '*' identifica estado final


def gerarAfndGramatica(afnd, gramatica, alfabeto):
    if not afnd:
        afnd[0] = {}
    
    afndTemporario = {}
    mapaRegras = {}
    
    for regra in gramatica:
        regra_normalizada = regra.replace('ε', '&').replace('ɛ', '&')
        # symbols[0] é o não-terminal da cabeça da regra; symbols[1:] são as produções
        symbols = find(r'(\w*<\w+>|\w+|&)', regra_normalizada)
        
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
                # Produção sem não-terminal à direita transita direto para um novo estado final
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
