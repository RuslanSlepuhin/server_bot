
detailed_designer = {
    'ma': (),
    'ma2': (),
    'mdef': (),
    'mex': (),
    'mex2': (),
    'mincl': ()
}

detailed_designer['sub'] = {}

print('\nDETAILED DESIGNER:')
for i in detailed_designer:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {detailed_designer[i]}")
    else:
        print('sub: ')
        for j in detailed_designer[i]:
            print(f"   * {j}: {detailed_designer[i][j]}")

