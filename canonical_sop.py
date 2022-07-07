from typing import List


def minterm_to_binary(num_bits, minterms: List[int]) -> List[str]:
    """
    Converts each number in the minterms list to binary.
    :param num_bits: Number of bits to represent the binary convertion.
    :param minterms: List of minterms in string format.
    :return minterms_bin: List of minterms in binary.
    """
    minterms = [format(int(minterm), f'0{num_bits}b') for minterm in minterms]

    return minterms


def canonical_sop(minterms_bin: List[str]) -> str:
    """
    Generates the canonical sum of products based on the list of minterms.
    :param minterms_bin: List of minterms in binary.
    :return c_sop: The canonical sum of products.
    """
    for i, minterm in enumerate(minterms_bin):
        temp = ''
        for j, bit in enumerate(minterm):
            temp += chr(65+j)
            if bit == '0':
                temp += "'"
        minterms_bin[i] = temp

    c_sop = ' + '.join(minterms_bin)
    return c_sop
