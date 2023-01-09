from patterns.data_pattern._data_pattern import pattern

mobile = {
    'ma': pattern['mobile']['ma'],
    'ma2': pattern['mobile']['ma2'],
    'mdef': pattern['mobile']['mdef'],
    'mex': pattern['mobile']['mex'],
    'mex2': pattern['mobile']['mex2'],
    'mincl': pattern['mobile']['mincl'],
}
mobile['ma'] = set(mobile['ma2']).union(set(mobile['mdef']))

ios = {
    'ma': pattern['mobile']['sub']['ios']['ma'],
    'ma2': pattern['mobile']['sub']['ios']['ma2'],
    'mdef': pattern['mobile']['sub']['ios']['mdef'],
    'mex': pattern['mobile']['sub']['ios']['mex'],
    'mex2': pattern['mobile']['sub']['ios']['mex2'],
    'mincl': pattern['mobile']['sub']['ios']['mincl'],
}
ios['mex'] = set(mobile['mex']).union(set(ios['mex2']))

android = {
    'ma': pattern['mobile']['sub']['android']['ma'],
    'ma2': pattern['mobile']['sub']['android']['ma2'],
    'mdef': pattern['mobile']['sub']['android']['mdef'],
    'mex': pattern['mobile']['sub']['android']['mex'],
    'mex2': pattern['mobile']['sub']['android']['mex2'],
    'mincl': pattern['mobile']['sub']['android']['mincl'],
}
android['mex'] = set(mobile['mex']).union(set(android['mex2']))

flutter = {
    'ma': pattern['mobile']['sub']['flutter']['ma'],
    'ma2': pattern['mobile']['sub']['flutter']['ma2'],
    'mdef': pattern['mobile']['sub']['flutter']['mdef'],
    'mex': pattern['mobile']['sub']['flutter']['mex'],
    'mex2': pattern['mobile']['sub']['flutter']['mex2'],
    'mincl': pattern['mobile']['sub']['flutter']['mincl'],
}
flutter['mex'] = set(mobile['mex']).union(set(flutter['mex2']))

react_native = {
    'ma': pattern['mobile']['sub']['react_native']['ma'],
    'ma2': pattern['mobile']['sub']['react_native']['ma2'],
    'mdef': pattern['mobile']['sub']['react_native']['mdef'],
    'mex': pattern['mobile']['sub']['react_native']['mex'],
    'mex2': pattern['mobile']['sub']['react_native']['mex2'],
    'mincl': pattern['mobile']['sub']['react_native']['mincl'],
}
react_native['mex'] = set(mobile['mex']).union(set(react_native['mex2']))

cross_mobile = {
    'ma': pattern['mobile']['sub']['cross_mobile']['ma'],
    'ma2': pattern['mobile']['sub']['cross_mobile']['ma2'],
    'mdef': pattern['mobile']['sub']['cross_mobile']['mdef'],
    'mex': pattern['mobile']['sub']['cross_mobile']['mex'],
    'mex2': pattern['mobile']['sub']['cross_mobile']['mex2'],
    'mincl': pattern['mobile']['sub']['cross_mobile']['mincl'],
}
cross_mobile['mex'] = set(mobile['mex']).union(set(cross_mobile['mex2']))
cross_mobile['ma'] = set(cross_mobile['ma2']).union(set(flutter['ma'])).union(set(react_native['ma']))


mobile['sub'] = {
    'ios': ios,
    'android': android,
    'cross_mobile': cross_mobile,
    'flutter': flutter,
    'react_native': react_native
}
# print(f"\n********************\n{backend}\n****************\n")

print('\nMOBILE')
for i in mobile:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {mobile[i]}")
    else:
        print('sub: ')
        for j in mobile[i]:
            print(f"   * {j}: {mobile[i][j]}")