casa = float(input('valor da casa: R$'))
salário = float(input('salário do comprador: R$'))
anos = int(input('quantos anos de financiamento? '))
prestação = casa / (anos * 12)
mínimo = salário * 30 / 100
print('para pagar uma casa de R${:.2f} em {} anos'.format(casa, anos), end='')
print(' a prestação será de R${:.2f}'.format(prestação))
print('COMPARANDO tem que pagar {} e o mínimo é de {}'.format(prestação, mínimo))
if prestação <= mínimo:
    print('empréstimo pode ser CONCEDIDO!')
else:
    print('empréstimo NEGADO!')
