import qm_method as qm
import petricks_method as pm
import canonical_sop as cn

if __name__ == '__main__':
    num_variables = int(input('Número de variáveis: '))
    minterms = input('Informe os mintermos separados por espaço: ')
    minterms = minterms.strip().split()
    if not minterms or len(minterms) >= 2**num_variables:
        print('entrada inválida!')
        exit()
    minterms = [int(minterm) for minterm in minterms]
    minterms.sort()
    minterms_bin = qm.minterm_to_binary(num_variables, minterms)
    groups = qm.create_groups(minterms_bin)

    prime_implicants = qm.prime_implicants(groups, minterms_bin)
    essencial_prime_implicants = qm.essencial_prime_implicants(prime_implicants, minterms)

    expression = qm.implicant_to_product(essencial_prime_implicants)

    uncovered_minterms = qm.uncovered_minterms(minterms, prime_implicants,
                                            essencial_prime_implicants)
    
    canonical_sop = cn.canonical_sop(minterms_bin)
    print(f'\nSoma de produtos canonica:\nX = {canonical_sop}')
    print('\nForma(s) reduzidas(s):')
    if uncovered_minterms:
        for i, key in enumerate(prime_implicants.copy()):
            new_key = (chr(65 + num_variables + i), key)
            prime_implicants[new_key] = prime_implicants.pop(key)
            
        petricks_minterms = pm.petricks_method(prime_implicants)

        for minterm in petricks_minterms:
            final_expression = [expression] if expression else []
            for term in minterm:
                for key in prime_implicants:
                    if term in key:
                        final_expression.append(''.join(qm.implicant_to_product([key[1]])))
            print(f"X = {' + '.join(final_expression)}")
    else:
        print(f'\nX = {expression}')