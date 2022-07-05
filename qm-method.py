from utils import *


def create_groups(minterms: List[str]) -> dict:
    """
    Creates a dictionary in witch the keys represent the number of '1's and the 
    values are the minterms that contain such number of '1's.
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

if __name__ == '__main__':
    num_variables = int(input('Número de variáveis: '))
    minterms = input('Informe os mintermos separados por espaço: ')
    minterms = minterms.strip().split()
    minterms = [int(minterm) for minterm in minterms]
    minterms.sort()
    
    minterms_bin = minterm_to_binary(num_variables, minterms)

    groups = create_groups(minterms_bin)
    print(groups)
    