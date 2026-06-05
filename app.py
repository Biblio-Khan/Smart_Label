import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="BiblioKhan Pro")

# --- INICIALIZAÇÃO ---
if "tela" not in st.session_state: st.session_state.tela = "entrada"
if "livros" not in st.session_state: st.session_state.livros = []
if "livro_ativo" not in st.session_state: st.session_state.livro_ativo = 0

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
                st.success("Adicionado!")
    
    with col2:
        st.subheader("Importar via CSV")
        file = st.file_uploader("Subir arquivo CSV", type=["csv"])
        if file:
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                ajuste = (row['paginas'] / 2) * 0.1 + 2.0
                st.session_state.livros.append({"titulo": row['titulo'], "cdd": row['cdd'], "ajuste": min(ajuste, 50.0)})
            st.success("Dados importados!")

    if st.button("Ir para Estante de Calibragem ➡️", type="primary"):
        mudar_tela("calibragem"); st.rerun()

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.title("📚 Estante de Calibragem")
    if st.button("⬅️ Voltar para Entrada"):
        mudar_tela("entrada"); st.rerun()
    
    st.write("---")
    
    if not st.session_state.livros:
        st.warning("Nenhum livro cadastrado.")
    else:
        # ESTANTE
        st.markdown("<div style='display: flex; flex-wrap: wrap; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 40px; min-height: 250px; background-color: #f9f9f9; border-radius: 10px;'>", unsafe_allow_html=True)
        
        for i, livro in enumerate(st.session_state.livros):
            largura = max(livro['ajuste'] * 3, 50)
            # Botão para selecionar livro
            if st.button(f"👁️ {livro['titulo']}", key=f"sel_{i}"):
                st.session_state.livro_ativo = i
            
            st.markdown(f"""
            <div style="width: {largura}px; height: 180px; background: #A084E8; border-radius: 2px; 
            display: flex; align-items: center; justify-content: center; color: white; 
            writing-mode: vertical-rl; font-size: 14px; box-shadow: 5px 5px 10px rgba(0,0,0,0.3);">
            {livro['titulo']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # VISUALIZAÇÃO 3D DO LIVRO ATIVO
        l = st.session_state.livros[st.session_state.livro_ativo]
        st.subheader(f"Calibragem: {l['titulo']}")
        
        # Cores de Aviso
        cor_aviso = "border: 5px solid #EF4444;" if l['ajuste'] < 5.0 else "border: 5px solid #22C55E;"
        
        st.markdown(f"""
        <div style="perspective: 1000px; display: flex; justify-content: center; margin: 40px 0;">
            <div style="width: {max(l['ajuste']*6, 60)}px; height: 300px; background: #A084E8; {cor_aviso} transform: rotateY(-20deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.4);"></div>
            <div style="width: 150px; height: 300px; background: #D1D5DB; transform-origin: left; transform: rotateY(30deg); box-shadow: 20px 10px 30px rgba(0,0,0,0.3);"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Alertas e Slider
        if l['ajuste'] < 5.0:
            st.error("⚠️ ATENÇÃO: Lombada muito fina (abaixo de 5mm). Use etiqueta de capa!")
        else:
            st.success("✅ Espessura ideal para etiqueta de lombada.")
            
        st.session_state.livros[st.session_state.livro_ativo]['ajuste'] = st.slider(
            "Ajustar largura (mm)", 1.0, 50.0, float(l['ajuste']), 0.5
        )
