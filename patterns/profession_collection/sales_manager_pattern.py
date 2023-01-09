from patterns.data_pattern._data_pattern import pattern

sales_manager = {
    'ma': pattern['sales_manager']['ma'],
    'ma2': pattern['sales_manager']['ma2'],
    'mdef': pattern['sales_manager']['mdef'],
    'mex': pattern['sales_manager']['mex'],
    'mex2': pattern['sales_manager']['mex2'],
    'mincl': pattern['sales_manager']['mincl'],
}

sales_manager['sub'] = {}

# print(f"\n********************\n{backend}\n****************\n")

print('\nSALES MANAGER')
for i in sales_manager:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {sales_manager[i]}")
    else:
        print('sub: ')
        for j in sales_manager[i]:
            print(f"   * {j}: {sales_manager[i][j]}")