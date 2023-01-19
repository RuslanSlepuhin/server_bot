from patterns.data_pattern._data_pattern import pattern

non_code_manager = {
    'ma': pattern['non_code_manager']['ma'],
    'ma2': pattern['non_code_manager']['ma2'],
    'mdef': pattern['non_code_manager']['mdef'],
    'mex': pattern['non_code_manager']['mex'],
    'mex2': pattern['non_code_manager']['mex2'],
    'mincl': pattern['non_code_manager']['mincl'],
}

non_code_manager['sub'] = {}

# add mincl to mex
for sub_profession in non_code_manager['sub']:
    non_code_manager['sub'][sub_profession]['mex'] = set(non_code_manager['sub'][sub_profession]['mex']).union(set(non_code_manager['sub'][sub_profession]['mincl']))

# print(f"\n********************\n{backend}\n****************\n")

print('\nSALES MANAGER')
for i in non_code_manager:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {non_code_manager[i]}")
    else:
        print('sub: ')
        for j in non_code_manager[i]:
            print(f"   * {j}: {non_code_manager[i][j]}")
