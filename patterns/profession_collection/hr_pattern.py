from patterns.data_pattern._data_pattern import pattern

hr = {
    'ma': pattern['hr']['ma'],
    'ma2': pattern['hr']['ma2'],
    'mdef': pattern['hr']['mdef'],
    'mex': pattern['hr']['mex'],
    'mex2': pattern['hr']['mex2'],
    'mincl': pattern['hr']['mincl'],
}

hr['sub'] = {}

# add mincl to mex
for sub_profession in hr['sub']:
    hr['sub'][sub_profession]['mex'] = set(hr['sub'][sub_profession]['mex']).union(set(hr['sub'][sub_profession]['mincl']))

# print(f"\n********************\n{frontend}\n****************\n")
print('\nGAME:')
for i in hr:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {hr[i]}")
    else:
        print('sub: ')
        for j in hr[i]:
            print(f"   * {j}: {hr[i][j]}")
