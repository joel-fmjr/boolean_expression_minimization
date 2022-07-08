from typing import List, Iterable
import re


def create_groups(minterms: List[str]) -> dict:
    """
    Creates a dictionary in witch the keys represent the number of '1's 
    and the values are the minterms that contain such number of '1's.
    :param minterms: List of minterms in binary.
    :return groups: grouped minterms.
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
    """
    Finds the minterms, in binary form, witch are represented by the given implicant. 
    Than converts them to decimal form.

    EX.: implicant = 1-0-, minterms = [8, 9, 12, 13]

    :param implicant: string of '1's, '-'s or '0's.
    :param minterms: list of minterms in binary form
    :return minterms_int: list of minterms in decimal form
    """
    if not implicant.count('-'):
        return [int(implicant, 2)]
    minterms_int = []
    regex = re.sub('-', '.+', implicant)
    for minterm in minterms:
        if re.match(regex, minterm):
            minterms_int.append(int(minterm, 2))
    return minterms_int


def prime_implicants(current_groups: dict, minterms: List[str]) -> dict:
    """
    Generates the prime implicants and the minterms they represent using the minterms, 
    grouped by the number of '1' in each minterm, as established in the Quine–McCluskey algorithm.
    :param current_groups: minterms grouped by number of '1's.
    :param minterms: list of minterms in binary form
    :return prime_implicant_groups: Dictionary {prime_implicant: [minterms_int]}
    """
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


# TO DO: Talvez não seja necessário passar o parâmetro minterm
def essencial_prime_implicants(prime_implicants: dict, minterms: List[int]) -> dict:
    """
    Filters the essencial prime implicants out of the prime implicants passed.
    :param prime_implicants: dictionary of prime implicants and their respective minterms.
    :param minterms: list of minterms
    :return essencial_prime_implicants: Dictionary {essencial_prime_implicant: [minterms_int]}
    """
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


def uncovered_minterms(minterms: List[int], prime_implicants: dict, 
                       essencial_pis: dict) -> bool:
    """
    Checks whether there are minterms not covered by the essencial prime implicants.
    :param minterms: list of minterms in decimal form.
    :param prime_implicants: dictionary of prime implicants.
    :param essencial_pis: dictionary of essencial prime implicants.
    :return bool: True if there are uncovered minterms
    """
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


def implicant_to_product(implicants: Iterable) -> str:
    """
    Transforms a list implicants into a sum of products.
    
    EX.:  implicants = [1--0, 0-10], return = AD' + A'CD'

    :param implicants: list of implicants.
    :return str: sum of products.
    """
    products = []
    for implicant in implicants:
        product = ''
        for j, bit in enumerate(implicant):
            if bit != '-':
                product += chr(65 + j)
                if bit == '0':
                    product += "'"
        products.append(product)
    return ' + '.join(products)
