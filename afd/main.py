from pathlib import Path
from src.afnd import *
from src.minimiza import *
from src.determiniza import *
from src.helpers import *

def process_input_file(file_path):
    with open(file_path, "r", encoding="utf-8") as entrada:
        entrada_lista = [linha.strip() for linha in entrada.read().splitlines()]

    afd = {}
    alfabeto = []
    gramatica = []

    index = 0
    while index < len(entrada_lista):
        token_lido = entrada_lista[index]
        index += 1
        if token_lido == '':
            break
        gerarAfndToken(afd, token_lido, alfabeto)

    while index < len(entrada_lista):
        regra_gramatica_lida = entrada_lista[index]
        index += 1
        if regra_gramatica_lida:
            gramatica.append(regra_gramatica_lida)
        else: # caso tenha mais gramaticas
            if gramatica:
                gerarAfndGramatica(afd, gramatica, alfabeto)
                gramatica.clear()

    if gramatica:
        gerarAfndGramatica(afd, gramatica, alfabeto)
        gramatica.clear()

    eliminarEpsilonTransicoes(afd)
    determinizar(afd)
    
    print('Automato finito deterministico:')
    display_deterministic_automaton(afd, alfabeto)
    
    eliminarInalcancaveis(afd)
    print('\n Após eliminar inalcançáveis:')
    display_deterministic_automaton(afd, alfabeto)

    eliminarInuteis(afd)
    print('\n Após eliminar inúteis:')
    display_deterministic_automaton(afd, alfabeto)

    adicionarEstadoErro(afd, alfabeto)
    print('\n Após adicionar estado de erro:')
    display_deterministic_automaton(afd, alfabeto)

if __name__ == "__main__":
    input_file_path = Path(__file__).resolve().parent / "entrada.txt"
    process_input_file(input_file_path)