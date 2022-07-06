import re
from typing import List

def multiply_terms(A, B):
    menor = min(A, B, key=len)
    maior = B if menor == A else A
    regex = re.findall(r'[{}]'.format(menor), maior)
    found = ''.join(sorted(regex))
    menor = ''.join(sorted(menor))

    if menor in found:
        return maior
    return menor + maior


def sum_terms(A, B):
    menor = min(A, B, key=len)
    maior = B if menor == A else A
    regex = re.findall(r'[{}]'.format(menor), maior)
    found = ''.join(sorted(regex))
    menor = ''.join(sorted(menor))

    if menor in found:
        return menor
    return menor + '+' + maior

def petricks_method(minterms: dict) -> List[str]:
    for i, key in enumerate(minterms):
        
    sops = re.findall(r'\((.+?)\)', expression)
    print(sops)
    result = ''
    tamanho = len(sops)
    while tamanho > 1:
        sops_splited1 = sops[0].split('+')
        sops_splited1.remove('') if '' in sops_splited1 else sops_splited1
        for term1 in sops_splited1:
            sops_splited2 = sops[1].split('+')
            sops_splited2.remove('') if '' in sops_splited2 else sops_splited2
            for term2 in sops_splited2:
                result += multiply_terms(term1, term2)
                result += '+'
        splited_result = sorted(result.split('+')[:-1], key=len)
        temp = splited_result.copy()
        i = 0
        while i < len(splited_result) - 1:
            j = i + 1
            while j < len(splited_result):
                result = sum_terms(splited_result[i], splited_result[j])
                if result == "".join(sorted(splited_result[i])):
                    try:
                        temp.remove(splited_result[j])
                    except ValueError:
                        None
                j += 1
            i += 1
            splited_result = temp.copy()
        result = '+'.join(temp)
        result += '+'
        sops[0] = result
        sops.pop(1)
        result = ''
        tamanho = len(sops)

    result = sops[0].split('+')[:-1]
    menor = min(result, key=len)
    menores = [minterm for minterm in result if len(minterm) == len(menor)]
    return menores