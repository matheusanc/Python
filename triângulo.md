r1 = float(input('primeiro segmento: '))
r2 = float(input('segundo segmento: '))
r3 = float(input('terceiro segmento: '))
if r1 < r2 + r3 and r2 < r1 + r3 and r3 < r1 + r2:
    print('os segmentos acima PODEM FORMAR um triângulo ',end='')
    if r1 == r2 == r3:
        print('EQUILÁTERO')
    elif r1 != r2 != r3 :
        print('ESCALENO')
    else:
        print('ISÓSCELES')
else:
    print('os segmentos acima NÃO PODEM FORMAR triângulo!')
