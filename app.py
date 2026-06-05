import streamlit as st
import pandas as pd

# Configuração de página com layout amplo
st.set_page_config(layout="wide", page_title="BiblioKhan Pro", page_icon="📚")

# ==========================================================
# INJEÇÃO DE INFORMAÇÕES VISUAIS PREMIUM (CSS FORÇADO PARA TABLÉ)
# ==========================================================
st.markdown("""
    <style>
        .stApp {
            background-color: #f8fafc;
        }
        .custom-card {
            background-color: #ffffff;
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }
        
        /* FORÇA AS COLUNAS A FICAREM LADO A LADO NO TABLET SEM QUEBRAR LINHA */
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            width: 100% !important;
            gap: 15px !important;
        }
        
        /* Ajusta o tamanho da coluna do formulário */
        [data-testid="stHorizontalBlock"] > div:nth-child(1) {
            min-width: 60% !important;
            max-width: 60% !important;
        }
        
        /* Ajusta o tamanho da coluna do preview */
        [data-testid="stHorizontalBlock"] > div:nth-child(2) {
            min-width: 40% !important;
            max-width: 40% !important;
        }
        
        /* Compacta os espaços internos para caber tudo na tela do tablet */
        .stTextInput div div input {
            padding: 4px 8px !important;
            height: 32px !important;
        }
        .stNumberInput div div input {
            padding: 4px 8px !important;
            height: 32px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO STATE ---
if "tela" not in st.session_state: st.session_state.tela = "entrada"
if "livros" not in st.session_state: st.session_state.livros = []
if "livro_ativo" not in st.session_state: st.session_state.livro_ativo = 0
if "mostrar_3d" not in st.session_state: st.session_state.mostrar_3d = False
if "mensagem_sucesso" not in st.session_state: st.session_state.mensagem_sucesso = ""

if "campos_extras_dinamicos" not in st.session_state:
    st.session_state.campos_extras_dinamicos = {
        "Cutter": {"ativo": True, "valor": ""},
        "Coleção": {"ativo": False, "valor": ""}
    }

if "cfg_ordem_linhas" not in st.session_state:
    st.session_state.cfg_ordem_linhas = ["Classificação", "Cutter", "Edição", "Exemplar", "Coleção"]

if "cfg_exibir_cdd" not in st.session_state: st.session_state.cfg_exibir_cdd = True
if "cfg_exibir_ed" not in st.session_state: st.session_state.cfg_exibir_ed = True
if "cfg_exibir_ex" not in st.session_state: st.session_state.cfg_exibir_ex = True

def mudar_tela(nova_tela):
    st.session_state.tela = nova_tela

# ==========================================================
# TELA 1: ENTRADA DE DADOS
# ==========================================================
if st.session_state.tela == "entrada":
    
    # Barra Superior
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 10px 20px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 15px;">
            <div style="font-size: 18px; font-weight: bold; color: #1e3a8a;">📚 BIBLIOKHAN SMART</div>
            <div style="font-size: 12px; color: #64748b; font-weight: 500;">Modo: Administrador ⚙️</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.mensagem_sucesso:
        st.success(st.session_state.mensagem_sucesso)
        st.session_state.mensagem_sucesso = ""

    # Divisão Principal: Área de Trabalho (Esquerda) e Fila Curta (Direita)
    col_esquerda, col_direita = st.columns([1.8, 0.5])
    
    with col_esquerda:
        aba_manual, aba_lote = st.tabs(["📝 Cadastro Manual & Configurações", "📥 Importação em Lote"])
        
        with aba_manual:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            
            # Subcolunas internas que eram jogadas para baixo e agora estão travadas lado a lado
            col_form, col_preview = st.columns([1.2, 0.8])
            
            with col_form:
                st.markdown('<p style="font-weight:bold; margin-bottom:2px;">Propriedades do Livro</p>', unsafe_allow_html=True)
                titulo_input = st.text_input("Título do Livro *", placeholder="Ex: O Senhor dos Anéis", label_visibility="collapsed")
                
                st.markdown('<p style="font-weight:bold; margin-top:6px; margin-bottom:2px;">Classificação (CDD/CDU) *</p>', unsafe_allow_html=True)
                cdd_input = st.text_input("Classificação *", placeholder="Ex: 823.91", label_visibility="collapsed")
                
                c1, c2 = st.columns(2)
                paginas_input = c1.number_input("Páginas", min_value=1, value=100)
                dimensao_input = c2.text_input("Dimensão", placeholder="Ex: 23 cm")
                
                c3, c4 = st.columns(2)
                edicao_input = c3.text_input("Edição", value="1.ed.")
                exemplar_input = c4.text_input("Exemplar", value="Ex.1")
                
                # Campos extras dinâmicos
                valores_extras = {}
                for nome_campo, info in st.session_state.campos_extras_dinamicos.items():
                    if info["ativo"]:
                        st.markdown(f'<p style="font-weight:bold; margin-top:6px; margin-bottom:2px;">{nome_campo}</p>', unsafe_allow_html=True)
                        valores_extras[nome_campo] = st.text_input(nome_campo, placeholder=f"Digite...", label_visibility="collapsed")
                    else:
                        valores_extras[nome_campo] = ""

                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                st.markdown('<p style="font-weight:bold; margin-bottom:2px;">➕ Criar Novo Campo Extra</p>', unsafe_allow_html=True)
                
                c_novo1, c_novo2 = st.columns([1.2, 0.8])
                novo_nome_campo = c_novo1.text_input("Nome do campo", placeholder="Ex: Volume, Editora...", label_visibility="collapsed")
                if c_novo2.button("Adicionar", use_container_width=True):
                    nome_limpo = novo_nome_campo.strip()
                    if nome_limpo and nome_limpo not in st.session_state.campos_extras_dinamicos:
                        st.session_state.campos_extras_dinamicos[nome_limpo] = {"ativo": True, "valor": ""}
                        st.session_state.cfg_ordem_linhas.append(nome_limpo)
                        st.rerun()

            with col_preview:
                st.markdown('<p style="font-weight:bold; margin-bottom:5px;">Configuração & Preview</p>', unsafe_allow_html=True)
                
                st.session_state.cfg_exibir_cdd = st.checkbox("Exibir CDD", value=st.session_state.cfg_exibir_cdd)
                st.session_state.cfg_exibir_ed = st.checkbox("Exibir Edição", value=st.session_state.cfg_exibir_ed)
                st.session_state.cfg_exibir_ex = st.checkbox("Exibir Exemplar", value=st.session_state.cfg_exibir_ex)
                
                for nome_campo in list(st.session_state.campos_extras_dinamicos.keys()):
                    is_ativo = st.checkbox(f"Ativar {nome_campo}", value=st.session_state.campos_extras_dinamicos[nome_campo]["ativo"], key=f"chk_{nome_campo}")
                    st.session_state.campos_extras_dinamicos[nome_campo]["ativo"] = is_ativo

                # Ordenação estruturada
                nomes_mapeados = {
                    "Classificação": "Classificação" if st.session_state.cfg_exibir_cdd else None,
                    "Edição": "Edição" if st.session_state.cfg_exibir_ed else None,
                    "Exemplar": "Exemplar" if st.session_state.cfg_exibir_ex else None,
                }
                for nome_campo, info in st.session_state.campos_extras_dinamicos.items():
                    if info["ativo"]:
                        nomes_mapeados[nome_campo] = nome_campo

                itens_ativos = [k for k, v in nomes_mapeados.items() if v is not None]
                
                nova_ordem_vistas = []
                if itens_ativos:
                    for rank in range(min(3, len(itens_ativos))): # Limita selects visuais para poupar espaço vertical no tablet
                        opcoes_disponiveis = [x for x in itens_ativos if x not in nova_ordem_vistas]
                        default_idx = 0
                        if rank < len(st.session_state.cfg_ordem_linhas) and st.session_state.cfg_ordem_linhas[rank] in opcoes_disponiveis:
                            default_idx = opcoes_disponiveis.index(st.session_state.cfg_ordem_linhas[rank])
                        
                        escolha = st.selectbox(f"L{rank+1}:", opcoes_disponiveis, index=default_idx, key=f"sel_ordem_{rank}")
                        nova_ordem_vistas.append(escolha)
                    
                    # Preenche o resto automaticamente para não dar erro
                    for sobrou in itens_ativos:
                        if sobrou not in nova_ordem_vistas:
                            nova_ordem_vistas.append(sobrou)
                    st.session_state.cfg_ordem_linhas = nova_ordem_vistas

                # --- EMBLEMA IMPRESSO DA ETIQUETA ---
                dados_etiqueta = {
                    "Classificação": cdd_input if cdd_input else "---",
                    "Edição": edicao_input if edicao_input else "---",
                    "Exemplar": exemplar_input if exemplar_input else "---"
                }
                dados_etiqueta.update(valores_extras)
                
                tamanho_fonte_titulo = "10px" if len(titulo_input) < 20 else "8px"
                html_preview = f'<div style="font-size: {tamanho_fonte_titulo}; font-weight: bold; border-bottom: 1px solid #cbd5e1; margin-bottom: 4px; padding-bottom: 2px; width: 100%; word-wrap: break-word; line-height: 1.1;">{titulo_input.upper() if titulo_input else "TÍTULO DO LIVRO"}</div>'
                
                for tag in st.session_state.cfg_ordem_linhas:
                    if tag in dados_etiqueta:
                        estilo_linha = "font-weight: bold; font-size: 12px;" if tag in ["Classificação"] or tag in st.session_state.campos_extras_dinamicos else "font-size: 10px;"
                        html_preview += f'<div style="{estilo_linha}">{dados_etiqueta[tag] if dados_etiqueta[tag] else "---"}</div>'
                    
                st.markdown(f"""
                    <div style="display: flex; background: #f8fafc; padding: 5px; border-radius: 8px; border: 1px solid #e2e8f0; justify-content: center; margin-top: 10px;">
                        <div style="width: 115px; min-height: 130px; background: white; color: black; border: 1px solid #94a3b8; font-family: monospace; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            {html_preview}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Botão de Envio posicionado na base do formulário
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Adicionar à Fila 📥", type="primary", use_container_width=True):
                if titulo_input.strip() and cdd_input.strip():
                    ajuste = (paginas_input / 2) * 0.1 + 2.0
                    novo_livro = {
                        "titulo": titulo_input.strip(), "cdd": cdd_input.strip(), "paginas": str(paginas_input),
                        "dimensao": dimensao_input.strip(), "ed": edicao_input.strip(), "ex": exemplar_input.strip(),
                        "ajuste": min(ajuste, 50.0)
                    }
                    for k, v in valores_extras.items():
                        novo_livro[k] = v.strip() if v else ""
                    st.session_state.livros.append(novo_livro)
                    st.session_state.mensagem_sucesso = f"🎉 Inserido!"
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)

        with aba_lote:
            st.markdown('<div class="custom-card">Processamento em Lote</div>', unsafe_allow_html=True)
            file = st.file_uploader("Upload CSV", type=["csv", "xlsx"])
            if file:
                df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
                for _, row in df.iterrows():
                    st.session_state.livros.append({
                        "titulo": str(row.get('titulo', 'Sem título')), "cdd": str(row.get('cdd', '')),
                        "paginas": "100", "dimensao": "", "ed": "1.ed.", "ex": "Ex.1", "ajuste": 15.0
                    })
                st.rerun()

    with col_direita:
        st.markdown('<div class="custom-card" style="text-align:center;">', unsafe_allow_html=True)
        st.metric(label="Fila", value=len(st.session_state.livros))
        if st.button("Estante ➡️", type="primary", use_container_width=True):
            mudar_tela("calibragem")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.markdown('### 📚 Estante de Calibragem')
    if st.button("⬅️ Voltar"):
        mudar_tela("entrada")
        st.rerun()
        
    if not st.session_state.livros:
        st.warning("Fila vazia.")
    else:
        html_estante = "<div style='display: flex; align-items: flex-end; border-bottom: 15px solid #5D4037; padding: 10px; gap: 10px; background: #f1f5f9; overflow-x: auto;'>"
        for i, libro in enumerate(st.session_state.livros):
            largura = max(libro.get('ajuste', 15.0) * 3, 70)
            html_estante += f"""
            <div style="flex: 0 0 {largura}px; width: {largura}px; height: 160px; background: #3b82f6; color: white; display: flex; flex-direction: column; justify-content: space-between; padding: 4px; text-align: center;">
                <div style="font-size: 9px; font-weight: bold;">{libro['titulo'][:10]}</div>
                <div style="background: white; color: black; font-size: 9px; font-family: monospace; padding: 1px;">
                    <div><b>{libro['cdd']}</b></div>
                </div>
            </div>
            """
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)
