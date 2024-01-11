import json

with open("dados/clientes.json", "r") as arquivo:
    clientes = json.load(arquivo)

for key, value in clientes.items():
    for sub_key, sub_value in value.items():
        if sub_key == 'CPF' or sub_key == 'CNPJ':
            print(f'{sub_key}: {sub_value}')
