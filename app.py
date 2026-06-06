import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="BiblioKhan Pro")

# --- ESTADO INICIAL ---
if "livros" not in st.session_state: st.session_state.livros = []
if "campos_config" not in st.session_state: st.session_state.campos_config = ["Título", "CDD", "Edição", "Exemplar"]
if "livro_ativo" not in st.session_state: st.session_state.livro_ativo = None

# --- MOTOR DE RENDERIZAÇÃO 3D ---
def renderizar_etiqueta_3d(livro):
    html_campos = ""
    for campo in st.session_state.campos_config:
        valor = livro.get(campo, "")
        html_campos += f"<div style='margin-bottom: 2px;'>{valor}</div>"
    
    # CSS 3D: Perspectiva, Rotação Y e Sombra para efeito de lombada
    return f"""
    <div style="
        perspective: 800px; 
        display: flex; 
        justify-content: center; 
        margin-top: 50px;">
        <div style="
            width: 140px; 
            height: 250px; 
            background: #7E57C2; 
            transform: rotateY(-20deg); 
            box-shadow: -10px 10px 20px rgba(0,0,0,0.3);
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            padding-top: 20px;
            color: white;">
            
            <div style="
                background: white; 
                color: black; 
                width: 80%; 
                padding: 10px; 
                font-family: monospace; 
                font-size: 11px; 
                text-align: center;">
                {html_campos}
            </div>
        </div>
    </div>
    """

# --- UI PRINCIPAL ---
st.title("📚 BiblioKhan Pro | Visualização 3D")

tab1, tab2, tab3 = st.tabs(["⚙️ Configurar Campos", "➕ Entrada de Dados", "📚 Estante 3D"])

with tab1:
    st.subheader("Definir Estrutura da Etiqueta")
    novo = st.text_input("Adicionar campo (ex: Cutter, Vol):")
    if st.button("Adicionar"):
        if novo and novo not in st.session_state.campos_config:
            st.session_state.campos_config.append(novo)
            st.rerun()
    st.write("Ordem atual:", st.session_state.campos_config)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cadastro Manual")
        with st.form("manual"):
            dados = {campo: st.text_input(campo) for campo in st.session_state.campos_config}
            if st.form_submit_button("Salvar Livro"):
                st.session_state.livros.append(dados)
                st.success("Livro adicionado!")
    with col2:
        st.subheader("Upload CSV")
        file = st.file_uploader("Subir CSV", type=["csv"])
        if file:
            df = pd.read_csv(file)
            st.session_state.livros.extend(df.to_dict('records'))
            st.success("Dados importados!")

with tab3:
    if not st.session_state.livros:
        st.info("Adicione um livro para ver o efeito 3D.")
    else:
        # Lista horizontal simples de livros
        cols = st.columns(len(st.session_state.livros))
        for i, l in enumerate(st.session_state.livros):
            with cols[i]:
                if st.button(l.get("Título", "Livro"), key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                if st.button("Remover", key=f"del_{i}"):
                    st.session_state.livros.pop(i)
                    st.rerun()
        
        st.write("---")
        if st.session_state.livro_ativo is not None:
            idx = st.session_state.livro_ativo
            livro = st.session_state.livros[idx]
            st.subheader(f"Lombada: {livro.get('Título')}")
            st.markdown(renderizar_etiqueta_3d(livro), unsafe_allow_html=True)
