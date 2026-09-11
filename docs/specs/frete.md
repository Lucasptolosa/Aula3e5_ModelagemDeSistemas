RF-01: WHEN o usuário calcular o frete e o carrinho atingir o limite regional, THE SYSTEM SHALL zerar o frete

RB-02: WHILE a região for 'Norte', o limite é R$300,00. Demais regiões: R$ 200,00

RB-03: IF valor <=0, THEN exibir erro 'Valor de Carringo inválido'.

RF-04: WHEN o usuário informar o CEP de entrega, THE SYSTEM SHALL calcular o valor do frete com base na região.

RB-05: IF o CEP informado for inválido, THEN exibir erro "CEP inválido".

RF-06: WHEN o usuário alterar o endereço de entrega, THE SYSTEM SHALL recalcular o valor do frete.