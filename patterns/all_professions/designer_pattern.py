from patterns.data_pattern._data_pattern import pattern

designer = {
    'ma': pattern['designer']['ma'],
    'ma2': pattern['designer']['ma2'],
    'mdef': pattern['designer']['mdef'],
    'mex': pattern['designer']['mex'],
    'mex2': pattern['designer']['mex2'],
    'mincl': pattern['designer']['mincl'],
}

ui_ux = {
    'ma': pattern['designer']['sub']['ui_ux']['ma'],
    'ma2': pattern['designer']['sub']['ui_ux']['ma2'],
    'mdef': pattern['designer']['sub']['ui_ux']['mdef'],
    'mex': pattern['designer']['sub']['ui_ux']['mex'],
    'mex2': pattern['designer']['sub']['ui_ux']['mex2'],
    'mincl': pattern['designer']['sub']['ui_ux']['mincl'],
}
ui_ux['mex'] = set(designer['mex']).union(set(ui_ux['mex2']))

motion = {
    'ma': pattern['designer']['sub']['motion']['ma'],
    'ma2': pattern['designer']['sub']['motion']['ma2'],
    'mdef': pattern['designer']['sub']['motion']['mdef'],
    'mex': pattern['designer']['sub']['motion']['mex'],
    'mex2': pattern['designer']['sub']['motion']['mex2'],
    'mincl': pattern['designer']['sub']['motion']['mincl'],
}
motion['mex'] = set(designer['mex']).union(set(motion['mex2']))

dd = {
    'ma': pattern['designer']['sub']['dd']['ma'],
    'ma2': pattern['designer']['sub']['dd']['ma2'],
    'mdef': pattern['designer']['sub']['dd']['mdef'],
    'mex': pattern['designer']['sub']['dd']['mex'],
    'mex2': pattern['designer']['sub']['dd']['mex2'],
    'mincl': pattern['designer']['sub']['dd']['mincl'],
}
dd['mex'] = set(designer['mex']).union(set(dd['mex2']))

ddd = {
    'ma': pattern['designer']['sub']['ddd']['ma'],
    'ma2': pattern['designer']['sub']['ddd']['ma2'],
    'mdef': pattern['designer']['sub']['ddd']['mdef'],
    'mex': pattern['designer']['sub']['ddd']['mex'],
    'mex2': pattern['designer']['sub']['ddd']['mex2'],
    'mincl': pattern['designer']['sub']['ddd']['mincl'],
}
ddd['mex'] = set(designer['mex']).union(set(ddd['mex2']))

game_designer = {
    'ma': pattern['designer']['sub']['game_designer']['ma'],
    'ma2': pattern['designer']['sub']['game_designer']['ma2'],
    'mdef': pattern['designer']['sub']['game_designer']['mdef'],
    'mex': pattern['designer']['sub']['game_designer']['mex'],
    'mex2': pattern['designer']['sub']['game_designer']['mex2'],
    'mincl': pattern['designer']['sub']['game_designer']['mincl'],
}
game_designer['mex'] = set(designer['mex']).union(set(game_designer['mex2']))

illustrator = {
    'ma': pattern['designer']['sub']['illustrator']['ma'],
    'ma2': pattern['designer']['sub']['illustrator']['ma2'],
    'mdef': pattern['designer']['sub']['illustrator']['mdef'],
    'mex': pattern['designer']['sub']['illustrator']['mex'],
    'mex2': pattern['designer']['sub']['illustrator']['mex2'],
    'mincl': pattern['designer']['sub']['illustrator']['mincl'],
}
illustrator['mex'] = set(designer['mex']).union(set(illustrator['mex2']))

graphic = {
    'ma': pattern['designer']['sub']['graphic']['ma'],
    'ma2': pattern['designer']['sub']['graphic']['ma2'],
    'mdef': pattern['designer']['sub']['graphic']['mdef'],
    'mex': pattern['designer']['sub']['graphic']['mex'],
    'mex2': pattern['designer']['sub']['graphic']['mex2'],
    'mincl': pattern['designer']['sub']['graphic']['mincl'],
}
graphic['mex'] = set(designer['mex']).union(set(graphic['mex2']))

uxre_searcher = {
    'ma': pattern['designer']['sub']['uxre_searcher']['ma'],
    'ma2': pattern['designer']['sub']['uxre_searcher']['ma2'],
    'mdef': pattern['designer']['sub']['uxre_searcher']['mdef'],
    'mex': pattern['designer']['sub']['uxre_searcher']['mex'],
    'mex2': pattern['designer']['sub']['uxre_searcher']['mex2'],
    'mincl': pattern['designer']['sub']['uxre_searcher']['mincl'],
}
uxre_searcher['mex'] = set(designer['mex']).union(set(uxre_searcher['mex2']))



designer['sub'] = {
    'ui_ux': ui_ux,
    'motion': motion,
    'dd': dd,
    'ddd': ddd,
    'game_designer': game_designer,
    'illustrator': illustrator,
    'graphic': graphic,
    'uxre_searcher': uxre_searcher
}
# print(f"\n********************\n{backend}\n****************\n")

print('\nDESIGNER')
for i in designer:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {designer[i]}")
    else:
        print('sub: ')
        for j in designer[i]:
            print(f"   * {j}: {designer[i][j]}")