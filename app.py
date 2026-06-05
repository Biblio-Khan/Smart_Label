import streamlit as st
import pandas as pd

# Configuração da página para usar o espaço máximo disponível
st.set_page_config(layout="wide", page_title="BiblioKhan Smart", page_icon="📚")

# ==========================================================
# ESTILOS E AMBIENTE 3D DA ESTANTE
# ==========================================================
st.markdown("""
    <style>
        .stApp { background-color: #f8fafc; }
        .bloco-branco {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 15px;
        }
        
        /* CENÁRIO DA ESTANTE DE MADEIRA */
        .estante-container {
            background: #f1f5f9;
            padding: 30px 20px 10px 20px;
            border-radius: 8px;
            overflow-x: auto;
            white-space: nowrap;
            margin-bottom: 20px;
            box-shadow: inset 0 4px 10px rgba(0,0,0,0.05);
        }
        
        .prateleira-3d {
            display: inline-flex;
            align-items: flex-end;
            gap: 15px;
            padding-bottom: 10px;
            border-bottom: 18px solid #5d4037; /* Madeira da Prateleira */
            perspective: 800px;
            perspective-origin: 50% -20%;
            min-width: 100%;
        }
        
        /* O LIVRO INDIVIDUAL EM 3D */
        .livro-container-3d {
            display: inline-block;
            width: var(--lombada-largura);
            height: 180px;
            position: relative;
            transform-style: preserve-3d;
            transform: rotateX(10deg) rotateY(-20deg); /* Angulação para ver a lombada e a lateral */
            transition: transform 0.3s;
            margin-right: 10px;
        }
        
        .livro-container-3d:hover {
            transform: rotateX(5deg) rotateY(-10deg) translateZ(10px);
        }
        
        /* FACE: LOMBADA DO LIVRO (FRENTE PARA O USUÁRIO) */
        .lombada-3d {
            position: absolute;
            width: var(--lombada-largura);
            height: 180px;
            background: #2563eb;
            color: white;
            font-family: monospace;
            box-shadow: inset -3px 0 8px rgba(0,0,0,0.3), 2px 2px 5px rgba(0,0,0,0.15);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            left: 0;
            top: 0;
            transform: translateZ(50px); /* Joga para a frente do bloco */
            overflow: hidden;
        }
        
        /* FACE: CAPA DO LIVRO (LATERAL ESQUERDA) */
        .capa-3d {
            position: absolute;
            width: 100px; /* Profundidade do livro na estante */
            height: 180px;
            background: #1d4ed8;
            border-radius: 0 4px 4px 0;
            left: 0;
            top: 0;
            transform: rotateY(-90deg);
            transform-origin: left center;
            box-shadow: inset 5px 0 10px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            color: rgba(255,255,255,0.7);
            font-size: 10px;
            font-weight: bold;
            padding: 10px;
            white-space: normal;
            word-wrap: break-word;
            text-align: center;
        }
        
        /* FACE: PÁGINAS DO LIVRO (LATERAL DIREITA) */
        .paginas-3d {
            position: absolute;
            width: 100px;
            height: 176px;
            background: #f8fafc;
            top: 2px;
            right: 0;
            transform: rotateY(90deg);
            transform-origin: right center;
            background-image: linear-gradient(90deg, #cbd5e1 1px, transparent 1px);
            background-size: 3px 100%;
        }
        
        /* MINI MINI ETIQUETA COLADA NA LOMBADA */
        .mini-etiqueta-lombada {
            background: white;
            color: black;
            padding: 4px 2px;
            width: 85%;
            font-size: 8px;
            text-align: center;
            border-radius: 2px;
            font-weight: bold;
            line-height: 1.1;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO STATE ---
if "tela" not in st.session_state: st.session_state.tela = "entrada"
if "livros" not in st.session_state: st.session_state.livros = []
if "mensagem_sucesso" not in st.session_state: st.session_state.mensagem_sucesso = ""

if "campos_extras" not in st.session_state:
    st.session_state.campos_extras = {
        "Cutter": {"ativo": True},
        "Coleção": {"ativo": False}
    }

if "ordem_linhas" not in st.session_state:
    st.session_state.ordem_linhas = ["Classificação", "Cutter", "Edição", "Exemplar", "Coleção"]

if "ver_cdd" not in st.session_state: st.session_state.ver_cdd = True
if "ver_ed" not in st.session_state: st.session_state.ver_ed = True
if "ver_ex" not in st.session_state: st.session_state.ver_ex = True

# ==========================================================
# TELA PRINCIPAL: ENTRADA DE DADOS
# ==========================================================
if st.session_state.tela == "entrada":
    
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
            <div style="font-size: 18px; font-weight: bold; color: #1e3a8a;">📚 BIBLIOKHAN SMART</div>
            <div style="font-size: 12px; color: #64748b; font-weight: 500;">Modo: Administrador ⚙️</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.mensagem_sucesso:
        st.success(st.session_state.mensagem_sucesso)
        st.session_state.mensagem_sucesso = ""

    col_dados, col_controle = st.columns([1.1, 0.9], gap="large")
    
    # ------------------------------------------------------
    # COLUNA DA ESQUERDA: CADASTRO MANUAL E FILE UPLOADER
    # ------------------------------------------------------
    with col_dados:
        aba_manual, aba_upload = st.tabs(["📝 Cadastro Manual", "📥 Upload de Arquivos (CSV/Excel)"])
        
        with aba_manual:
            st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
            st.markdown("### 📝 Propriedades do Livro")
            
            titulo_input = st.text_input("Título do Livro *", placeholder="Ex: O Senhor dos Anéis", key="man_titulo")
            cdd_input = st.text_input("Classificação (CDD/CDU) *", placeholder="Ex: 823.91", key="man_cdd")
            
            c1, c2 = st.columns(2)
            paginas_input = c1.number_input("Páginas", min_value=1, value=100, key="man_paginas")
            dimensao_input = c2.text_input("Dimensão", placeholder="Ex: 23 cm", key="man_dim")
            
            c3, c4 = st.columns(2)
            edicao_input = c3.text_input("Edição", value="1.ed.", key="man_ed")
            exemplar_input = c4.text_input("Exemplar", value="Ex.1", key="man_ex")
            
            # Renderização dinâmica dos campos extras ativos
            valores_extras = {}
            for nome_campo, info in st.session_state.campos_extras.items():
                if info["ativo"]:
                    valores_extras[nome_campo] = st.text_input(f"{nome_campo}", placeholder=f"Digite o valor de {nome_campo.lower()}", key=f"inp_ext_{nome_campo}")
                else:
                    valores_extras[nome_campo] = ""
                    
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SUB-BLOCO: CRIADOR DE NOVOS CAMPOS EXTRAS
            st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
            st.markdown("### ➕ Adicionar Opção de Mais Campos")
            c_novo_nome, c_novo_btn = st.columns([1.3, 0.7])
            novo_campo = c_novo_nome.text_input("Nome do novo campo:", placeholder="Ex: Volume, ISBN...", label_visibility="collapsed", key="add_field")
            
            if c_novo_btn.button("Criar Campo", use_container_width=True, key="btn_add_field"):
                nome_limpo = novo_campo.strip()
                if nome_limpo and nome_limpo not in st.session_state.campos_extras:
                    st.session_state.campos_extras[nome_limpo] = {"ativo": True}
                    if nome_limpo not in st.session_state.ordem_linhas:
                        st.session_state.ordem_linhas.append(nome_limpo)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with aba_upload:
            st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
            st.markdown("### 📥 Importação em Lote")
            arquivo_carregado = st.file_uploader("Selecione um arquivo CSV ou Excel", type=["csv", "xlsx"], key="up_file")
            
            if arquivo_carregado is not None:
                try:
                    df = pd.read_csv(arquivo_carregado) if arquivo_carregado.name.endswith('.csv') else pd.read_excel(arquivo_carregado)
                    df.columns = df.columns.str.lower()
                    
                    if 'titulo' in df.columns and 'cdd' in df.columns:
                        st.dataframe(df[['titulo', 'cdd']].head(3), use_container_width=True)
                        if st.button("Confirmar Importação de Livros", type="primary", use_container_width=True, key="btn_confirm_upload"):
                            contador = 0
                            for _, linha in df.iterrows():
                                t_lote = str(linha['titulo']).strip()
                                c_lote = str(linha['cdd']).strip()
                                if t_lote and c_lote and t_lote != "nan" and c_lote != "nan":
                                    p_lote = int(linha['paginas']) if 'paginas' in df.columns and pd.notna(linha['paginas']) else 100
                                    calc_lombada = (p_lote / 2) * 0.1 + 2.0
                                    
                                    novo_livro = {
                                        "titulo": t_lote, "cdd": c_lote, "paginas": str(p_lote),
                                        "dimensao": str(linha['dimensao']).strip() if 'dimensao' in df.columns and pd.notna(linha['dimensao']) else "",
                                        "ed": str(linha['edicao']).strip() if 'edicao' in df.columns and pd.notna(linha['edicao']) else "1.ed.",
                                        "ex": str(linha['exemplar']).strip() if 'exemplar' in df.columns and pd.notna(linha['exemplar']) else "Ex.1",
                                        "ajuste": min(calc_lombada, 50.0)
                                    }
                                    for extra in st.session_state.campos_extras.keys():
                                        extra_lower = extra.lower()
                                        novo_livro[extra] = str(linha[extra_lower]).strip() if extra_lower in df.columns and pd.notna(linha[extra_lower]) else ""
                                    st.session_state.livros.append(novo_livro)
                                    contador += 1
                            st.session_state.mensagem_sucesso = f"🎉 Sucesso! {contador} livros adicionados via planilha."
                            st.rerun()
                    else:
                        st.error("Planilha inválida! Precisa conter as colunas 'titulo' e 'cdd'.")
                except Exception as e:
                    st.error(f"Erro ao ler arquivo: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # COLUNA DA DIREITA: PREVIEW PLANO DO ADESIVO
    # ------------------------------------------------------
    with col_controle:
        st.markdown('<div class="bloco-branco" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight: bold; margin-top: 0; color: #475569;'>👁️ PRÉ-VISUALIZAÇÃO EM TEMPO REAL</p>", unsafe_allow_html=True)
        
        t_prev = titulo_input if 'titulo_input' in locals() else ""
        c_prev = cdd_input if 'cdd_input' in locals() else ""
        e_prev = edicao_input if 'edicao_input' in locals() else "1.ed."
        ex_prev = exemplar_input if 'exemplar_input' in locals() else "Ex.1"
        ext_prev = valores_extras if 'valores_extras' in locals() else {}

        dados_etiqueta = {
            "Classificação": c_prev if c_prev else "---",
            "Edição": e_prev if e_prev else "---",
            "Exemplar": ex_prev if ex_prev else "---"
        }
        dados_etiqueta.update(ext_prev)
        
        tam_fonte = "11px" if len(t_prev) < 20 else "9px"
        html_etiqueta = f'<div style="font-size: {tam_fonte}; font-weight: bold; border-bottom: 1px solid #cbd5e1; margin-bottom: 6px; padding-bottom: 2px; width: 100%; word-wrap: break-word;">{t_prev.upper() if t_prev else "TÍTULO DO LIVRO"}</div>'
        
        for tag in st.session_state.ordem_linhas:
            if tag in dados_etiqueta:
                if tag == "Classificação" and st.session_state.ver_cdd:
                    html_etiqueta += f'<div style="font-weight: bold; font-size: 13px;">{dados_etiqueta[tag]}</div>'
                elif tag in st.session_state.campos_extras and st.session_state.campos_extras[tag]["ativo"]:
                    html_etiqueta += f'<div style="font-weight: bold; font-size: 13px;">{dados_etiqueta[tag] if dados_etiqueta[tag] else "---"}</div>'
                elif tag == "Edição" and st.session_state.ver_ed:
                    html_etiqueta += f'<div style="font-size: 11px; color:#334155;">{dados_etiqueta[tag]}</div>'
                elif tag == "Exemplar" and st.session_state.ver_ex:
                    html_etiqueta += f'<div style="font-size: 11px; color:#334155;">{dados_etiqueta[tag]}</div>'

        st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-bottom: 15px;">
                <div style="width: 130px; min-height: 145px; background: white; color: black; border: 2px solid #64748b; font-family: monospace; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); border-radius: 4px;">
                    {html_etiqueta}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # CONFIGURAÇÕES DE VISIBILIDADE DAS LINHAS
        st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Ativar/Desativar Linhas")
        st.session_state.ver_cdd = st.checkbox("Exibir Classificação (CDD)", value=st.session_state.ver_cdd)
        st.session_state.ver_ed = st.checkbox("Exibir Edição", value=st.session_state.ver_ed)
        st.session_state.ver_ex = st.checkbox("Exibir Exemplar", value=st.session_state.ver_ex)
        for nome_campo in list(st.session_state.campos_extras.keys()):
            st.session_state.campos_extras[nome_campo]["ativo"] = st.checkbox(f"Exibir {nome_campo}", value=st.session_state.campos_extras[nome_campo]["ativo"], key=f"chk_{nome_campo}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # BASE DA TELA: BOTÕES DE SALVAMENTO
    # ------------------------------------------------------
    st.markdown("---")
    c_salvar, c_fila_info = st.columns([1.5, 0.5])
    
    with c_salvar:
        if st.button("📥 Adicionar Este Livro Manual e Gerar Etiqueta", type="primary", use_container_width=True, key="btn_save_man"):
            if 'titulo_input' in locals() and titulo_input.strip() and cdd_input.strip():
                calc_lombada = (paginas_input / 2) * 0.1 + 2.0
                novo_livro = {
                    "titulo": titulo_input.strip(), "cdd": cdd_input.strip(), "paginas": str(paginas_input),
                    "dimensao": dimensao_input.strip(), "ed": edicao_input.strip(), "ex": exemplar_input.strip(),
                    "ajuste": min(calc_lombada, 50.0)
                }
                for k, v in valores_extras.items():
                    novo_livro[k] = v.strip() if v else ""
                st.session_state.livros.append(novo_livro)
                st.session_state.mensagem_sucesso = f"✔️ Livro '{titulo_input.strip()}' adicionado com sucesso!"
                st.rerun()
            else:
                st.error("Preencha o Título e a Classificação antes de salvar!")
                
    with c_fila_info:
        if st.button(f"📋 Ver Estante (Fila: {len(st.session_state.livros)}) ➡️", use_container_width=True, key="btn_go_calib"):
            st.session_state.tela = "calibragem"
            st.rerun()

# ==========================================================
# TELA DA ESTANTE DE CALIBRAGEM (AGORA EM 3D REAL!)
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.markdown("### 📚 Estante de Calibragem Física (Fila de Impressão)")
    
    if st.button("⬅️ Voltar para o Cadastro"):
        st.session_state.tela = "entrada"
        st.rerun()
        
    if not st.session_state.livros:
        st.warning("Nenhum livro cadastrado na fila de impressão para exibição.")
    else:
        # Monta a renderização da prateleira contendo os livros volumétricos em CSS 3D
        html_estante = '<div class="estante-container"><div class="prateleira-3d">'
        
        for idx, l in enumerate(st.session_state.livros):
            # Calcula largura proporcional da lombada com base nas páginas informadas
            p_num = int(l.get('paginas', 100))
            largura_lombada_px = min(max(int(p_num * 0.18), 24), 70) # Limita entre 24px e 70px para não deformar
            
            # Monta o texto interno da etiqueta colada na lombada física do livro
            linhas_lombada = f"<div><b>{l['cdd']}</b></div>"
            if "Cutter" in l and l["Cutter"]:
                linhas_lombada += f"<div>{l['Cutter']}</div>"
            if st.session_state.ver_ed and l.get('ed'):
                linhas_lombada += f"<div style='font-size:7px; opacity:0.8;'>{l['ed']}</div>"
                
            # Cores alternadas automáticas para a estante ficar bonita
            cores_capas = ["#2563eb", "#16a34a", "#dc2626", "#d97706", "#7c3aed", "#0891b2", "#4f46e5"]
            cor_atual = cores_capas[idx % len(cores_capas)]
            
            html_estante += f"""
            <div class="livro-container-3d" style="--lombada-largura: {largura_lombada_px}px;">
                <div class="capa-3d" style="background: {cor_atual};">{l['titulo'][:25].upper()}...</div>
                
                <div class="paginas-3d"></div>
                
                <div class="lombada-3d" style="background: {cor_atual}; width: {largura_lombada_px}px;">
                    <div class="mini-etiqueta-lombada">
                        {linhas_lombada}
                    </div>
                </div>
            </div>
            """
            
        html_estante += "</div></div>"
        st.markdown(html_estante, unsafe_allow_html=True)
        st.caption("💡 Dica: Passe o mouse (ou toque) em cima de um livro para destacá-lo na prateleira!")
