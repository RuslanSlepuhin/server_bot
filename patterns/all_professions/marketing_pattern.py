from patterns.data_pattern._data_pattern import pattern

marketing = {
    'ma': pattern['marketing']['ma'],
    'ma2': pattern['marketing']['ma2'],
    'mdef': pattern['marketing']['mdef'],
    'mex': pattern['marketing']['mex'],
    'mex2': pattern['marketing']['mex2'],
    'mincl': pattern['marketing']['mincl'],
}

smm = {
    'ma': pattern['marketing']['sub']['smm']['ma'],
    'ma2': pattern['marketing']['sub']['smm']['ma2'],
    'mdef': pattern['marketing']['sub']['smm']['mdef'],
    'mex': pattern['marketing']['sub']['smm']['mex'],
    'mex2': pattern['marketing']['sub']['smm']['mex2'],
    'mincl': pattern['marketing']['sub']['smm']['mincl'],
}
smm['mex'] = set(marketing['mex']).union(set(smm['mex2']))

copyrighter = {
    'ma': pattern['marketing']['sub']['copyrighter']['ma'],
    'ma2': pattern['marketing']['sub']['copyrighter']['ma2'],
    'mdef': pattern['marketing']['sub']['copyrighter']['mdef'],
    'mex': pattern['marketing']['sub']['copyrighter']['mex'],
    'mex2': pattern['marketing']['sub']['copyrighter']['mex2'],
    'mincl': pattern['marketing']['sub']['copyrighter']['mincl'],
}
copyrighter['mex'] = set(marketing['mex']).union(set(copyrighter['mex2']))

seo = {
    'ma': pattern['marketing']['sub']['seo']['ma'],
    'ma2': pattern['marketing']['sub']['seo']['ma2'],
    'mdef': pattern['marketing']['sub']['seo']['mdef'],
    'mex': pattern['marketing']['sub']['seo']['mex'],
    'mex2': pattern['marketing']['sub']['seo']['mex2'],
    'mincl': pattern['marketing']['sub']['seo']['mincl'],
}
seo['mex'] = set(marketing['mex']).union(set(seo['mex2']))

link_builder = {
    'ma': pattern['marketing']['sub']['link_builder']['ma'],
    'ma2': pattern['marketing']['sub']['link_builder']['ma2'],
    'mdef': pattern['marketing']['sub']['link_builder']['mdef'],
    'mex': pattern['marketing']['sub']['link_builder']['mex'],
    'mex2': pattern['marketing']['sub']['link_builder']['mex2'],
    'mincl': pattern['marketing']['sub']['link_builder']['mincl'],
}
link_builder['mex'] = set(marketing['mex']).union(set(link_builder['mex2']))

media_buyer = {
    'ma': pattern['marketing']['sub']['media_buyer']['ma'],
    'ma2': pattern['marketing']['sub']['media_buyer']['ma2'],
    'mdef': pattern['marketing']['sub']['media_buyer']['mdef'],
    'mex': pattern['marketing']['sub']['media_buyer']['mex'],
    'mex2': pattern['marketing']['sub']['media_buyer']['mex2'],
    'mincl': pattern['marketing']['sub']['media_buyer']['mincl'],
}
media_buyer['mex'] = set(marketing['mex']).union(set(media_buyer['mex2']))

email_marketer = {
    'ma': pattern['marketing']['sub']['email_marketer']['ma'],
    'ma2': pattern['marketing']['sub']['email_marketer']['ma2'],
    'mdef': pattern['marketing']['sub']['email_marketer']['mdef'],
    'mex': pattern['marketing']['sub']['email_marketer']['mex'],
    'mex2': pattern['marketing']['sub']['email_marketer']['mex2'],
    'mincl': pattern['marketing']['sub']['email_marketer']['mincl'],
}
email_marketer['mex'] = set(marketing['mex']).union(set(email_marketer['mex2']))

context = {
    'ma': pattern['marketing']['sub']['context']['ma'],
    'ma2': pattern['marketing']['sub']['context']['ma2'],
    'mdef': pattern['marketing']['sub']['context']['mdef'],
    'mex': pattern['marketing']['sub']['context']['mex'],
    'mex2': pattern['marketing']['sub']['context']['mex2'],
    'mincl': pattern['marketing']['sub']['context']['mincl'],
}
context['mex'] = set(marketing['mex']).union(set(context['mex2']))

content_manager = {
    'ma': pattern['marketing']['sub']['content_manager']['ma'],
    'ma2': pattern['marketing']['sub']['content_manager']['ma2'],
    'mdef': pattern['marketing']['sub']['content_manager']['mdef'],
    'mex': pattern['marketing']['sub']['content_manager']['mex'],
    'mex2': pattern['marketing']['sub']['content_manager']['mex2'],
    'mincl': pattern['marketing']['sub']['content_manager']['mincl'],
}
content_manager['mex'] = set(marketing['mex']).union(set(content_manager['mex2']))

tech_writer = {
    'ma': pattern['marketing']['sub']['tech_writer']['ma'],
    'ma2': pattern['marketing']['sub']['tech_writer']['ma2'],
    'mdef': pattern['marketing']['sub']['tech_writer']['mdef'],
    'mex': pattern['marketing']['sub']['tech_writer']['mex'],
    'mex2': pattern['marketing']['sub']['tech_writer']['mex2'],
    'mincl': pattern['marketing']['sub']['tech_writer']['mincl'],
}
tech_writer['mex'] = set(marketing['mex']).union(set(tech_writer['mex2']))

marketing['sub'] = {
    'smm': smm,
    'copyrighter': copyrighter,
    'seo': seo,
    'link_builder': link_builder,
    'media_buyer': media_buyer,
    'email_marketer': email_marketer,
    'context': context,
    'content_manager': content_manager,
    'tech_writer': tech_writer,
}

# print(f"\n********************\n{frontend}\n****************\n")
print('\nMARKETING:')
for i in marketing:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {marketing[i]}")
    else:
        print('sub: ')
        for j in marketing[i]:
            print(f"   * {j}: {marketing[i][j]}")
