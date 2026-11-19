from .utils import *


def eliminarEpsilonTransicoes(afnd):
    epsilon = []

    for chave in afnd.keys():
        if '&' in afnd[chave]:
            epsilon.append(chave) # guarda os estados que têm '&'

    def copiarRegras(regras, nRegra):
        if nRegra not in epsilon:
            return

        epsilon.remove(nRegra) 

        for regra in regras['&']:
            chaves = afnd[regra].keys()
            
            if '&' in chaves: # se o destino também tiver '&', puxa os dele antes
                copiarRegras(afnd[regra], regra)
                regras['&'] = merge_lists(regras['&'], afnd[regra]['&'])
        
        afnd[nRegra] = merge_states(afnd, regras['&'] + [nRegra]) # puxa as transições do destino pro estado atual

    epAux = epsilon.copy()

    for ep in epAux:
        copiarRegras(afnd[ep], ep)
    
    for ep in epAux:
        del afnd[ep]['&'] # apaga o '&' depois de copiar tudo


def determinizar(afnd):
    mpRgs = {}
    visitados = set()

    def determiniza(regra, nReg):
        if nReg in visitados: 
            return
        visitados.add(nReg) 
        chaves = list(regra.keys())

        for chave in chaves:
            if len(regra[chave]) > 1: # se a mesma letra vai pra mais de um estado
                regra[chave].sort()
                nRg = str(regra[chave]) # vira texto (ex: '[1, 8]') pra salvar no mapa mpRgs
                
                if nRg not in mpRgs.keys(): 
                    nEst = len(afnd) # número do estado novo que vai juntar eles
                    mpRgs.update({nRg: nEst})
                    afnd.update({len(afnd): merge_states(afnd, regra[chave])}) # cria o estado novo juntando as transições
                    determiniza(afnd[nEst], nEst)
                
                regra.update({chave: [mpRgs[nRg]]}) # troca a lista repetida pelo estado único novo

    i, t = 0, len(afnd)
    while i < t:
        determiniza(afnd[i], i)
        i, t = i + 1, len(afnd) # atualiza o tamanho pq podem ter surgido estados novos
