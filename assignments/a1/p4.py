def opt_dist(bits, d):
    d = int(d)
    bits = [int(i) for i in str(bits)]
    bits_0 =[0]*len(bits)
    start_positions = [i for i in range(len(bits) - d + 1)]
    combinations = []
    steps = []
    for pos in start_positions:
        combination = bits_0.copy()
        combination[pos:pos+d] = [1]*d
        combinations.append(combination)
    for i in combinations:
        if i[0]==1:
                continue
        step = 0
        for j in range(len(bits_0)):
            if i[j]!=bits[j]:
                step+=1
        steps.append(step)
    return min(steps)
    

'''
    '0010001000 5\n'
    '0010001000 4\n'
    '0010001000 3\n'
    '0010001000 2\n'
    '0010001000 1\n'
    '0010001000 0\n'
    '0010101000 5\n'
    '0010101000 4\n'
    '0010101000 3\n'
    '0010101000 2\n'
    '0010101000 1\n'
    '0010101000 0\n',
'out': '3\n4\n3\n2\n1\n2\n2\n3\n2\n3\n2\n3\n'
'''


