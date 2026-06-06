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
                        "titulo": titulo.strip(), 
                        "cdd": classificacao.strip(), 
                        "paginas": str(paginas),
                        "dimensao": dimensao.strip(),
                        "ed": edicao.strip(),
                        "ex": exemplar.strip(),
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
                    qtd_pags = int(float(pags)) if str(pags).replace('.','',1).isdigit() else 100
                except:
                    qtd_pags = 100
                ajuste = (qtd_pags / 2) * 0.1 + 2.0
                st.session_state.livros.append({
                    "titulo": str(row.get('titulo', 'Sem título')).strip(), 
                    "cdd": str(row.get('cdd', row.get('classificacao', ''))).strip(), 
                    "paginas": str(qtd_pags),
                    "dimensao": str(row.get('dimensao', '')).strip(),
                    "ed": str(row.get('ed', row.get('edicao', '1.ed.'))).strip(),
                    "ex": str(row.get('ex', row.get('exemplar', 'Ex.1'))).strip(),
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
        st.write("👉 **Toque no botão do livro para abrir a calibragem detalhada:**")
        
        cols_botoes = st.columns(len(st.session_state.livros))
        for i, livro in enumerate(st.session_state.livros):
            with cols_botoes[i]:
                # Proteção adicionada aqui para evitar erro de tipo
                titulo_seguro = str(livro.get("titulo") or "Sem título")
                if st.button(f"{titulo_seguro[:12]}...", key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                    st.session_state.mostrar_3d = True
                    st.rerun()
        
        html_estante = "<div style='display: flex; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 25px; min-height: 260px; background-color: #f9f9f9; border-radius: 10px; overflow-x: auto;'>"
        
        for i, livro in enumerate(st.session_state.livros):
            largura_lombada = max(livro.get('ajuste', 15.0) * 4, 80) 
            borda_selecao = "outline: 3px solid #4B0082;" if (st.session_state.mostrar_3d and st.session_state.livro_ativo == i) else ""
            
            t_tit = str(livro.get('titulo', 'Livro'))
            t_cdd = livro.get('cdd', '')
            t_ed = livro.get('ed', '')
            t_ex = livro.get('ex', '')
            
            html_estante += f'<div style="flex: 0 0 {largura_lombada}px; width: {largura_lombada}px; height: 210px; background: #A084E8; border-radius: 3px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; color: white; box-shadow: 4px 4px 8px rgba(0,0,0,0.2); position: relative; {borda_selecao} padding: 8px 2px 0 2px; box-sizing: border-box;"><div style="font-size: 10px; font-weight: bold; text-align: center; width: 100%; word-wrap: break-word; overflow: hidden; max-height: 50px; line-height: 1.1;">{t_tit}</div><div style="width: 100%; background: white; color: black; font-family: \'Courier New\', monospace; font-size: 10px; border-top: 1px solid #bbb; padding: 4px 0; text-align: center; box-sizing: border-box; line-height: 1.1;"><div style="font-weight: bold; font-size: 9px; border-bottom: 1px solid #ddd; margin-bottom: 2px;">{t_tit[:10].upper()}</div><div style="font-weight: bold; font-size: 10px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; padding: 0 1px;">{t_cdd}</div><div style="font-size: 9px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{t_ed}</div><div style="font-size: 9px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{t_ex}</div></div></div>'
            
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)
        
        st.write(" ")
        st.write("---")
        
        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            livro_sel = st.session_state.livros[idx]
            
            col_ajustes, col_3d = st.columns([1.2, 1])
            
            with col_ajustes:
                st.subheader(f"⚙️ Ajustar Espessura: {livro_sel.get('titulo', 'Livro')}")
                novo_val = st.slider("Largura da Lombada (mm)", 1.0, 50.0, float(livro_sel.get('ajuste', 15.0)), 0.5)
                st.session_state.livros[idx]['ajuste'] = novo_val
            
            with col_3d:
                st.subheader("🔍 Visualização Detalhada da Lombada")
                esp_3d = max(livro_sel.get('ajuste', 15.0) * 6, 60)
                
                html_renderizado = f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; margin-top: 20px; height: 320px;">
                    <div style="width: {esp_3d}px; height: 280px; background: #A084E8; border: 5px solid #22C55E; transform: rotateY(-20deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.4); display: flex; flex-direction: column; justify-content: flex-end; position: relative;">
                        <div style="width: 100%; height: 120px; background: white; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: 'Courier New', monospace; font-size: 11px; color: black; border-top: 1px solid #ccc; padding: 2px; line-height: 1.1; overflow: hidden;">
                            <div style="text-align: center; font-weight: bold; font-size: 10px; margin-bottom: 5px; border-bottom: 1px solid #999; width: 90%;">{str(livro_sel.get('titulo', '')).upper()}</div>
                            <div style="text-align: center; font-weight: bold; font-size: 11px; width: 100%;">{livro_sel.get('cdd', '')}</div>
                            <div style="text-align: center; font-size: 10px; margin-top: 2px;">{livro_sel.get('ed', '')}</div>
                            <div style="text-align: center; font-size: 10px;">{livro_sel.get('ex', '')}</div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(html_renderizado, unsafe_allow_html=True)
