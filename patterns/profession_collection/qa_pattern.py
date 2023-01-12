from patterns.data_pattern._data_pattern import pattern

qa = {
    'ma': pattern['qa']['ma'],
    'ma2': pattern['qa']['ma2'],
    'mdef': pattern['qa']['mdef'],
    'mex': pattern['qa']['mex'],
    'mex2': pattern['qa']['mex2'],
    'mincl': pattern['qa']['mincl'],
}

manual_qa = {
    'ma': pattern['qa']['sub']['manual_qa']['ma'],
    'ma2': pattern['qa']['sub']['manual_qa']['ma2'],
    'mdef': pattern['qa']['sub']['manual_qa']['mdef'],
    'mex': pattern['qa']['sub']['manual_qa']['mex'],
    'mex2': pattern['qa']['sub']['manual_qa']['mex2'],
    'mincl': pattern['qa']['sub']['manual_qa']['mincl'],
}

aqa = {
    'ma': pattern['qa']['sub']['aqa']['ma'],
    'ma2': pattern['qa']['sub']['aqa']['ma2'],
    'mdef': pattern['qa']['sub']['aqa']['mdef'],
    'mex': pattern['qa']['sub']['aqa']['mex'],
    'mex2': pattern['qa']['sub']['aqa']['mex2'],
    'mincl': pattern['qa']['sub']['aqa']['mincl'],
}

support = {
    'ma': pattern['qa']['sub']['support']['ma'],
    'ma2': pattern['qa']['sub']['support']['ma2'],
    'mdef': pattern['qa']['sub']['support']['mdef'],
    'mex': pattern['qa']['sub']['support']['mex'],
    'mex2': pattern['qa']['sub']['support']['mex2'],
    'mincl': pattern['qa']['sub']['support']['mincl'],
}

qa['ma'] = set(manual_qa['ma']).union(set(aqa['ma'])).union(set(support['ma']))

qa['sub'] = {
    'manual_qa': manual_qa,
    'aqa': aqa,
    'support': support,
}
# print(f"\n********************\n{backend}\n****************\n")

print('\nQA')
for i in qa:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {qa[i]}")
    else:
        print('sub: ')
        for j in qa[i]:
            print(f"   * {j}: {qa[i][j]}")