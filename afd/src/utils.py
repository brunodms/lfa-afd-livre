def merge_states(automaton, states):
    final_state = {}
    
    def merge(state):
        for s in state:
            if s in final_state:
                final_state[s] = merge_lists(final_state[s], state[s]) # se já tem a letra, junta os destinos
            else:
                final_state.update({s: state[s].copy()}) # se não tem, copia a transição

    for state in states:
        merge(automaton[state]) # junta todas as transições dos estados passados na lista
    
    return final_state


def merge_lists(list1, list2):
    return list1 + list(set(list2) - set(list1)) # junta duas listas sem repetir


def merge_automatons(afd, afnd_temp):
    new_state_mapping = {x: x + len(afd) for x in range(len(afnd_temp))} # soma o tamanho do afd pra não bater com os estados que já existem
    
    if '&' in afd[0].keys():
        afd[0]['&'].append(new_state_mapping[0])
    else:
        afd[0].update({'&': [new_state_mapping[0]]}) # liga o estado 0 no começo da gramática com '&'
    
    for key in afnd_temp.keys():
        for ch in afnd_temp[key].keys():
            if ch == '*':
                continue
            new_states = [new_state_mapping[i] for i in afnd_temp[key][ch]] # atualiza os destinos pros números novos
            afnd_temp[key][ch] = new_states
    
    for key in afnd_temp.keys():
        afd.update({new_state_mapping[key]: afnd_temp[key]}) # joga os estados da gramática dentro do afd principal


def display_deterministic_automaton(afnd, alphabet):
    alphabet.sort()
    print('     {}'.format('-----' * len(alphabet)))
    print('     |', end='')
    for i in alphabet:
        print('  {:2}|'.format(i), end='')
    print('\n     {}'.format('-----' * len(alphabet)))
    
    for i in afnd.keys():
        if '*' in afnd[i].keys():
            print('*', end='')
        else:
            print(' ', end='')
        print('{:3}:|'.format(i), end='')
        
        for j in alphabet:
            if j in afnd[i].keys():
                print(' {:2} |'.format(afnd[i][j][0]), end='')
            else:
                print(' {:2} |'.format('-'), end='')
        print('')
    print('     {}'.format('-----' * len(alphabet)))
