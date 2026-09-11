# Especificação: Sistema de cálculo de Frete

## Requisitos Funcionais
- **RF-01 (Event-Driven)**: WHEN o usuário calcular o frete e o carrinho atingir o limite regional, THE SYSTEM SHALL zerar o frete
- **RF-04 (Event-Driven)**: WHEN o usuário informar o CEP de entrega, THE SYSTEM SHALL calcular o valor do frete com base na região.
- **RF-06 (Event-Driven)**: WHEN o usuário alterar o endereço de entrega, THE SYSTEM SHALL recalcular o valor do frete.

## Regras de Negócio e Exceções
- **RB-02 (State-Driven)**: WHILE a região for 'Norte', o limite é R$300,00. Demais regiões: R$ 200,00

- **RB-03 (Unwanted Behavior)**: IF valor <=0, THEN exibir erro 'Valor de Carringo inválido'.

- **RB-05 (Unwanted Behavior)**: IF o CEP informado for inválido, THEN exibir erro "CEP inválido".
