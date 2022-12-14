from patterns.data_pattern._data_pattern import pattern

devops = {
    'ma': pattern['devops']['ma'],
    'ma2': pattern['devops']['ma2'],
    'mdef': pattern['devops']['mdef'],
    'mex': pattern['devops']['mex'],
    'mex2': pattern['devops']['mex2'],
    'mincl': pattern['devops']['mincl'],
}

devops['sub'] = {}

# print(f"\n********************\n{backend}\n****************\n")

print('\nDEV')
for i in devops:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {devops[i]}")
    else:
        print('sub: ')
        for j in devops[i]:
            print(f"   * {j}: {devops[i][j]}")