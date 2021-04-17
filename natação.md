idade = atual - nascimento
print('o atleta tem {} anos'.format(idade))
if idade <= 9:
    print('classificação: MIRIM')
elif idade <= 14:
    print('classificação: INFANTIL')
elif idade <= 19:
    print('classificação: JUNIOR')
elif idade <= 25:
    print('clasificação: SÊNIOR')
else:
    print('classificação: MASTER')
