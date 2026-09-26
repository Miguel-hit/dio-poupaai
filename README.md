# 💰 PoupaIA - Assistente Consultivo de Metas Financeiras

O **PoupaIA** é um agente financeiro inteligente desenvolvido em Python com IA Generativa local e interface gráfica em Streamlit. O agente atua de forma consultiva e proativa, analisando transações financeiras, categorizando despesas, calculando o saldo livre real do cliente e sugerindo a destinação desse excedente para a construção de uma **reserva de emergência** (em CDB ou Tesouro Selic com liquidez diária).

---

## 🛠️ Requisitos do Sistema e Apps Auxiliares

Para rodar o agente localmente em sua máquina, é necessário atender aos seguintes pré-requisitos:

### 1. Requisitos de Software
* **Python**: Versão `3.10` ou superior.
* **Pip**: Gerenciador de pacotes do Python.
* **Git**: Para clonar o repositório (opcional).

### 2. Aplicação Auxiliar: Ollama (LLM Local)
O agente utiliza o **Ollama** para executar o modelo de linguagem de forma local, garantindo privacidade dos dados financeiros e sem necessidade de chaves de API pagas.

* **Download do Ollama**: Baixe e instale o aplicativo oficial para o seu sistema operacional em [ollama.com](https://ollama.com/).
* **Modelo Utilizado**: `gpt-oss` (ou qualquer outro modelo local de sua preferência, como `llama3` ou `mistral`).

---

## 📦 Instalação e Configuração

Siga o passo a passo abaixo para configurar e executar o projeto:

### Passo 1: Iniciar e Baixar o Modelo no Ollama
Abra o seu terminal ou prompt de comando e execute o comando abaixo para baixar e testar o modelo `gpt-oss`:

```bash
ollama pull gpt-oss
```

> **Nota:** Certifique-se de que o serviço do Ollama esteja rodando em segundo plano (`ollama serve`).

---

### Passo 2: Clonar ou Acessar a Pasta do Repositório
Navegue até a pasta raiz do projeto:

```bash
cd dio-poupaai-main
```

---

### Passo 3: Criar um Ambiente Virtual (Recomendado)
É altamente recomendável utilizar um ambiente virtual em Python:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Linux/macOS:
source venv/bin/activate

# Ativar no Windows (Command Prompt):
venv\Scripts\activate

# Ativar no Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```

---

### Passo 4: Instalar as Dependências do Python
Com o ambiente virtual ativo, instale as bibliotecas necessárias listadas no arquivo `src/requirements.txt`:

```bash
pip install -r src/requirements.txt
```

#### 📋 Bibliotecas Principais (`src/requirements.txt`):
* **`streamlit`** (>= 1.30.0): Interface web interativa do chatbot e dashboard financeiro.
* **`pandas`** (>= 2.0.0): Leitura e processamento das bases de dados CSV.
* **`ollama`** (>= 0.1.6): Biblioteca cliente oficial para integração do Python com o modelo LLM no Ollama.
* **`python-dotenv`** (>= 1.0.0): Gerenciamento de variáveis de ambiente.

---

## 🚀 Como Executar o Agente

Com o Ollama rodando e as dependências instaladas, execute a aplicação Streamlit a partir da raiz do projeto:

```bash
streamlit run src/app.py
```

Após executar o comando, o navegador abrirá automaticamente no endereço:
👉 **`http://localhost:8501`**

---

## 📁 Estrutura do Repositório

```text
dio-poupaai-main/
│
├── 📄 README.md                        # Documentação principal e guia de instalação
│
├── 📁 data/                            # Bases de dados utilizadas pelo agente
│   ├── transacoes.csv                  # Extrato financeiro e categorias de gastos
│   ├── historico_atendimento.csv       # Histórico de interações prévias
│   ├── perfil_investidor.json          # Perfil de risco e preferências
│   └── produtos_financeiros.json       # Prateleira de produtos autorizados
│
├── 📁 docs/                            # Documentação técnica e estratégica
│   ├── 01-documentacao-agente.md       # Caso de uso, persona, arquitetura e segurança
│   ├── 02-base-conhecimento.md         # Estratégia de dados e contexto
│   └── 03-prompts.md                   # System Prompt, few-shot e edge cases
│
└── 📁 src/                             # Código-fonte da aplicação
    ├── app.py                          # Código principal do chatbot (Streamlit + Ollama)
    └── requirements.txt                # Dependências Python
```

---

## 🔍 Funcionalidades Principais

1. **Dashboard Orçamentário Lateral**:
   * Cálculo automático da Receita Total, Despesas Totais e Saldo Livre Disponível.
   * Detalhamento por categoria de gastos (Moradia, Alimentação, Transporte, Saúde, Lazer).
2. **Consultoria Proativa no Chat**:
   * O agente identifica automaticamente o saldo excedente e sugere a alocação em CDB ou Tesouro Selic para fortalecimento da reserva de emergência.
   * Integração do histórico prévio de atendimentos do cliente.
3. **Mecanismo Anti-Alucinação**:
   * Respostas ancoradas estritamente nos dados reais do cliente.
   * Recusa graciosa e educada para perguntas fora do escopo ou solicitações sensíveis.

---

## ⚠️ Solução de Problemas (Troubleshooting)

| Problema | Causa Provável | Solução |
| :--- | :--- | :--- |
| `ConnectionRefusedError` ou erro ao conectar com o Ollama | O serviço do Ollama não está ativo localmente. | Execute `ollama serve` no terminal para iniciar o serviço. |
| `model 'gpt-oss' not found` | O modelo não foi baixado previamente no Ollama. | Execute `ollama pull gpt-oss` no terminal. |
| `ModuleNotFoundError: No module named 'streamlit'` | As dependências não foram instaladas no ambiente ativo. | Garanta que o venv está ativado e rode `pip install -r src/requirements.txt`. |
| Erro de leitura dos arquivos `.csv` | O comando foi executado fora do diretório correto. | Execute `streamlit run src/app.py` a partir da raiz do repositório. |

---

## 📜 Licença e Créditos

Projeto desenvolvido como solução do desafio **Agente Financeiro Inteligente com IA Generativa** pela **DIO (Digital Innovation One)**.
