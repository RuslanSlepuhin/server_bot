from patterns.data_pattern._data_pattern import pattern

pm = {
    'ma': pattern['pm']['ma'],
    'ma2': pattern['pm']['ma2'],
    'mdef': pattern['pm']['mdef'],
    'mex': pattern['pm']['mex'],
    'mex2': pattern['pm']['mex2'],
    'mincl': pattern['pm']['mincl'],
}

project = {
    'ma': pattern['pm']['sub']['project']['ma'],
    'ma2': pattern['pm']['sub']['project']['ma2'],
    'mdef': pattern['pm']['sub']['project']['mdef'],
    'mex': pattern['pm']['sub']['project']['mex'],
    'mex2': pattern['pm']['sub']['project']['mex2'],
    'mincl': pattern['pm']['sub']['project']['mincl'],
}

product = {
    'ma': pattern['pm']['sub']['product']['ma'],
    'ma2': pattern['pm']['sub']['product']['ma2'],
    'mdef': pattern['pm']['sub']['product']['mdef'],
    'mex': pattern['pm']['sub']['product']['mex'],
    'mex2': pattern['pm']['sub']['product']['mex2'],
    'mincl': pattern['pm']['sub']['product']['mincl'],
}
product['mex'] = set(pm['mex2']).union(set(product['mex2']))
project['mex'] = set(pm['mex2']).union(set(project['mex2']))
pm['ma'] = set(project['mdef']).union(set(pm['mincl'])).union(set(product['mdef']))


pm['sub'] = {
    'project': project,
    'product': product
}
# print(f"\n********************\n{backend}\n****************\n")

print('\nPM')
for i in pm:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {pm[i]}")
    else:
        print('sub: ')
        for j in pm[i]:
            print(f"   * {j}: {pm[i][j]}")