from patterns.data_pattern._data_pattern import pattern

game = {
    'ma': pattern['game']['ma'],
    'ma2': pattern['game']['ma2'],
    'mdef': pattern['game']['mdef'],
    'mex': pattern['game']['mex'],
    'mex2': pattern['game']['mex2'],
    'mincl': pattern['game']['mincl'],
}

game['sub'] = {}

# print(f"\n********************\n{frontend}\n****************\n")
print('\nGAME:')
for i in game:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {game[i]}")
    else:
        print('sub: ')
        for j in game[i]:
            print(f"   * {j}: {game[i][j]}")
