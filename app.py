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
# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.title("📚 Estante de Calibragem")
    if st.button("⬅️ Voltar para Entrada"):
        # Reseta o livro ativo ao voltar
        if "mostrar_3d" in st.session_state:
            del st.session_state.mostrar_3d
        mudar_tela("entrada")
        st.rerun()
    
    st.write("---")
    
    if not st.session_state.livros:
        st.warning("Nenhum livro cadastrado.")
    else:
        # ESTANTE (Livros bem espaçados)
        st.markdown("<div style='display: flex; flex-wrap: wrap; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 50px; min-height: 250px; background-color: #f9f9f9; border-radius: 10px;'>", unsafe_allow_html=True)
        
        for i, livro in enumerate(st.session_state.livros):
            largura = max(livro['ajuste'] * 3, 50)
            
            # Quando clica no botão, ativa a visualização 3D para este livro
            if st.button(f"👁️ {livro['titulo']}", key=f"sel_{i}"):
                st.session_state.livro_ativo = i
                st.session_state.mostrar_3d = True # Ativa o gatilho visual
                st.rerun()
            
            st.markdown(f"""
            <div style="width: {largura}px; height: 180px; background: #A084E8; border-radius: 2px; 
            display: flex; align-items: center; justify-content: center; color: white; 
            writing-mode: vertical-rl; font-size: 14px; box-shadow: 5px 5px 10px rgba(0,0,0,0.3);">
            {livro['titulo']}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.write(" ")
        
        # SÓ ABRE SE O USUÁRIO CLICOU EM ALGUM LIVRO
        if "mostrar_3d" in st.session_state and st.session_state.mostrar_3d:
            l = st.session_state.livros[st.session_state.livro_ativo]
            
            # Divide a tela de baixo em duas colunas: Ajustes na Esquerda | 3D na Direita
            col_ajustes, col_3d = st.columns([1.2, 1])
            
            with col_ajustes:
                st.subheader(f"⚙️ Ajustar: {l['titulo']}")
                
                # Slider de Calibragem
                novo_ajuste = st.slider(
                    "Largura da Lombada (mm)", 1.0, 50.0, float(l['ajuste']), 0.5, key="slider_ativo"
                )
                st.session_state.livros[st.session_state.livro_ativo]['ajuste'] = novo_ajuste
                
                # Alertas e Avisos de Cor abaixo do Slider
                if novo_ajuste < 5.0:
                    st.error("⚠️ ATENÇÃO: Lombada muito fina (abaixo de 5mm). Use etiqueta de capa!")
                else:
                    st.success("✅ Espessura ideal para etiqueta de lombada.")
            
            with col_3d:
                st.subheader("🔍 Visualização 3D")
                
                # Cores de Aviso na borda do modelo 3D
                cor_aviso = "border: 5px solid #EF4444;" if l['ajuste'] < 5.0 else "border: 5px solid #22C55E;"
                esp_3d = max(l['ajuste'] * 6, 60)
                
                st.markdown(f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; margin-top: 20px; height: 320px;">
                    <div style="width: {esp_3d}px; height: 280px; background: #A084E8; {cor_aviso} transform: rotateY(-20deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.4); display: flex; justify-content: center; align-items: center; color: white; font-size: 11px;"></div>
                    <div style="width: 140px; height: 280px; background: #D1D5DB; transform-origin: left; transform: rotateY(30deg); box-shadow: 20px 10px 30px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; color: #4B5563; font-size: 12px;">CAPA</div>
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
