from .helpers import *


def eliminarEpsilonTransicoes(afnd):
    epsilon = []

    for chave in afnd.keys():
        if '&' in afnd[chave]:
            epsilon.append(chave)

    def copiarRegras(regras, nRegra):
        if nRegra not in epsilon:
            return

        epsilon.remove(nRegra) 

        for regra in regras['&']:
            chaves = afnd[regra].keys()
            
            if '&' in chaves:
                copiarRegras(afnd[regra], regra)
                regras['&'] = merge_lists(regras['&'], afnd[regra]['&'])
        
        afnd[nRegra] = merge_states(afnd, regras['&'] + [nRegra])

    epAux = epsilon.copy()

    for ep in epAux:
        copiarRegras(afnd[ep], ep)
    
    for ep in epAux:
        del afnd[ep]['&']


def determinizar(afnd):
    mpRgs = {}
    visitados = set()

    def determiniza(regra, nReg):
        if nReg in visitados: 
            return
        visitados.add(nReg) 
        chaves = list(regra.keys())

        for chave in chaves:
            if len(regra[chave]) > 1:
                regra[chave].sort()
                # Usa a lista ordenada como chave canônica do subconjunto de estados
                nRg = str(regra[chave])
                
                if nRg not in mpRgs.keys(): 
                    nEst = len(afnd)
                    mpRgs.update({nRg: nEst})
                    afnd.update({len(afnd): merge_states(afnd, regra[chave])})
                    determiniza(afnd[nEst], nEst)
                
                regra.update({chave: [mpRgs[nRg]]})

    i, t = 0, len(afnd)
    while i < t:
        determiniza(afnd[i], i)
        i, t = i + 1, len(afnd)
