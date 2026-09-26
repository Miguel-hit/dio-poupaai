# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Mapear interações prévias do cliente, resgatando dúvidas sobre produtos (CDB, Tesouro Selic) e o progresso da reserva de emergência |
| `perfil_investidor.json` | JSON | Definir a tolerância a risco e perfil do cliente para orientar sugestões de liquidez diária |
| `produtos_financeiros.json` | JSON | Fornecer a prateleira de produtos autorizados (CDB, Tesouro Selic) para alocação do saldo excedente |
| `transacoes.csv` | CSV | Analisar a receita mensal, categorizar as despesas (moradia, alimentação, transporte, saúde, lazer) e calcular o saldo livre disponível |

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos CSV são lidos em Python via biblioteca `pandas` durante a inicialização da aplicação.

Os dados são sumarizados e convertidos em texto estruturado mantido no estado da sessão.

---

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

O resumo consolidado do extrato financeiro e a linha do tempo do atendimento são injetados diretamente no **System Prompt** do agente antes do início da conversa.

Isso permite que a IA acesse os valores reais do cliente sem risco de alucinação.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente
- Nome: Cliente Fictício
- Mês de Referência: Outubro/2025

Resumo do Extrato
- Receita Total: R$ 5.000,00
- Despesas Totais: R$ 2.488,90
- Moradia (Aluguel, Luz): R$ 1.380,00
- Alimentação (Supermercado, Restaurante): R$ 570,00
- Transporte (Uber, Combustível): R$ 295,00
- Saúde (Farmácia, Academia): R$ 188,00
- Lazer (Netflix): R$ 55,90
- Saldo Livre para Investimento: R$ 2.511,10

Histórico de Atendimento Recente
- 15/09/2025: Consulta sobre rentabilidade e prazos de CDB (Resolvido).
- 01/10/2025: Explicação sobre funcionamento do Tesouro Selic (Resolvido).
- 12/10/2025: Acompanhamento do progresso da reserva de emergência (Resolvido).
...
```
