from patterns.pseudo_pattern.fake_pattern import pattern

fullstack = {
    'ma': pattern['fullstack']['ma'],
    'ma2': pattern['fullstack']['ma2'],
    'mdef': pattern['fullstack']['mdef'],
    'mex': pattern['fullstack']['mex'],
    'mex2': pattern['fullstack']['mex2'],
    'mincl': pattern['fullstack']['mincl'],
}
fullstack['sub'] = {}

# add mincl to mex
for sub_profession in fullstack['sub']:
    fullstack['sub'][sub_profession]['mex'] = set(fullstack['sub'][sub_profession]['mex']).union(set(fullstack['sub'][sub_profession]['mincl']))
