import streamlit as st
from openai import OpenAI

# Treinamento para o time da Carglass
st.set_page_config(page_title="Mini GPT didático", page_icon="🤖")
st.title("🤖 Mini GPT didático (Streamlit + OpenAI)")

# 1) Lê a chave do Streamlit Secrets (Cloud ou local)
api_key = st.secrets.get("OPENAI_API_KEY", None)
if not api_key:
    st.warning("Defina OPENAI_API_KEY em st.secrets para continuar.")
    st.stop()

client = OpenAI(api_key=api_key)

# 2) Sidebar para configurar personalidade
st.sidebar.header("Configuração")
personalidade = st.sidebar.text_area(
    "Defina a personalidade do assistente:",
    "Você é um assistente educado e didático, que explica de forma simples."
)

# 3) Inicializa estado da conversa com o system prompt dinâmico
if "messages" not in st.session_state or st.sidebar.button("🔄 Redefinir conversa"):
    st.session_state.messages = [
        {"role": "system", "content": personalidade}
    ]

# 4) Renderiza histórico
for m in st.session_state.messages:
    if m["role"] in ("user", "assistant"):
        with st.chat_message("user" if m["role"] == "user" else "assistant"):
            st.markdown(m["content"])

# 5) Entrada do usuário
prompt = st.chat_input("Pergunte algo...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            temperature=0.6,
        )
        answer = resp.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Erro ao chamar a API: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
