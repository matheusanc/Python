imc = peso / (altura ** 2)
print('O IMC dessa pessoa é de {:.1f}'.format(imc))
if imc < 18.5:
    print('você está ABAIXO do peso normal')
elif 18.5 <= imc < 25:
    print('PARABÉNS, você está na faixa de PESO NORMAL')
elif 25 <= imc < 30:
    print('você está em SOBREPESO')
elif 30 <= imc < 40:
    print('você está em OBESIDADE')
elif imc >= 40:
    print('você está em OBESIDADE MÓRBIDA, cuidado')
