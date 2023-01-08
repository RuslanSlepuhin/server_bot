from patterns.data_pattern._data_pattern import pattern

backend = {
    'ma': pattern['backend']['ma'],
    'ma2': pattern['backend']['ma2'],
    'mdef': pattern['backend']['mdef'],
    'mex': pattern['backend']['mex'],
    'mex2': pattern['backend']['mex2'],
    'mincl': pattern['backend']['mincl'],
}

python = {
    'ma': pattern['backend']['sub']['python']['ma'],
    'ma2': pattern['backend']['sub']['python']['ma2'],
    'mdef': pattern['backend']['sub']['python']['mdef'],
    'mex': pattern['backend']['sub']['python']['mex'],
    'mex2': pattern['backend']['sub']['python']['mex2'],
    'mincl': pattern['backend']['sub']['python']['mincl'],
}
python['mex'] = set(backend['mex']).union(set(python['mex2']))

c = {
    'ma': pattern['backend']['sub']['c']['ma'],
    'ma2': pattern['backend']['sub']['c']['ma2'],
    'mdef': pattern['backend']['sub']['c']['mdef'],
    'mex': pattern['backend']['sub']['c']['mex'],
    'mex2': pattern['backend']['sub']['c']['mex2'],
    'mincl': pattern['backend']['sub']['c']['mincl'],
}
c['mex'] = set(backend['mex']).union(set(c['mex2']))

php = {
    'ma': pattern['backend']['sub']['php']['ma'],
    'ma2': pattern['backend']['sub']['php']['ma2'],
    'mdef': pattern['backend']['sub']['php']['mdef'],
    'mex': pattern['backend']['sub']['php']['mex'],
    'mex2': pattern['backend']['sub']['php']['mex2'],
    'mincl': pattern['backend']['sub']['php']['mincl'],
}
php['mex'] = set(backend['mex']).union(set(php['mex2']))

java = {
    'ma': pattern['backend']['sub']['java']['ma'],
    'ma2': pattern['backend']['sub']['java']['ma2'],
    'mdef': pattern['backend']['sub']['java']['mdef'],
    'mex': pattern['backend']['sub']['java']['mex'],
    'mex2': pattern['backend']['sub']['java']['mex2'],
    'mincl': pattern['backend']['sub']['java']['mincl'],
}
java['mex'] = set(backend['mex']).union(set(java['mex2']))

ruby = {
    'ma': pattern['backend']['sub']['ruby']['ma'],
    'ma2': pattern['backend']['sub']['ruby']['ma2'],
    'mdef': pattern['backend']['sub']['ruby']['mdef'],
    'mex': pattern['backend']['sub']['ruby']['mex'],
    'mex2': pattern['backend']['sub']['ruby']['mex2'],
    'mincl': pattern['backend']['sub']['ruby']['mincl'],
}
ruby['mex'] = set(backend['mex']).union(set(ruby['mex2']))

scala = {
    'ma': pattern['backend']['sub']['scala']['ma'],
    'ma2': pattern['backend']['sub']['scala']['ma2'],
    'mdef': pattern['backend']['sub']['scala']['mdef'],
    'mex': pattern['backend']['sub']['scala']['mex'],
    'mex2': pattern['backend']['sub']['scala']['mex2'],
    'mincl': pattern['backend']['sub']['scala']['mincl'],
}
scala['mex'] = set(backend['mex']).union(set(scala['mex2']))

net = {
    'ma': pattern['backend']['sub']['net']['ma'],
    'ma2': pattern['backend']['sub']['net']['ma2'],
    'mdef': pattern['backend']['sub']['net']['mdef'],
    'mex': pattern['backend']['sub']['net']['mex'],
    'mex2': pattern['backend']['sub']['net']['mex2'],
    'mincl': pattern['backend']['sub']['net']['mincl'],
}
net['mex'] = set(backend['mex']).union(set(net['mex2']))

nodejs = {
    'ma': pattern['backend']['sub']['nodejs']['ma'],
    'ma2': pattern['backend']['sub']['nodejs']['ma2'],
    'mdef': pattern['backend']['sub']['nodejs']['mdef'],
    'mex': pattern['backend']['sub']['nodejs']['mex'],
    'mex2': pattern['backend']['sub']['nodejs']['mex2'],
    'mincl': pattern['backend']['sub']['nodejs']['mincl'],
}
nodejs['mex'] = set(backend['mex']).union(set(nodejs['mex2']))

laravel = {
    'ma': pattern['backend']['sub']['laravel']['ma'],
    'ma2': pattern['backend']['sub']['laravel']['ma2'],
    'mdef': pattern['backend']['sub']['laravel']['mdef'],
    'mex': pattern['backend']['sub']['laravel']['mex'],
    'mex2': pattern['backend']['sub']['laravel']['mex2'],
    'mincl': pattern['backend']['sub']['laravel']['mincl'],
}
laravel['mex'] = set(backend['mex']).union(set(laravel['mex2']))

golang = {
    'ma': pattern['backend']['sub']['golang']['ma'],
    'ma2': pattern['backend']['sub']['golang']['ma2'],
    'mdef': pattern['backend']['sub']['golang']['mdef'],
    'mex': pattern['backend']['sub']['golang']['mex'],
    'mex2': pattern['backend']['sub']['golang']['mex2'],
    'mincl': pattern['backend']['sub']['golang']['mincl'],
}
golang['mex'] = set(backend['mex']).union(set(golang['mex2']))

delphi = {
    'ma': pattern['backend']['sub']['delphi']['ma'],
    'ma2': pattern['backend']['sub']['delphi']['ma2'],
    'mdef': pattern['backend']['sub']['delphi']['mdef'],
    'mex': pattern['backend']['sub']['delphi']['mex'],
    'mex2': pattern['backend']['sub']['delphi']['mex2'],
    'mincl': pattern['backend']['sub']['delphi']['mincl'],
}
delphi['mex'] = set(backend['mex']).union(set(delphi['mex2']))

abap = {
    'ma': pattern['backend']['sub']['abap']['ma'],
    'ma2': pattern['backend']['sub']['abap']['ma2'],
    'mdef': pattern['backend']['sub']['abap']['mdef'],
    'mex': pattern['backend']['sub']['abap']['mex'],
    'mex2': pattern['backend']['sub']['abap']['mex2'],
    'mincl': pattern['backend']['sub']['abap']['mincl'],
}
abap['mex'] = set(backend['mex']).union(set(abap['mex2']))

ml = {
    'ma': pattern['backend']['sub']['ml']['ma'],
    'ma2': pattern['backend']['sub']['ml']['ma2'],
    'mdef': pattern['backend']['sub']['ml']['mdef'],
    'mex': pattern['backend']['sub']['ml']['mex'],
    'mex2': pattern['backend']['sub']['ml']['mex2'],
    'mincl': pattern['backend']['sub']['ml']['mincl'],
}
ml['mex'] = set(backend['mex']).union(set(ml['mex2']))

data_engineer = {
    'ma': pattern['backend']['sub']['data_engineer']['ma'],
    'ma2': pattern['backend']['sub']['data_engineer']['ma2'],
    'mdef': pattern['backend']['sub']['data_engineer']['mdef'],
    'mex': pattern['backend']['sub']['data_engineer']['mex'],
    'mex2': pattern['backend']['sub']['data_engineer']['mex2'],
    'mincl': pattern['backend']['sub']['data_engineer']['mincl'],
}
data_engineer['mex'] = set(backend['mex']).union(set(data_engineer['mex2']))

unity = {
    'ma': pattern['backend']['sub']['unity']['ma'],
    'ma2': pattern['backend']['sub']['unity']['ma2'],
    'mdef': pattern['backend']['sub']['unity']['mdef'],
    'mex': pattern['backend']['sub']['unity']['mex'],
    'mex2': pattern['backend']['sub']['unity']['mex2'],
    'mincl': pattern['backend']['sub']['unity']['mincl'],
}
unity['mex'] = set(backend['mex']).union(set(unity['mex2']))

one_c = {
    'ma': pattern['backend']['sub']['one_c']['ma'],
    'ma2': pattern['backend']['sub']['one_c']['ma2'],
    'mdef': pattern['backend']['sub']['one_c']['mdef'],
    'mex': pattern['backend']['sub']['one_c']['mex'],
    'mex2': pattern['backend']['sub']['one_c']['mex2'],
    'mincl': pattern['backend']['sub']['one_c']['mincl'],
}
one_c['mex'] = set(backend['mex']).union(set(one_c['mex2']))

embedded = {
    'ma': pattern['backend']['sub']['embedded']['ma'],
    'ma2': pattern['backend']['sub']['embedded']['ma2'],
    'mdef': pattern['backend']['sub']['embedded']['mdef'],
    'mex': pattern['backend']['sub']['embedded']['mex'],
    'mex2': pattern['backend']['sub']['embedded']['mex2'],
    'mincl': pattern['backend']['sub']['embedded']['mincl'],
}
embedded['mex'] = set(backend['mex']).union(set(embedded['mex2']))

backend['ma']=set(python['ma']).union(set(c['ma'])).union(set(php['ma'])).union(set(java['ma']))\
    .union(set(ruby['ma'])).union(set(scala['ma'])).union(set(net['ma'])).union(set(nodejs['ma']))\
    .union(set(laravel['ma'])).union(set(golang['ma'])).union(set(delphi['ma'])).union(set(abap['ma']))\
    .union(set(ml['ma'])).union(set(data_engineer['ma']))

backend['sub'] = {
    'python': python,
    'c': c,
    'php': php,
    'java': java,
    'ruby': ruby,
    'scala': scala,
    'net': net,
    'nodejs': nodejs,
    'laravel': laravel,
    'golang': golang,
    'delphi': delphi,
    'abap': abap,
    'ml': ml,
    'data_engineer': data_engineer,
    'unity': unity,
    'one_c': one_c,
    'embedded': embedded
}
# print(f"\n********************\n{backend}\n****************\n")
print('\nBACKEND')
for i in backend:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {backend[i]}")
    else:
        print('sub: ')
        for j in backend[i]:
            print(f"   * {j}: {backend[i][j]}")

