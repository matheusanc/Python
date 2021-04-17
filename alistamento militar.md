from datetime import date
atual = date.today().year
nasc = int(input('ano de nascimento: '))
idade = atual - nasc
print('quem nasceu em {} tem {} anos em {}'.format(nasc, idade, atual))
if idade == 18:
    print('você tem que alistar IMEDIATAMENTE!')
elif idade < 18:
    saldo = 18 - idade
    print('ainda faltam {} anos para o ALISTAMENTO'.format(saldo))
    ano = atual + saldo
    print('seu alistamento será em {}'.format(ano))
elif idade > 18:
    saldo = idade - 18
    print('você já deveria ter se alistado há {} anos'.format(saldo))
    ano = atual - saldo
    print('seu alistamento foi em {}'.format(ano))
