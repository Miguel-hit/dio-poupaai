import os
import pathlib
import json
import pandas as pd
import streamlit as st
import ollama

# ==============================================================================
# 1. Configuração da Página do Streamlit
# ==============================================================================
st.set_page_config(
    page_title="PoupaIA - Assistente Consultivo de Metas Financeiras",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. Carregamento e Processamento da Base de Conhecimento (CSV & JSON)
# ==============================================================================
@st.cache_data
def load_data():
    """Procura e carrega os arquivos de dados (CSV e JSON) em pastas padrão."""
    base_dirs = [
        pathlib.Path("data"),
        pathlib.Path("../data"),
        pathlib.Path("."),
        pathlib.Path("/workspace/knowledge")
    ]
    
    trans_df = None
    hist_df = None
    perfil_json = None
    produtos_json = None
    
    for b_dir in base_dirs:
        # Transações CSV
        trans_path = b_dir / "transacoes.csv"
        if trans_path.exists() and trans_df is None:
            for enc in ["utf-8", "latin-1", "cp1252"]:
                try:
                    trans_df = pd.read_csv(trans_path, encoding=enc)
                    break
                except Exception:
                    continue

        # Histórico CSV
        hist_path = b_dir / "historico_atendimento.csv"
        if hist_path.exists() and hist_df is None:
            for enc in ["utf-8", "latin-1", "cp1252"]:
                try:
                    hist_df = pd.read_csv(hist_path, encoding=enc)
                    break
                except Exception:
                    continue

        # Perfil JSON
        perfil_path = b_dir / "perfil_investidor.json"
        if perfil_path.exists() and perfil_json is None:
            try:
                with open(perfil_path, "r", encoding="utf-8") as f:
                    perfil_json = json.load(f)
            except Exception:
                pass

        # Produtos JSON
        prod_path = b_dir / "produtos_financeiros.json"
        if prod_path.exists() and produtos_json is None:
            try:
                with open(prod_path, "r", encoding="utf-8") as f:
                    produtos_json = json.load(f)
            except Exception:
                pass
                
    return trans_df, hist_df, perfil_json, produtos_json

trans_df, hist_df, perfil_json, produtos_json = load_data()

# Helper para formatação de moeda BRL
def format_brl(val: float) -> str:
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Processamento de métricas financeiras
receita_total = 0.0
despesas_totais = 0.0
saldo_livre = 0.0
cat_summary = {}

if trans_df is not None:
    trans_df.columns = [c.strip().lower() for c in trans_df.columns]
    
    if 'valor' in trans_df.columns and 'tipo' in trans_df.columns:
        receita_df = trans_df[trans_df['tipo'].astype(str).str.lower().str.contains('entrada|receita', na=False)]
        despesa_df = trans_df[trans_df['tipo'].astype(str).str.lower().str.contains('saida|despesa', na=False)]
        
        receita_total = float(receita_df['valor'].sum())
        despesas_totais = float(despesa_df['valor'].sum())
        saldo_livre = receita_total - despesas_totais
        
        if 'categoria' in despesa_df.columns:
            cat_summary = despesa_df.groupby('categoria')['valor'].sum().to_dict()

# Formatação do contexto dinâmico para o System Prompt
context_lines = [
    f"- Receita Mensal Total: {format_brl(receita_total)}",
    f"- Despesas Totais: {format_brl(despesas_totais)}",
    f"- Saldo Livre Atual: {format_brl(saldo_livre)}"
]

if cat_summary:
    cat_str = "; ".join([f"{k.capitalize()}: {format_brl(v)}" for k, v in cat_summary.items()])
    context_lines.append(f"- Despesas por Categoria: {cat_str}")

if hist_df is not None:
    hist_df.columns = [c.strip().lower() for c in hist_df.columns]
    hist_items = []
    for _, row in hist_df.iterrows():
        d = row.get('data', '')
        t = row.get('tema', '')
        r = row.get('resumo', '')
        hist_items.append(f"  * {d} [{t}]: {r}")
    if hist_items:
        context_lines.append("- Histórico de Atendimento Prévio:\n" + "\n".join(hist_items))

if perfil_json:
    context_lines.append(f"- Perfil do Investidor: {json.dumps(perfil_json, ensure_ascii=False)}")

if produtos_json:
    context_lines.append(f"- Produtos Autorizados: {json.dumps(produtos_json, ensure_ascii=False)}")

context_data_str = "\n".join(context_lines)

# ==============================================================================
# 3. Definição do System Prompt do Agente
# ==============================================================================
SYSTEM_PROMPT = f"""Você é o PoupaIA, um assistente consultivo e proativo de metas financeiras especializado em organização orçamentária e construção de reserva de emergência.

SEU OBJETIVO:
Ajudar o cliente a organizar seu orçamento doméstico, analisar o saldo livre disponível no mês e orientar proativamente a alocação de excedentes financeiros em produtos de renda fixa com liquidez diária (CDB e Tesouro Selic) para fortalecimento da sua reserva de emergência.

CONTEXTO DO CLIENTE (EXTRAÍDO DA BASE DE DADOS):
{context_data_str}

REGRAS DE COMPORTAMENTO E SEGURANÇA:
1. ANCORAGEM RIGOROSA NOS DADOS: Responda a dúvidas financeiras utilizando estritamente os valores do extrato e do histórico. Nunca invente saldos, taxas ou despesas inexistentes.
2. ABORDAGEM CONSULTIVA E PROATIVA: Ao responder sobre gastos ou saldo, conecte proativamente a sobra orçamentária ({format_brl(saldo_livre)}) ao objetivo da reserva de emergência em CDB ou Tesouro Selic.
3. PERSONA E TOM DE VOZ: Didático, encorajador, transparente e acessível. Explique termos financeiros simples e evite jargões técnicos sem contexto.
4. RESTRICÕES E LIMITAÇÕES:
   - Não realize movimentações bancárias, transferências ou aplicações automáticas.
   - Não faça recomendações de renda variável (ações, fundos imobiliários, criptomoedas).
   - Não solicite ou armazene senhas, tokens ou dados de cartão de crédito.
   - Se o usuário fizer perguntas fora do escopo de finanças, decline educadamente e redirecione para a gestão das metas do cliente.
"""

# ==============================================================================
# 4. Barra Lateral (Sidebar) - Painel de Controle e Dashboard
# ==============================================================================
with st.sidebar:
    st.title("💰 PoupaIA")
    st.caption("Assistente Consultivo de Metas Financeiras")
    st.markdown("---")
    
    st.subheader("⚙️ Configuração do LLM")
    model_name = st.text_input("Modelo Ollama:", value="gpt-oss")
    st.caption(f"Provedor: Ollama Local (`{model_name}`)")
    
    st.markdown("---")
    st.subheader("📊 Resumo Financeiro")
    col1, col2 = st.columns(2)
    col1.metric("Receita", format_brl(receita_total))
    col2.metric("Despesas", format_brl(despesas_totais))
    
    st.metric(
        "Saldo Livre", 
        format_brl(saldo_livre), 
        delta="Pronto para investir" if saldo_livre > 0 else "Atenção ao orçamento",
        delta_color="normal" if saldo_livre > 0 else "inverse"
    )
    
    if cat_summary:
        st.markdown("**Detalhamento de Gastos:**")
        for cat, val in cat_summary.items():
            st.write(f"- **{cat.capitalize()}:** {format_brl(val)}")

    st.markdown("---")
    if hist_df is not None:
        with st.expander("📋 Histórico de Atendimentos"):
            st.dataframe(hist_df, use_container_width=True)

# ==============================================================================
# 5. Interface do Chat Principal
# ==============================================================================
st.title("💬 PoupaIA - Chat Financeiro")
st.markdown("Seu tutor de orçamento pessoal e construção de reserva de emergência.")

# Inicialização do histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Olá! Sou o PoupaIA, seu assistente de metas financeiras. Notei que você tem um saldo livre de {format_brl(saldo_livre)} este mês. Que tal alocarmos uma parte na sua reserva de emergência hoje?"
        }
    ]

# Exibição do histórico de conversa
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Entrada do usuário
if prompt := st.chat_input("Digite sua dúvida orçamentária ou sobre investimentos..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    # Monta payload para a API do Ollama
    ollama_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages:
        ollama_messages.append({"role": m["role"], "content": m["content"]})
        
    # Resposta com streaming e compatibilidade entre versões da biblioteca ollama
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response_stream = ollama.chat(
                model=model_name,
                messages=ollama_messages,
                stream=True
            )
            for chunk in response_stream:
                # Trata compatibilidade dict vs ChatResponse object do pacote ollama
                if isinstance(chunk, dict):
                    content = chunk.get('message', {}).get('content', '')
                else:
                    content = getattr(getattr(chunk, 'message', None), 'content', '')
                
                full_response += content
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            error_msg = f"⚠️ **Erro na conexão com o Ollama (`{model_name}`):** {str(e)}\n\n" \
                        f"**Passos para resolver:**\n" \
                        f"1. Verifique se o Ollama está rodando localmente (`ollama serve`).\n" \
                        f"2. Certifique-se de ter baixado o modelo exato (`ollama pull {model_name}`)."
            message_placeholder.markdown(error_msg)
            full_response = error_msg

    # Salva resposta no histórico da sessão
    st.session_state.messages.append({"role": "assistant", "content": full_response})
