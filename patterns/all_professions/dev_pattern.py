from patterns.data_pattern._data_pattern import pattern

dev = {
    'ma': pattern['analyst']['ma'],
    'ma2': pattern['analyst']['ma2'],
    'mdef': pattern['analyst']['mdef'],
    'mex': pattern['analyst']['mex'],
    'mex2': pattern['analyst']['mex2'],
    'mincl': pattern['analyst']['mincl'],
}

dev['sub'] = {}

# print(f"\n********************\n{backend}\n****************\n")

print('\nDEV')
for i in dev:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {dev[i]}")
    else:
        print('sub: ')
        for j in dev[i]:
            print(f"   * {j}: {dev[i][j]}")

