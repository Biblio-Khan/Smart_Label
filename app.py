import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="BiblioKhan Pro")

# --- INICIALIZAÇÃO ---
if "tela" not in st.session_state:
    st.session_state.tela = "entrada"
if "livros" not in st.session_state:
    st.session_state.livros = []

def mudar_tela(nova_tela):
    st.session_state.tela = nova_tela

# ==========================================================
# TELA 1: ENTRADA DE DADOS
# ==========================================================
if st.session_state.tela == "entrada":
    st.title("📝 BiblioKhan | Entrada de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cadastro Manual")
        with st.form("manual"):
            titulo = st.text_input("Título")
            cdd = st.text_input("CDD")
            paginas = st.number_input("Páginas", min_value=1, value=100)
            if st.form_submit_button("Adicionar à Lista"):
                ajuste = (paginas / 2) * 0.1 + 2.0
                st.session_state.livros.append({"titulo": titulo, "cdd": cdd, "ajuste": min(ajuste, 50.0)})
                st.success(f"'{titulo}' adicionado!")
    
    with col2:
        st.subheader("Importar via CSV")
        st.info("O CSV deve ter as colunas: 'titulo', 'cdd', 'paginas'")
        file = st.file_uploader("Subir arquivo", type=["csv"])
        if file:
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                ajuste = (row['paginas'] / 2) * 0.1 + 2.0
                st.session_state.livros.append({"titulo": row['titulo'], "cdd": row['cdd'], "ajuste": min(ajuste, 50.0)})
            st.success("Arquivo carregado com sucesso!")

    if st.button("Ir para Estante de Calibragem ➡️", type="primary"):
        mudar_tela("calibragem")
        st.rerun()

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.title("📚 Estante de Calibragem")
    
    if st.button("⬅️ Voltar para Entrada de Dados"):
        mudar_tela("entrada")
        st.rerun()
    
    st.divider()
    
    if not st.session_state.livros:
        st.warning("Nenhum livro cadastrado.")
    else:
        # PRATELEIRA: Container que simula a madeira
        st.markdown("""
        <div style="display: flex; align-items: flex-end; border-bottom: 15px solid #5D4037; padding-bottom: 5px; gap: 20px; min-height: 250px;">
        """, unsafe_allow_html=True)
        
        # Exibe os livros sobre a prateleira
        for i, livro in enumerate(st.session_state.livros):
            largura = livro['ajuste'] * 2 # Escala visual
            st.markdown(f"""
            <div style="width: {max(largura, 40)}px; height: 180px; background: #A084E8; border-radius: 2px; 
            display: flex; justify-content: center; align-items: center; color: white; writing-mode: vertical-rl; text-orientation: mixed; font-size: 12px; box-shadow: 2px -2px 5px rgba(0,0,0,0.2);">
            {livro['titulo']}
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.write("### Ajuste individual dos exemplares:")
        # Sliders abaixo da estante
        cols = st.columns(len(st.session_state.livros))
        for i, livro in enumerate(st.session_state.livros):
            with cols[i]:
                st.session_state.livros[i]['ajuste'] = st.slider(
                    f"{livro['titulo'][:10]}...", 5.0, 50.0, float(livro['ajuste']), 0.5, key=f"s_{i}"
                )
