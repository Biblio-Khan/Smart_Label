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

# --- INICIALIZAÇÃO DOS CAMPOS PERMANENTES DA BIBLIOTECA ---
if "cfg_exibir_cdd" not in st.session_state:
    st.session_state.cfg_exibir_cdd = True
if "cfg_exibir_ed" not in st.session_state:
    st.session_state.cfg_exibir_ed = True
if "cfg_exibir_ex" not in st.session_state:
    st.session_state.cfg_exibir_ex = True

if "cfg_usar_extra1" not in st.session_state:
    st.session_state.cfg_usar_extra1 = False
if "cfg_nome_extra1" not in st.session_state:
    st.session_state.cfg_nome_extra1 = "Cutter"

if "cfg_usar_extra2" not in st.session_state:
    st.session_state.cfg_usar_extra2 = False
if "cfg_nome_extra2" not in st.session_state:
    st.session_state.cfg_nome_extra2 = "Coleção"

# --- SIDEBAR: PAINEL DE CUSTOMIZAÇÃO PERMANENTE ---
st.sidebar.title("⚙️ Customizar Etiqueta")
st.sidebar.write("Defina o padrão visual da sua biblioteca:")

# Checkboxes vinculados ao estado permanente
exibir_cdd = st.sidebar.checkbox("Exibir Classificação (CDD/CDU)", value=st.session_state.cfg_exibir_cdd)
exibir_ed = st.sidebar.checkbox("Exibir Edição", value=st.session_state.cfg_exibir_ed)
exibir_ex = st.sidebar.checkbox("Exibir Exemplar", value=st.session_state.cfg_exibir_ex)

st.sidebar.write("---")
st.sidebar.write("➕ Campos Customizados:")

usar_extra1 = st.sidebar.checkbox("Ativar Campo Extra 1", value=st.session_state.cfg_usar_extra1)
nome_extra1 = st.session_state.cfg_nome_extra1
if usar_extra1:
    nome_extra1 = st.sidebar.text_input("Nome do Campo 1 (ex: Cutter)", value=st.session_state.cfg_nome_extra1)

usar_extra2 = st.sidebar.checkbox("Ativar Campo Extra 2", value=st.session_state.cfg_usar_extra2)
nome_extra2 = st.session_state.cfg_nome_extra2
if usar_extra2:
    nome_extra2 = st.sidebar.text_input("Nome do Campo 2 (ex: Coleção)", value=st.session_state.cfg_nome_extra2)

st.sidebar.write("---")
# Botão para travar a configuração permanentemente na sessão
if st.sidebar.button("💾 Tornar Campos Permanentes", type="primary", use_container_width=True):
    st.session_state.cfg_exibir_cdd = exibir_cdd
    st.session_state.cfg_exibir_ed = exibir_ed
    st.session_state.cfg_exibir_ex = exibir_ex
    st.session_state.cfg_usar_extra1 = usar_extra1
    st.session_state.cfg_nome_extra1 = nome_extra1
    st.session_state.cfg_usar_extra2 = usar_extra2
    st.session_state.cfg_nome_extra2 = nome_extra2
    st.sidebar.success("Padrão da biblioteca salvo!")

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
            
            # Inputs dinâmicos baseados no que está ativo/salvo no sistema
            val_extra1 = ""
            if usar_extra1:
                val_extra1 = st.text_input(f"{nome_extra1}")
                
            val_extra2 = ""
            if usar_extra2:
                val_extra2 = st.text_input(f"{nome_extra2}")
            
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
                        "extra1": val_extra1.strip() if val_extra1 else "",
                        "extra2": val_extra2.strip() if val_extra2 else "",
                        "ajuste": min(ajuste, 50.0)
                    })
                    st.success(f"'{titulo}' adicionado!")
                else:
                    st.error("Por favor, preencha Título e Classificação.")
    
    with col2:
        st.subheader("Importar via CSV")
        info_csv = f"O CSV deve conter: titulo, cdd, paginas, dimensao, ed, ex."
        if usar_extra1: info_csv += f" Envie também a coluna: {nome_extra1.lower()}"
        if usar_extra2: info_csv += f" Envie também a coluna: {nome_extra2.lower()}"
        st.info(info_csv)
        
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
                    "titulo": str(row.get('titulo', 'Sem título')).strip(), 
                    "cdd": str(row.get('cdd', row.get('classificacao', ''))).strip(), 
                    "paginas": str(qtd_pags),
                    "dimensao": str(row.get('dimensao', '')).strip(),
                    "ed": str(row.get('ed', row.get('edicao', '1.ed.'))).strip(),
                    "ex": str(row.get('ex', row.get('exemplar', 'Ex.1'))).strip(),
                    "extra1": str(row.get(nome_extra1.lower(), '')).strip(),
                    "extra2": str(row.get(nome_extra2.lower(), '')).strip(),
                    "ajuste": min(ajuste, 50.0)
                })
            st.success("Dados importados com sucesso!")

    if st.button("Ir para Estante de Calibragem ➡️", type="primary"):
        mudar_tela("calibragem")
        st.rerun()

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM (Preservada e Intocável)
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
                if st.button(f"👁️ {livro.get('titulo')[:12]}...", key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                    st.session_state.mostrar_3d = True
                    st.rerun()
        
        # --- ESTANTE DIGITAL PROTEGIDA (CÓDIGO ÚNICO EM LINHA - EM PARCERIA COM AS CONFIGURAÇÕES ATIVAS) ---
        html_estante = "<div style='display: flex; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 25px; min-height: 260px; background-color: #f9f9f9; border-radius: 10px; overflow-x: auto;'>"
        
        for i, livro in enumerate(st.session_state.livros):
            largura_lombada = max(livro.get('ajuste', 15.0) * 4, 85) 
            borda_selecao = "outline: 3px solid #4B0082;" if (st.session_state.mostrar_3d and st.session_state.livro_ativo == i) else ""
            
            t_tit = livro.get('titulo', 'Livro')
            
            linhas_etiqueta = ""
            if exibir_cdd:
                linhas_etiqueta += f'<div style="font-weight: bold; font-size: 10px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; padding: 0 1px;">{livro.get("cdd", "")}</div>'
            if usar_extra1 and livro.get("extra1"):
                linhas_etiqueta += f'<div style="font-size: 9px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #1E3A8A; font-weight: bold;">{livro.get("extra1", "")}</div>'
            if exibir_ed:
                linhas_etiqueta += f'<div style="font-size: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{livro.get("ed", "")}</div>'
            if exibir_ex:
                linhas_etiqueta += f'<div style="font-size: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{livro.get("ex", "")}</div>'
            if usar_extra2 and livro.get("extra2"):
                linhas_etiqueta += f'<div style="font-size: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #065F46;">{livro.get("extra2", "")}</div>'
            
            altura_etiqueta_estante = "65px" if (usar_extra1 or usar_extra2) else "55px"

            html_estante += f'<div style="flex: 0 0 {largura_lombada}px; width: {largura_lombada}px; height: 210px; background: #A084E8; border-radius: 3px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; color: white; box-shadow: 4px 4px 8px rgba(0,0,0,0.2); position: relative; {borda_selecao} padding: 8px 2px 0 2px; box-sizing: border-box;"><div style="font-size: 10px; font-weight: bold; text-align: center; width: 100%; word-wrap: break-word; overflow: hidden; max-height: 50px; line-height: 1.1;">{t_tit}</div><div style="width: 100%; background: white; color: black; font-family: \'Courier New\', monospace; font-size: 10px; border-top: 1px solid #ccc; padding: 4px 0; text-align: center; box-sizing: border-box; line-height: 1.1; min-height: {altura_etiqueta_estante}; display: flex; flex-direction: column; justify-content: center;">{linhas_etiqueta}</div></div>'
            
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)
        
        st.write(" ")
        st.write("---")
        
        # ==========================================================
        # INTERFACE INFERIOR LADO A LADO
        # ==========================================================
        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            livro_sel = st.session_state.livros[idx]
            
            col_ajustes, col_3d = st.columns([1.2, 1])
            
            with col_ajustes:
                st.subheader(f"⚙️ Ajustar Espessura: {livro_sel.get('titulo', 'Livro')}")
                
                pags_txt = livro_sel.get('paginas', 'Não informada')
                dim_txt = livro_sel.get('dimensao', '')
                
                st.markdown(f"""
                **Informações Registradas:**
                * **Título:** {livro_sel.get('titulo')}
                * **Páginas:** {pags_txt} pág.
                * **Dimensão:** {dim_txt if dim_txt and dim_txt != 'nan' else 'Não informada'}
                """)
                
                if usar_extra1 or usar_extra2:
                    st.write("**Campos Adicionais da Biblioteca:**")
                    if usar_extra1:
                        st.session_state.livros[idx]["extra1"] = st.text_input(f"Editar {nome_extra1}:", value=livro_sel.get("extra1", ""))
                    if usar_extra2:
                        st.session_state.livros[idx]["extra2"] = st.text_input(f"Editar {nome_extra2}:", value=livro_sel.get("extra2", ""))
                
                st.write("---")
                novo_val = st.slider(
                    "Largura da Lombada (mm)", 1.0, 50.0, float(livro_sel.get('ajuste', 15.0)), 0.5, key="slider_lombada"
                )
                st.session_state.livros[idx]['ajuste'] = novo_val
                
                if novo_val < 5.0:
                    st.error("⚠️ ATENÇÃO: Lombada muito fina (abaixo de 5mm). Use etiqueta de capa!")
                else:
                    st.success("✅ Espessura ideal para etiqueta de lombada.")
            
            with col_3d:
                st.subheader("🔍 Visualização Detalhada da Lombada")
                
                val_atual = st.session_state.livros[idx]['ajuste']
                cor_borda = "#EF4444" if val_atual < 5.0 else "#22C55E"
                esp_3d = max(val_atual * 6, 60)
                
                linhas_3d = ""
                if exibir_cdd:
                    linhas_3d += f'<div style="text-align: center; font-weight: bold; font-size: 11px; width: 100%; word-wrap: break-word;">{livro_sel.get("cdd", "")}</div>'
                if usar_extra1 and livro_sel.get("extra1"):
                    linhas_3d += f'<div style="text-align: center; font-size: 10px; margin-top: 2px; font-weight: bold; color: #1E3A8A;">{livro_sel.get("extra1", "")}</div>'
                if exibir_ed:
                    linhas_3d += f'<div style="text-align: center; font-size: 10px; margin-top: 2px;">{livro_sel.get("ed", "")}</div>'
                if exibir_ex:
                    linhas_3d += f'<div style="text-align: center; font-size: 10px;">{livro_sel.get("ex", "")}</div>'
                if usar_extra2 and livro_sel.get("extra2"):
                    linhas_3d += f'<div style="text-align: center; font-size: 10px; color: #065F46; font-weight: bold;">{livro_sel.get("extra2", "")}</div>'

                altura_etiqueta_3d = "110px" if (usar_extra1 or usar_extra2) else "95px"

                html_renderizado = f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; margin-top: 20px; height: 320px;">
                    <div style="width: {esp_3d}px; height: 280px; background: #A084E8; border: 5px solid {cor_borda}; transform: rotateY(-20deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.4); display: flex; flex-direction: column; justify-content: flex-end; position: relative;">
                        <div style="width: 100%; min-height: {altura_etiqueta_3d}; background: white; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: 'Courier New', monospace; font-size: 11px; color: black; border-top: 1px solid #ccc; padding: 4px 2px; line-height: 1.2; overflow: hidden; box-sizing: border-box;">
                            {linhas_3d}
                        </div>
                    </div>
                    <div style="width: 140px; height: 280px; background: #D1D5DB; transform-origin: left; transform: rotateY(30deg); box-shadow: 20px 10px 30px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; color: #4B5563; font-size: 12px; font-weight: bold;">CAPA</div>
                </div>
                """
                st.markdown(html_renderizado, unsafe_allow_html=True)
