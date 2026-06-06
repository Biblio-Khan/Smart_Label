import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(layout="wide", page_title="BiblioKhan Pro")

# --- INICIALIZAÇÃO SEGURA DO ESTADO ---
if "tela" not in st.session_state: st.session_state.tela = "entrada"
if "livros" not in st.session_state: st.session_state.livros = []
if "livro_ativo" not in st.session_state: st.session_state.livro_ativo = 0
if "mostrar_3d" not in st.session_state: st.session_state.mostrar_3d = False

def mudar_tela(nova_tela): st.session_state.tela = nova_tela

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
            dimensao = c2.text_input("Dimensão")
            c3, c4 = st.columns(2)
            edicao = c3.text_input("Edição", value="1.ed.")
            exemplar = c4.text_input("Exemplar", value="Ex.1")
            
            if st.form_submit_button("Adicionar à Lista"):
                if titulo and classificacao:
                    st.session_state.livros.append({
                        "titulo": titulo, "cdd": classificacao, "paginas": str(paginas),
                        "dimensao": dimensao, "ed": edicao, "ex": exemplar, "ajuste": 15.0
                    })
                    st.success("Adicionado!")
    
    with col2:
        st.subheader("Importar (CSV ou XML)")
        file = st.file_uploader("Subir arquivo", type=["csv", "xml"])
        if file:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                    df.columns = df.columns.str.lower()
                    data = df.to_dict('records')
                else: # XML
                    tree = ET.parse(file)
                    root = tree.getroot()
                    data = [{child.tag: child.text for child in item} for item in root]
                
                for row in data:
                    st.session_state.livros.append({
                        "titulo": str(row.get('titulo', 'Sem título')),
                        "cdd": str(row.get('cdd', '')),
                        "paginas": str(row.get('paginas', '100')),
                        "dimensao": str(row.get('dimensao', '')),
                        "ed": str(row.get('ed', '1.ed.')),
                        "ex": str(row.get('ex', 'Ex.1')),
                        "ajuste": 15.0
                    })
                st.success("Importado!")
            except Exception as e:
                st.error(f"Erro na importação: {e}")

    if st.button("Ir para Estante de Calibragem ➡️", type="primary"):
        mudar_tela("calibragem")
        st.rerun()

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.title("📚 Estante de Calibragem")
    if st.button("⬅️ Voltar"):
        st.session_state.mostrar_3d = False
        mudar_tela("entrada")
        st.rerun()
    
    if not st.session_state.livros:
        st.warning("Nenhum livro cadastrado.")
    else:
        # Layout da Estante com botões de Seleção e Remoção
        cols = st.columns(len(st.session_state.livros))
        for i, livro in enumerate(st.session_state.livros):
            with cols[i]:
                t_seguro = str(livro.get("titulo") or "Sem título")
                if st.button(f"{t_seguro[:10]}", key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                    st.session_state.mostrar_3d = True
                    st.rerun()
                if st.button("🗑️ Remover", key=f"del_{i}"):
                    st.session_state.livros.pop(i)
                    st.session_state.mostrar_3d = False
                    st.rerun()
        
        # Renderização visual compacta
        html_estante = "<div style='display: flex; gap: 10px; border-bottom: 20px solid #5D4037; padding: 20px; overflow-x: auto;'>"
        for l in st.session_state.livros:
            html_estante += f"<div style='min-width: 60px; height: 150px; background: #A084E8; color: white; font-size: 9px; text-align: center; padding: 5px;'>{l['titulo'][:10]}</div>"
        st.markdown(html_estante + "</div>", unsafe_allow_html=True)

        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            l = st.session_state.livros[idx]
            col_aj, col_3d = st.columns([1, 1])
            with col_aj:
                l['ajuste'] = st.slider("Espessura (mm)", 1.0, 50.0, float(l['ajuste']))
            with col_3d:
                esp = max(l['ajuste'] * 6, 60)
                st.markdown(f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; margin-top: 20px;">
                    <div style="width: {esp}px; height: 280px; background: #A084E8; border: 5px solid #22C55E; transform: rotateY(-20deg); padding: 10px; font-family: monospace; font-size: 10px; color: black; background: white;">
                        <b>{l['titulo'].upper()}</b><br>{l['cdd']}<br>{l['ed']}<br>{l['ex']}
                    </div>
                </div>
                """, unsafe_allow_html=True)import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(layout="wide", page_title="BiblioKhan Pro")

# --- INICIALIZAÇÃO SEGURA DO ESTADO ---
if "tela" not in st.session_state: st.session_state.tela = "entrada"
if "livros" not in st.session_state: st.session_state.livros = []
if "livro_ativo" not in st.session_state: st.session_state.livro_ativo = 0
if "mostrar_3d" not in st.session_state: st.session_state.mostrar_3d = False

def mudar_tela(nova_tela): st.session_state.tela = nova_tela

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
            dimensao = c2.text_input("Dimensão")
            c3, c4 = st.columns(2)
            edicao = c3.text_input("Edição", value="1.ed.")
            exemplar = c4.text_input("Exemplar", value="Ex.1")
            
            if st.form_submit_button("Adicionar à Lista"):
                if titulo and classificacao:
                    st.session_state.livros.append({
                        "titulo": titulo, "cdd": classificacao, "paginas": str(paginas),
                        "dimensao": dimensao, "ed": edicao, "ex": exemplar, "ajuste": 15.0
                    })
                    st.success("Adicionado!")
    
    with col2:
        st.subheader("Importar (CSV ou XML)")
        file = st.file_uploader("Subir arquivo", type=["csv", "xml"])
        if file:
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                    df.columns = df.columns.str.lower()
                    data = df.to_dict('records')
                else: # XML
                    tree = ET.parse(file)
                    root = tree.getroot()
                    data = [{child.tag: child.text for child in item} for item in root]
                
                for row in data:
                    st.session_state.livros.append({
                        "titulo": str(row.get('titulo', 'Sem título')),
                        "cdd": str(row.get('cdd', '')),
                        "paginas": str(row.get('paginas', '100')),
                        "dimensao": str(row.get('dimensao', '')),
                        "ed": str(row.get('ed', '1.ed.')),
                        "ex": str(row.get('ex', 'Ex.1')),
                        "ajuste": 15.0
                    })
                st.success("Importado!")
            except Exception as e:
                st.error(f"Erro na importação: {e}")

    if st.button("Ir para Estante de Calibragem ➡️", type="primary"):
        mudar_tela("calibragem")
        st.rerun()

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.title("📚 Estante de Calibragem")
    if st.button("⬅️ Voltar"):
        st.session_state.mostrar_3d = False
        mudar_tela("entrada")
        st.rerun()
    
    if not st.session_state.livros:
        st.warning("Nenhum livro cadastrado.")
    else:
        # Layout da Estante com botões de Seleção e Remoção
        cols = st.columns(len(st.session_state.livros))
        for i, livro in enumerate(st.session_state.livros):
            with cols[i]:
                t_seguro = str(livro.get("titulo") or "Sem título")
                if st.button(f"{t_seguro[:10]}", key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                    st.session_state.mostrar_3d = True
                    st.rerun()
                if st.button("🗑️ Remover", key=f"del_{i}"):
                    st.session_state.livros.pop(i)
                    st.session_state.mostrar_3d = False
                    st.rerun()
        
        # Renderização visual compacta
        html_estante = "<div style='display: flex; gap: 10px; border-bottom: 20px solid #5D4037; padding: 20px; overflow-x: auto;'>"
        for l in st.session_state.livros:
            html_estante += f"<div style='min-width: 60px; height: 150px; background: #A084E8; color: white; font-size: 9px; text-align: center; padding: 5px;'>{l['titulo'][:10]}</div>"
        st.markdown(html_estante + "</div>", unsafe_allow_html=True)

        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            l = st.session_state.livros[idx]
            col_aj, col_3d = st.columns([1, 1])
            with col_aj:
                l['ajuste'] = st.slider("Espessura (mm)", 1.0, 50.0, float(l['ajuste']))
            with col_3d:
                esp = max(l['ajuste'] * 6, 60)
                st.markdown(f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; margin-top: 20px;">
                    <div style="width: {esp}px; height: 280px; background: #A084E8; border: 5px solid #22C55E; transform: rotateY(-20deg); padding: 10px; font-family: monospace; font-size: 10px; color: black; background: white;">
                        <b>{l['titulo'].upper()}</b><br>{l['cdd']}<br>{l['ed']}<br>{l['ex']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
              
