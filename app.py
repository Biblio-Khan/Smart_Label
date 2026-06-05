import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="BiblioKhan Pro")

# --- INICIALIZAÇÃO SEGURA DO ESTADO ---
if "tela" not in st.session_state: 
    st.session_state.tela = "entrada"
if "livros" not in st.session_state: 
    st.session_state.livros = []
if "livro_ativo" not in st.session_state: 
    st.session_state.livro_ativo = 0
if "mostrar_3d" not in st.session_state:
    st.session_state.mostrar_3d = False

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
            titulo = st.text_input("Título *")
            classificacao = st.text_input("Classificação *")
            
            c1, c2 = st.columns(2)
            paginas = c1.number_input("Páginas", min_value=1, value=100)
            dimensao = c2.text_input("Dimensão (ex: 23 cm)")
            
            c3, c4 = st.columns(2)
            edicao = c3.text_input("Edição", value="1.ed.")
            exemplar = c4.text_input("Exemplar", value="Ex.1")
            
            if st.form_submit_button("Adicionar à Lista"):
                if titulo and classificacao:
                    ajuste = (paginas / 2) * 0.1 + 2.0
                    st.session_state.livros.append({
                        "titulo": titulo, 
                        "cdd": classificacao, 
                        "paginas": str(paginas),
                        "dimensao": dimensao,
                        "ed": edicao,
                        "ex": exemplar,
                        "ajuste": min(ajuste, 50.0)
                    })
                    st.success(f"'{titulo}' adicionado!")
                else:
                    st.error("Por favor, preencha Título e Classificação.")
    
    with col2:
        st.subheader("Importar via CSV")
        st.info("O CSV deve conter: titulo, cdd, paginas, dimensao, ed, ex")
        file = st.file_uploader("Subir arquivo CSV", type=["csv"])
        if file:
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                ajuste = (int(row.get('paginas', 100)) / 2) * 0.1 + 2.0
                st.session_state.livros.append({
                    "titulo": str(row.get('titulo', '')), 
                    "cdd": str(row.get('cdd', '')), 
                    "paginas": str(row.get('paginas', '')),
                    "dimensao": str(row.get('dimensao', '')),
                    "ed": str(row.get('ed', '1.ed.')),
                    "ex": str(row.get('ex', 'Ex.1')),
                    "ajuste": min(ajuste, 50.0)
                })
            st.success("Dados importados com sucesso!")

    if st.button("Ir para Estante de Calibragem ➡️", type="primary"):
        mudar_tela("calibragem")
        st.rerun()

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.title("📚 Estante de Calibragem")
    if st.button("⬅️ Voltar para Entrada"):
        st.session_state.mostrar_3d = False
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
            
            if st.button(f"👁️ {livro['titulo']}", key=f"sel_{i}"):
                st.session_state.livro_ativo = i
                st.session_state.mostrar_3d = True
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
        
        # INTERFACE INFERIOR LADO A LADO
        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            livro_sel = st.session_state.livros[idx]
            
            col_ajustes, col_3d = st.columns([1.2, 1])
            
            with col_ajustes:
                st.subheader(f"⚙️ Ajustar: {livro_sel['titulo']}")
                
                # Exibição dos dados técnicos salvos
                st.markdown(f"""
                **Dados do Livro:**
                * **Classificação:** {livro_sel['cdd']}
                * **Páginas:** {livro_sel['paginas']} pág.
                * **Dimensão:** {livro_sel['dimensao'] if livro_sel['dimensao'] else 'Não informada'}
                """)
                
                # O Slider altera o valor diretamente no session_state
                novo_val = st.slider(
                    "Largura da Lombada (mm)", 1.0, 50.0, float(livro_sel['ajuste']), 0.5, key="slider_lombada"
                )
                st.session_state.livros[idx]['ajuste'] = novo_val
                
                # Alertas baseados no valor atualizado
                if novo_val < 5.0:
                    st.error("⚠️ ATENÇÃO: Lombada muito fina (abaixo de 5mm). Use etiqueta de capa!")
                else:
                    st.success("✅ Espessura ideal para etiqueta de lombada.")
            
            with col_3d:
                st.subheader("🔍 Visualização 3D da Etiqueta")
                
                val_atual = st.session_state.livros[idx]['ajuste']
                cor_aviso = "border: 5px solid #EF4444;" if val_atual < 5.0 else "border: 5px solid #22C55E;"
                esp_3d = max(val_atual * 6, 60)
                
                # Interface 3D Renderizando a Etiqueta de Lombada real com os dados digitados
                st.markdown(f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; margin-top: 20px; height: 320px;">
                    
                    <div style="width: {esp_3d}px; height: 280px; background: #A084E8; {cor_aviso} transform: rotateY(-20deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.4); display: flex; flex-direction: column; justify-content: flex-end; position: relative;">
                        
                        <div style="width: 100%; height: 95px; background: white; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: 'Courier New', monospace; font-size: 11px; color: black; border-top: 1px solid #ccc; padding: 2px; line-height: 1.2; overflow: hidden;">
                            <div style="text-align: center; font-weight: bold; font-size: 11px; width: 100%; word-wrap: break-word;">{livro_sel['cdd']}</div>
                            <div style="text-align: center; font-size: 10px; margin-top: 3px;">{livro_sel['ed']}</div>
                            <div style="text-align: center; font-size: 10px;">{livro_sel['ex']}</div>
                        </div>
                        
                    </div>
                    
                    <div style="width: 140px; height: 280px; background: #D1D5DB; transform-origin: left; transform: rotateY(30deg); box-shadow: 20px 10px 30px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; color: #4B5563; font-size: 12px; font-weight: bold;">CAPA</div>
                </div>
                """, unsafe_allow_html=True)
