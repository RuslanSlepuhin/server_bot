from patterns.all_professions.analyst_pattern import analyst

ba = analyst

print('\nDETAILED DESIGNER:')
for i in ba:
    if i in ['mex', 'mex2', 'ma', 'ma2', 'mdef', 'mincl']:
        print(f"{i}: {ba[i]}")
    else:
        print('sub: ')
        for j in ba[i]:
            print(f"   * {j}: {ba[i][j]}")

