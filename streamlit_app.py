import streamlit as st
from openai import OpenAI

# Treinamento para o nosso time da Carglass, abaixo temos o passo a passo do que foi feito de maneira simplificada.

st.set_page_config(page_title="Mini GPT didático", page_icon="🤖")
st.title("🤖 Mini GPT didático (Streamlit + OpenAI)")

# 1) Lê a chave do Streamlit Secrets (Cloud) ou do secrets.toml (local)
#    Em deploy no Streamlit Cloud, adicione OPENAI_API_KEY nas Configurações > Secrets.
api_key = st.secrets.get("OPENAI_API_KEY", None)
if not api_key:
    st.warning("Defina OPENAI_API_KEY em st.secrets para continuar.")
    st.stop()

client = OpenAI(api_key=api_key)

# 2) Estado de conversa
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Você é um assistente irritado com respostas grossas."}
    ]

# 3) Renderiza histórico (pula o 'system' no UI)
for m in st.session_state.messages:
    if m["role"] in ("user", "assistant"):
        with st.chat_message("user" if m["role"] == "user" else "assistant"):
            st.markdown(m["content"])

# 4) Entrada do usuário
prompt = st.chat_input("Pergunte algo...")
if prompt:
    # mostra no chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5) Chamada ao modelo (simples e direto)
    # Dica: para custo/latência, use um modelo leve (ex.: gpt-4o-mini).
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                # Passa todo o histórico para manter contexto
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in ("system", "user", "assistant")
                ]
            ],
            temperature=0.2,
        )
        answer = resp.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Erro ao chamar a API: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
