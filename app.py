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
            df.columns = df.columns.str.lower()
            for _, row in df.iterrows():
                pags = str(row.get('paginas', '100'))
                try:
                    qtd_pags = int(float(pags)) if pags.replace('.','',1).isdigit() else 100
                except:
                    qtd_pags = 100
                ajuste = (qtd_pags / 2) * 0.1 + 2.0
                st.session_state.livros.append({
                    "titulo": str(row.get('titulo', 'Sem título')), 
                    "cdd": str(row.get('cdd', row.get('classificacao', ''))), 
                    "paginas": str(qtd_pags),
                    "dimensao": str(row.get('dimensao', '')),
                    "ed": str(row.get('ed', row.get('edicao', '1.ed.'))),
                    "ex": str(row.get('ex', row.get('exemplar', 'Ex.1'))),
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
        # ESTANTE: Uma única linha flexível pura em HTML/CSS (Garante alinhamento lado a lado no tablet)
        html_estante = "<div style='display: flex; flex-direction: row; flex-wrap: wrap; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 35px; min-height: 260px; background-color: #f9f9f9; border-radius: 10px; overflow-x: auto;'>"
        
        for i, livro in enumerate(st.session_state.livros):
            largura = max(livro.get('ajuste', 15.0) * 3, 45)
            
            # Criamos uma caixinha estilizada com link invisível para clique nativo HTML
            html_estante += f"""
            <a href="?selecionar={i}" target="_self" style="text-decoration: none; color: inherit;">
                <div style="width: {largura}px; height: 200px; background: #A084E8; border-radius: 2px; 
                display: flex; flex-direction: column; justify-content: space-between; align-items: center; color: white; 
                box-shadow: 4px 4px 8px rgba(0,0,0,0.25); position: relative; overflow: hidden; padding-top: 10px; cursor: pointer;">
                    
                    <div style="writing-mode: vertical-rl; font-size: 11px; max-height: 110px; overflow: hidden; text-align: center; font-weight: bold; width: 100%;">
                        {livro.get('titulo', 'Livro')}
                    </div>
                    
                    <div style="width: 100%; height: 55px; background: white; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: 'Courier New', monospace; font-size: 9px; color: black; border-top: 1px solid #ccc; line-height: 1.1; overflow: hidden; padding: 1px;">
                        <div style="font-weight: bold; text-align: center; width: 100%; white-space: nowrap; overflow: hidden;">{livro.get('cdd', '')}</div>
                        <div style="font-size: 8px; white-space: nowrap; overflow: hidden;">{livro.get('ed', '')}</div>
                        <div style="font-size: 8px; white-space: nowrap; overflow: hidden;">{livro.get('ex', '')}</div>
                    </div>
                </div>
            </a>
            """
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)
        
        # Monitora cliques na estante via parâmetros da URL do Streamlit
        parametros = st.query_params
        if "selecionar" in parametros:
            st.session_state.livro_ativo = int(parametros["selecionar"])
            st.session_state.mostrar_3d = True

        # Botão alternativo caso o clique na imagem falhe em telas touch antigas
        st.write(" ")
        opcoes_livros = [f"{i+1}. {l.get('titulo')}" for i, l in enumerate(st.session_state.livros)]
        escolha = st.selectbox("Selecione o livro para calibrar abaixo:", opcoes_livros, index=st.session_state.livro_ativo)
        
        idx_novo = opcoes_livros.index(escolha)
        if idx_novo != st.session_state.livro_ativo:
            st.session_state.livro_ativo = idx_novo
            st.session_state.mostrar_3d = True
            st.rerun()
            
        st.write("---")
        
        # INTERFACE INFERIOR LADO A LADO
        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            livro_sel = st.session_state.livros[idx]
            
            col_ajustes, col_3d = st.columns([1.2, 1])
            
            with col_ajustes:
                st.subheader(f"⚙️ Ajustar: {livro_sel.get('titulo', 'Livro')}")
                
                pags_txt = livro_sel.get('paginas', 'Não informada')
                dim_txt = livro_sel.get('dimensao', '')
                
                st.markdown(f"""
                **Dados do Livro:**
                * **Classificação:** {livro_sel.get('cdd', 'Sem Classificação')}
                * **Páginas:** {pags_txt} pág.
                * **Dimensão:** {dim_txt if dim_txt and dim_txt != 'nan' else 'Não informada'}
                """)
                
                novo_val = st.slider(
                    "Largura da Lombada (mm)", 1.0, 50.0, float(livro_sel.get('ajuste', 15.0)), 0.5, key="slider_lombada"
                )
                st.session_state.livros[idx]['ajuste'] = novo_val
                
                if novo_val < 5.0:
                    st.error("⚠️ ATENÇÃO: Lombada muito fina (abaixo de 5mm). Use etiqueta de capa!")
                else:
                    st.success("✅ Espessura ideal para etiqueta de lombada.")
            
            with col_3d:
                st.subheader("🔍 Visualização 3D da Etiqueta")
                
                val_atual = st.session_state.livros[idx]['ajuste']
                cor_borda = "#EF4444" if val_atual < 5.0 else "#22C55E"
                esp_3d = max(val_atual * 6, 60)
                
                html_renderizado = f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; margin-top: 20px; height: 320px;">
                    <div style="width: {esp_3d}px; height: 280px; background: #A084E8; border: 5px solid {cor_borda}; transform: rotateY(-20deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.4); display: flex; flex-direction: column; justify-content: flex-end; position: relative;">
                        <div style="width: 100%; height: 95px; background: white; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: 'Courier New', monospace; font-size: 11px; color: black; border-top: 1px solid #ccc; padding: 2px; line-height: 1.2; overflow: hidden;">
                            <div style="text-align: center; font-weight: bold; font-size: 11px; width: 100%; word-wrap: break-word;">{livro_sel.get('cdd', '')}</div>
                            <div style="text-align: center; font-size: 10px; margin-top: 3px;">{livro_sel.get('ed', '')}</div>
                            <div style="text-align: center; font-size: 10px;">{livro_sel.get('ex', '')}</div>
                        </div>
                    </div>
                    <div style="width: 140px; height: 280px; background: #D1D5DB; transform-origin: left; transform: rotateY(30deg); box-shadow: 20px 10px 30px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; color: #4B5563; font-size: 12px; font-weight: bold;">CAPA</div>
                </div>
                """
                st.markdown(html_renderizado, unsafe_allow_html=True)
