from typing import List

def minterm_to_binary(num_bits, minterms: List[str]) -> List[str]:
    """
    Converts each number in the minterms list to binary.
    :param num_bits: Number of bits to represent the binary convertion.
    :param minterms: List of minterms in string format.
    :return minterms_bin: List of minterms in binary.
    """
    minterms = [format(int(minterm), f'0{num_bits}b') for minterm in minterms]

    return minterms