from utils import *


def canonical_sop(minterms_bin: List[str]) -> str:
    '''
    Generates the canonical sum of products based on the list of minterms.
    :param minterms: List of minterms in binary.
    :return c_sop: String. The canonical sum of products.
    '''
    for i, minterm in enumerate(minterms_bin):
        temp = ''
        for j, bit in enumerate(minterm):
            temp += chr(65+j)
            if bit == '0':
                temp += "'"
        minterms_bin[i] = temp

    c_sop = ' + '.join(minterms_bin)
    return c_sop


if __name__ == '__main__':
    num_variables = int(input('Número de variáveis: '))
    minterms = input('Informe os mintermos separados por espaço: ')
    minterms = minterms.strip().split()
    minterms = [int(minterm) for minterm in minterms]
    minterms.sort()

    minterms_bin = minterm_to_binary(num_variables, minterms)
    can_sop = canonical_sop(minterms_bin)
    
    print(f'\nX = {can_sop}')
