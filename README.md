# Python - Simulador de Caixa Eletrônico

## Equipe
- [Flávia Reis](https://github.com/flaviare1s)
- [Mariana](https://github.com/)
- [Miguel Rodrigues](https://github.com/)
- [Gabriel Andrade](https://github.com/Bieolzard)
- [Renato Costa](https://github.com/RenatinoCS)
- [Silvia Neves](https://github.com/SilviaNeves)


## Projeto feito no bootcamp de Análise de Dados da SoulCode Academy

### Desenvolvimento de um Simulador de Caixa Eletrônico em Python

#### Contexto
Em um mundo onde a digitalização dos serviços bancários é cada vez mais essencial, a necessidade de proporcionar uma experiência prática e segura para os usuários é uma prioridade. Bancos e instituições financeiras buscam maneiras eficientes de educar seus clientes sobre o uso de caixas eletrônicos e aplicativos bancários. Pensando nisso, um Simulador de Caixa Eletrônico pode ajudar tanto na educação financeira quanto na prática de programação.

#### Desafio
Desenvolver um Simulador de Caixa Eletrônico utilizando a linguagem de programação Python, capaz de realizar operações bancárias simples como consulta de saldo, depósitos, saques e verificação de extrato. O sistema deve garantir a segurança do usuário através da implementação de uma senha de acesso e limitar a quantidade de saques diários.

#### Tecnologias Utilizadas
- Python
- Flask
- HTML
- CSS

#### Requisitos Funcionais
O sistema deverá ter as seguintes funcionalidades:
 ##### Ver o saldo da conta:
- O usuário poderá consultar o saldo atual de sua conta a qualquer momento.
- O saldo inicial deve ser definido ao iniciar o programa e atualizado conforme transações realizadas.
 ##### Depositar um valor:
- O usuário poderá adicionar um valor à sua conta, aumentando o saldo disponível.
- Deve haver validação para garantir que o valor informado seja positivo.
- Sacar um valor:
 ##### O usuário poderá retirar um valor de sua conta, desde que haja saldo suficiente.
- O sistema deve verificar se o valor do saque não excede o saldo disponível.
- Ver o extrato das últimas transações:
- O usuário poderá visualizar um histórico das transações realizadas (depósitos e saques).
- O extrato deve mostrar o tipo de transação, o valor e a data/hora em que foi realizada.
 ##### Sair do sistema:
- Finalizar a execução do programa de forma segura, salvando o histórico de transações para consultas futuras.

#### Desafios Extras
 ##### Para tornar o sistema mais robusto e funcional, implemente as seguintes melhorias:
- Impedir saques acima do limite diário:
- Definir um limite máximo de saques por dia (ex: R$ 1.000,00).
- O sistema deve rastrear o total sacado no dia e impedir que o usuário exceda o limite definido.
 ##### Implementar uma senha de acesso ao sistema:
- Solicitar uma senha ao iniciar o programa para garantir a segurança do usuário.
- Permitir um número limitado de tentativas (ex: 3 tentativas) antes de bloquear o acesso.
- Utilizar uma senha padrão (ex: 1234) que pode ser alterada pelo usuário após o primeiro acesso.

