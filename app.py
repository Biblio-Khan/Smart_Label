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
if "campos_personalizados" not in st.session_state:
    st.session_state.campos_personalizados = []

def mudar_tela(nova_tela):
    st.session_state.tela = nova_tela

# ==========================================================
# TELA 1: ENTRADA DE DADOS E CONFIGURAÇÃO
# ==========================================================
if st.session_state.tela == "entrada":
    st.title("📝 BiblioKhan | Entrada de Dados")
    
    aba_manual, aba_upload = st.tabs(["📝 Cadastro Manual e Configuração", "📥 Upload CSV"])
    
    with aba_manual:
        # Colunas: Form, Config/Preview
        col_form, col_extra = st.columns([1, 1])
        
        with col_form:
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
                
                valores_dinamicos = {}
                for campo in st.session_state.campos_personalizados:
                    valores_dinamicos[campo] = st.text_input(campo)
                
                if st.form_submit_button("Adicionar à Lista"):
                    if titulo and classificacao:
                        ajuste = (paginas / 2) * 0.1 + 2.0
                        novo_livro = {
                            "titulo": titulo.strip(), "cdd": classificacao.strip(), "paginas": str(paginas),
                            "dimensao": dimensao.strip(), "ed": edicao.strip(), "ex": exemplar.strip(),
                            "ajuste": min(ajuste, 50.0)
                        }
                        novo_livro.update(valores_dinamicos)
                        st.session_state.livros.append(novo_livro)
                        st.success(f"'{titulo}' adicionado!")
                    else:
                        st.error("Preencha Título e Classificação.")
        
        with col_extra:
            st.subheader("⚙️ Configurar Campos")
            novo_campo = st.text_input("Novo Campo para Etiqueta:")
            if st.button("Adicionar Campo"):
                if novo_campo.strip() and novo_campo.strip() not in st.session_state.campos_personalizados:
                    st.session_state.campos_personalizados.append(novo_campo.strip())
                    st.rerun()
            
            st.subheader("👁️ Pré-visualização")
            st.markdown(f"""
                <div style="border: 2px solid #333; width: 150px; padding: 10px; font-family: monospace; font-size: 12px; background: #fff; color: #000;">
                    <b>{titulo if titulo else 'TÍTULO'}</b><br>
                    {classificacao if classificacao else '000.00'}<br>
                    {edicao}<br>
                    {exemplar}
                </div>
            """, unsafe_allow_html=True)

    with aba_upload:
        st.info("O arquivo deve conter: titulo, cdd, paginas, dimensao, ed, ex")
        file = st.file_uploader("Subir arquivo CSV", type=["csv"])
        if file:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower()
            for _, row in df.iterrows():
                novo_livro = {"titulo": str(row.get('titulo', '')), "cdd": str(row.get('cdd', '')), "paginas": "100", "ed": str(row.get('ed', '')), "ex": str(row.get('ex', '')), "ajuste": 15.0}
                st.session_state.livros.append(novo_livro)
            st.success("Dados importados!")

    if st.button("Ir para Estante ➡️", type="primary"):
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
        cols = st.columns(len(st.session_state.livros))
        for i, livro in enumerate(st.session_state.livros):
            with cols[i]:
                if st.button(f"👁️ {livro['titulo'][:8]}", key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                    st.session_state.mostrar_3d = True
                    st.rerun()
                if st.button(f"🗑️ Del", key=f"del_{i}"):
                    st.session_state.livros.pop(i)
                    st.rerun()
        
        html_estante = "<div style='display: flex; gap: 10px; border-bottom: 20px solid #5D4037; padding: 20px;'>"
        for livro in st.session_state.livros:
            html_estante += f"<div style='width: 80px; height: 200px; background: #A084E8; color: white; padding: 5px; font-size: 10px;'>{livro['titulo']}</div>"
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)

        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            st.subheader(f"⚙️ Ajustar {st.session_state.livros[idx]['titulo']}")
            st.session_state.livros[idx]['ajuste'] = st.slider("Largura (mm)", 1.0, 50.0, float(st.session_state.livros[idx]['ajuste']))
