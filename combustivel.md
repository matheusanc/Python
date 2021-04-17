# Python
nome = input("Qual é o seu nome?")

gasto = float(input("{}, digite o tempo gasto na viagem (em horas): ".format(nome)))

velocidade = float(input('{}, digite agora a velocidade média praticado na viagem:'.format(nome)))

consumo = velocidade/12

print("Foram gastos ", consumo, " litros de combustível.")
