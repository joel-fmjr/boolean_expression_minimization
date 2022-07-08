import re
from typing import List


def find_x_in_y(x, y):
    smallest = min(x, y, key=len)
    biggest = y if smallest == x else x
    regex = re.findall(r'[{}]'.format(smallest), biggest)
    found = ''.join(sorted(regex))
    smallest = ''.join(sorted(smallest))
    return found, smallest, biggest
    

def multiply_terms(x, y):
    found, smallest, biggest = find_x_in_y(x, y)    
    if smallest in found:
        return biggest
    return smallest + biggest


def sum_terms(x, y):
    found, smallest, biggest = find_x_in_y(x, y)    
    if smallest in found:
        return smallest
    return smallest + '+' + biggest


def petricks_method(minterms: dict) -> List[str]:
    keys = list(minterms.keys())
    sops = []
    for i in range(len(keys) - 1):
        for minterm_1 in minterms[keys[i]]:
            for j in range(i+1, len(keys)):
                if minterm_1 in minterms[keys[j]]:
                    summ = '+'.join([keys[i][0], keys[j][0]])
                    sops.append(summ) if summ not in sops else None
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
    smallest = min(result, key=len)
    smallest_terms = [minterm for minterm in result if len(minterm) == len(smallest)]
    return smallest_terms
