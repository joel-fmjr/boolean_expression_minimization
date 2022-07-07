from petricks_method import *
from typing import Iterable
from utils import *


def create_groups(minterms: List[str]) -> dict:
    """
    Creates a dictionary in witch the keys represent the number of '1's 
    and the values are the minterms that contain such number of '1's.
    :param minterms: List of minterms in binary.
    :return: Dictionary.
    """
    groups = {}
    for minterm in minterms:
        number_of_1s = minterm.count('1')
        try:
            groups[number_of_1s].append(minterm)
        except KeyError:
            groups[number_of_1s] = [minterm]

    sorting = sorted(groups.items(), key=lambda key_value: key_value[0])
    groups = dict(sorting)

    return groups


def implicant_to_int(implicant: str, minterms: List[str]) -> List[int]:
    if not implicant.count('-'):
        return [int(implicant, 2)]
    minterms_int = []
    regex = re.sub('-', '.+', implicant)
    for minterm in minterms:
        if re.match(regex, minterm):
            minterms_int.append(int(minterm, 2))
    return minterms_int


def prime_implicants(current_groups: dict, minterms: List[str]) -> dict:
    prime_implicants = set()
    while True:
        previous_groups = current_groups.copy()
        keys = list(previous_groups.keys())
        current_groups, marked = {}, set()
        stop = True

        for i in range(len(keys) - 1):
            for minterm_1 in previous_groups[keys[i]]:
                for minterm_2 in previous_groups[keys[i + 1]]:
                    count = 0
                    pos = None
                    for j, bits in enumerate(zip(minterm_1, minterm_2)):
                        if bits[0] != bits[1]:
                            count += 1
                            if count > 1:
                                break
                            pos = j
                    if count == 1:
                        product = minterm_1[:pos] + '-' + minterm_1[pos + 1:]
                        try:
                            current_groups[keys[i]].append(product)
                        except KeyError:
                            current_groups[keys[i]] = [product]
                        marked.update([minterm_1, minterm_2])
                        stop = False
        groups_values = previous_groups.values()
        implicants = []
        for group in groups_values:
            implicants += group
        unmarked = set(implicants).difference(marked)
        prime_implicants = prime_implicants.union(unmarked)
        prime_implicants_groups = {
            implicant: implicant_to_int(implicant, minterms)
            for implicant in prime_implicants
        }
        if stop:
            return prime_implicants_groups


def essencial_prime_implicants(prime_implicants: dict, minterms: List[int]) -> dict:
    essencial_prime_implicants = set()
    for minterm in minterms:
        count = 0
        essencial_pi = None
        for key in prime_implicants:
            if minterm in prime_implicants[key]:
                count += 1
                if count > 1:
                    break
                essencial_pi = key
        if count == 1:
            essencial_prime_implicants.add(essencial_pi)
    essencial_prime_implicants = {
        key: prime_implicants[key] for key in essencial_prime_implicants
    }
    return essencial_prime_implicants


def uncovered_minterms(minterms: List[int], prime_implicants: dict, essencial_pis: Iterable):
    covered_minterms = set()
    for minterm in essencial_pis.values():
        covered_minterms.update(minterm)
    covered_minterms = list(covered_minterms)
    covered_minterms.sort()

    if covered_minterms != minterms:
        for key in essencial_pis:
            prime_implicants.pop(key)
        for e_value in essencial_pis.values():
            for minterm in e_value:
                for value in prime_implicants.values():
                    if minterm in value:
                        value.remove(minterm)
        return True
    return False


def implicant_to_product(implicants: Iterable) -> List[str]:
    products = []
    for implicant in implicants:
        product = ''
        for j, bit in enumerate(implicant):
            if bit != '-':
                product += chr(65 + j)
                if bit == '0':
                    product += "'"
        products.append(product)
    return products


if __name__ == '__main__':
    num_variables = int(input('Número de variáveis: '))
    minterms = input('Informe os mintermos separados por espaço: ')
    minterms = minterms.strip().split()
    minterms = [int(minterm) for minterm in minterms]
    minterms.sort()

    minterms_bin = minterm_to_binary(num_variables, minterms)
    groups = create_groups(minterms_bin)

    prime_implicants = prime_implicants(groups, minterms_bin)
    essencial_prime_implicants = essencial_prime_implicants(prime_implicants, minterms)

    products = implicant_to_product(essencial_prime_implicants)
    expression = ""
    if products:
        expression = ' + '.join(products)

    uncovered_minterms = uncovered_minterms(minterms, prime_implicants, 
                                            essencial_prime_implicants)
    if uncovered_minterms:
        for i, key in enumerate(prime_implicants.copy()):
            new_key = (chr(65 + num_variables + i), key)
            prime_implicants[new_key] = prime_implicants.pop(key)

        petricks_minterms = petricks_method(prime_implicants)

        for minterm in petricks_minterms:
            final_expression = [expression] if expression else []
            for term in minterm:
                for key in prime_implicants:
                    if term in key:
                        final_expression.append(''.join(implicant_to_product([key[1]])))
            print(f"X = {' + '.join(final_expression)}")
    else:
        print(f'\nX = {expression}')
