#conversão para números binário, octal ou hexadecimal

num = int(input('digite um número inteiro: '))
print('''escolha umas das bases para conversão:
[1] converter para BINÁRIO
[2] converter para OCTAL
[3] converter para HEXADECIMAL''')
opção = int(input('sua opção: '))
if opção == 1:
    print('{} covertido para BINÁRIO é igual a {}'.format(num, bin(num)[2:]))
elif opção == 2:
    print('{} conertido para OCTAL é igual a {}'.format(num, oct(num)[2:]))
elif opção == 3:
    print('{} convertido para HEXADECIMAL é igual a {}'.format(num, hex(num)[2:]))
else:
    print('opção inválida. Tente novamente')
