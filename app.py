import streamlit as st
import pandas as pd

# Configuração da página para usar o espaço máximo disponível
st.set_page_config(layout="wide", page_title="BiblioKhan Smart", page_icon="📚")

# ==========================================================
# ESTILOS E ANIMAÇÃO DO LIVRO 3D
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
        
        /* CONTAINER DO LIVRO 3D */
        .cena-3d {
            width: 100%;
            height: 220px;
            perspective: 600px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 15px;
            background: #f1f5f9;
            border-radius: 8px;
            padding: 10px;
        }
        .livro-3d {
            width: 100px;
            height: 150px;
            position: relative;
            transform-style: preserve-3d;
            transform: rotateX(20deg) rotateY(-30deg);
            transition: transform 0.5s;
        }
        .capa-livro {
            position: absolute;
            width: 100px;
            height: 150px;
            background: #3b82f6;
            border-radius: 2px 6px 6px 2px;
            box-shadow: inset 4px 0 10px rgba(0,0,0,0.2);
            transform: translateZ(var(--lombada-metade));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 10px;
            text-align: center;
            padding: 5px;
        }
        .lombada-livro {
            position: absolute;
            height: 150px;
            background: #2563eb;
            transform: rotateY(-90deg) translateZ(50px);
            width: var(--lombada-largura);
            left: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            font-family: monospace;
            font-size: 8px;
            box-shadow: inset -3px 0 8px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .paginas-livro {
            position: absolute;
            height: 146px;
            background: #f8fafc;
            width: var(--lombada-largura);
            transform: rotateY(90deg) translateZ(50px);
            right: 0;
            top: 2px;
            box-shadow: inset 0 0 5px #cbd5e1;
            background-image: linear-gradient(90deg, #e2e8f0 1px, transparent 1px);
            background-size: 3px 100%;
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
    # COLUNA DA ESQUERDA: ENTRADA MANUAL E LOTE
    # ------------------------------------------------------
    with col_dados:
        aba_manual, aba_upload = st.tabs(["📝 Cadastro Manual", "📥 Upload de Arquivos (CSV/Excel)"])
        
        with aba_manual:
            st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
            st.markdown("### 📝 Propriedades do Livro")
            
            titulo_input = st.text_input("Título do Livro *", placeholder="Ex: O Senhor dos Anéis", key="manual_titulo")
            cdd_input = st.text_input("Classificação (CDD/CDU) *", placeholder="Ex: 823.91", key="manual_cdd")
            
            c1, c2 = st.columns(2)
            paginas_input = c1.number_input("Páginas", min_value=1, value=100, key="manual_paginas")
            dimensao_input = c2.text_input("Dimensão", placeholder="Ex: 23 cm", key="manual_dimensao")
            
            c3, c4 = st.columns(2)
            edicao_input = c3.text_input("Edição", value="1.ed.", key="manual_ed")
            exemplar_input = c4.text_input("Exemplar", value="Ex.1", key="manual_ex")
            
            # --- CORREÇÃO: Renderiza as caixas de texto de TODOS os campos extras ativos aqui ---
            valores_extras = {}
            for nome_campo, info in st.session_state.campos_extras.items():
                if info["ativo"]:
                    valores_extras[nome_campo] = st.text_input(f"{nome_campo}", placeholder=f"Digite o valor de {nome_campo.lower()}", key=f"input_extra_{nome_campo}")
                else:
                    valores_extras[nome_campo] = ""
                    
            st.markdown('</div>', unsafe_allow_html=True)
            
            # CRIADOR DE CAMPOS EXTRAS
            st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
            st.markdown("### ➕ Adicionar Opção de Mais Campos")
            c_novo_nome, c_novo_btn = st.columns([1.3, 0.7])
            novo_campo = c_novo_nome.text_input("Nome do novo campo:", placeholder="Ex: Volume, ISBN, Editora...", label_visibility="collapsed", key="add_novo_campo")
            
            if c_novo_btn.button("Criar Campo", use_container_width=True, key="btn_criar_campo"):
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
            arquivo_carregado = st.file_uploader("Selecione um arquivo CSV ou Excel", type=["csv", "xlsx"], key="uploader_lote")
            
            if arquivo_carregado is not None:
                try:
                    df = pd.read_csv(arquivo_carregado) if arquivo_carregado.name.endswith('.csv') else pd.read_excel(arquivo_carregado)
                    df.columns = df.columns.str.lower()
                    
                    if 'titulo' in df.columns and 'cdd' in df.columns:
                        st.dataframe(df[['titulo', 'cdd']].head(3), use_container_width=True)
                        if st.button("Confirmar Importação", type="primary", use_container_width=True, key="btn_confirma_lote"):
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
                            st.session_state.mensagem_sucesso = f"🎉 Importados {contador} livros com sucesso!"
                            st.rerun()
                    else:
                        st.error("O arquivo precisa ter as colunas 'titulo' and 'cdd'!")
                except Exception as e:
                    st.error(f"Erro: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # COLUNA DA DIREITA: PREVIEW DA ETIQUETA & LIVRO 3D
    # ------------------------------------------------------
    with col_controle:
        st.markdown('<div class="bloco-branco" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight: bold; margin-top: 0; color: #475569;'>👁️ PREVIEW EM TEMPO REAL</p>", unsafe_allow_html=True)
        
        t_preview = titulo_input if 'titulo_input' in locals() else ""
        c_preview = cdd_input if 'cdd_input' in locals() else ""
        e_preview = edicao_input if 'edicao_input' in locals() else "1.ed."
        ex_preview = exemplar_input if 'exemplar_input' in locals() else "Ex.1"
        ext_preview = valores_extras if 'valores_extras' in locals() else {}

        dados_etiqueta = {
            "Classificação": c_preview if c_preview else "---",
            "Edição": e_preview if e_preview else "---",
            "Exemplar": ex_preview if ex_preview else "---"
        }
        dados_etiqueta.update(ext_preview)
        
        tam_fonte = "11px" if len(t_preview) < 20 else "9px"
        html_etiqueta = f'<div style="font-size: {tam_fonte}; font-weight: bold; border-bottom: 1px solid #cbd5e1; margin-bottom: 4px; padding-bottom: 2px; width: 100%; word-wrap: break-word;">{t_preview.upper() if t_preview else "TÍTULO"}</div>'
        
        # Monta as linhas conforme configuração de exibição
        for tag in st.session_state.ordem_linhas:
            if tag in dados_etiqueta:
                if tag == "Classificação" and st.session_state.ver_cdd:
                    html_etiqueta += f'<div style="font-weight: bold; font-size: 13px;">{dados_etiqueta[tag]}</div>'
                elif tag in st.session_state.campos_extras and st.session_state.campos_extras[tag]["ativo"]:
                    html_etiqueta += f'<div style="font-weight: bold; font-size: 12px; color: #1e40af;">{dados_etiqueta[tag] if dados_etiqueta[tag] else "---"}</div>'
                elif tag == "Edição" and st.session_state.ver_ed:
                    html_etiqueta += f'<div style="font-size: 11px;">{dados_etiqueta[tag]}</div>'
                elif tag == "Exemplar" and st.session_state.ver_ex:
                    html_etiqueta += f'<div style="font-size: 11px;">{dados_etiqueta[tag]}</div>'

        # Render plano do Selo Adesivo
        st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                <div style="width: 125px; min-height: 135px; background: white; color: black; border: 2px solid #64748b; font-family: monospace; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    {html_etiqueta}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- SEGUNDAMENTE: SISTEMA DE VISUALIZAÇÃO 3D DO LIVRO ---
        st.markdown('<div class="bloco-branco" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight: bold; margin-top: 0; color: #475569;'>📖 VISUALIZAÇÃO 3D DO LIVRO</p>", unsafe_allow_html=True)
        
        # Calcula espessura dinâmica baseada na quantidade de páginas informada
        paginas_num = paginas_input if 'paginas_input' in locals() else 100
        largura_lombada_px = min(max(int(paginas_num * 0.15), 15), 65)
        metade_lombada_px = largura_lombada_px // 2
        
        html_lombada_etiqueta = f"<b>{c_preview}</b><br>{ext_preview.get('Cutter', '')}"
        
        st.markdown(f"""
            <div class="cena-3d">
                <div class="livro-3d" style="--lombada-largura: {largura_lombada_px}px; --lombada-metade: {metade_lombada_px}px;">
                    <div class="capa-livro">{t_preview[:15].upper() if t_preview else "LIVRO"}</div>
                    <div class="lombada-livro" style="width: {largura_lombada_px}px; transform: rotateY(-90deg) translateZ({metade_lombada_px}px);">
                        <div style="background: white; color: black; padding: 2px; width: 85%; font-size: 7px; text-align: center; border-radius: 1px;">
                            {html_lombada_etiqueta}
                        </div>
                    </div>
                    <div class="paginas-livro" style="width: {largura_lombada_px}px; transform: rotateY(90deg) translateZ({100 - metade_lombada_px}px);"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # SELETOR DE CONFIGURAÇÃO DE LINHAS
        st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Ativar/Desativar Linhas")
        st.session_state.ver_cdd = st.checkbox("Exibir Classificação (CDD)", value=st.session_state.ver_cdd)
        st.session_state.ver_ed = st.checkbox("Exibir Edição", value=st.session_state.ver_ed)
        st.session_state.ver_ex = st.checkbox("Exibir Exemplar", value=st.session_state.ver_ex)
        for nome_campo in list(st.session_state.campos_extras.keys()):
            st.session_state.campos_extras[nome_campo]["ativo"] = st.checkbox(f"Exibir {nome_campo}", value=st.session_state.campos_extras[nome_campo]["ativo"], key=f"chk_{nome_campo}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # BARRA FINAL DE COMPACTAÇÃO
    # ------------------------------------------------------
    st.markdown("---")
    c_salvar, c_fila_info = st.columns([1.5, 0.5])
    
    with c_salvar:
        if st.button("📥 Adicionar Este Livro Manual e Gerar Etiqueta", type="primary", use_container_width=True, key="btn_salvar_manual"):
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
                st.session_state.mensagem_sucesso = f"✔️ Livro '{titulo_input.strip()}' adicionado!"
                st.rerun()
            else:
                st.error("Preencha o Título e a Classificação na aba de Cadastro Manual!")
                
    with c_fila_info:
        if st.button(f"📋 Ver Estante (Fila: {len(st.session_state.livros)}) ➡️", use_container_width=True, key="btn_mudar_estante"):
            st.session_state.tela = "calibragem"
            st.rerun()

# ==========================================================
# TELA DE CALIBRAGEM
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.markdown("### 📚 Estante de Calibragem Física")
    if st.button("⬅️ Voltar para o Cadastro"):
        st.session_state.tela = "entrada"
        st.rerun()
        
    if not st.session_state.livros:
        st.warning("Nenhum livro cadastrado na fila de impressão.")
    else:
        html_estante = "<div style='display: flex; align-items: flex-end; border-bottom: 15px solid #5D4037; padding: 15px; gap: 10px; background: #f1f5f9; overflow-x: auto;'>"
        for l in st.session_state.livros:
            largura = max(l.get('ajuste', 15.0) * 3, 75)
            html_estante += f"""
            <div style="flex: 0 0 {largura}px; width: {largura}px; height: 160px; background: #3b82f6; color: white; display: flex; flex-direction: column; justify-content: space-between; padding: 5px; text-align: center; border-radius: 2px 2px 0 0; box-shadow: inset -2px 0 5px rgba(0,0,0,0.1);">
                <div style="font-size: 9px; font-weight: bold; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{l['titulo']}</div>
                <div style="background: white; color: black; font-size: 9px; font-family: monospace; padding: 2px; border-radius: 1px;">
                    <div><b>{l['cdd']}</b></div>
                </div>
            </div>
            """
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)
