import streamlit as st
import pandas as pd

# Configuração da página para usar o espaço máximo disponível
st.set_page_config(layout="wide", page_title="BiblioKhan Smart", page_icon="📚")

# Estilos básicos para deixar os cartões brancos e organizados
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
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO STATE ---
if "tela" not in st.session_state: st.session_state.tela = "entrada"
if "livros" not in st.session_state: st.session_state.livros = []
if "livro_ativo" not in st.session_state: st.session_state.livro_ativo = 0
if "mensagem_sucesso" not in st.session_state: st.session_state.mensagem_sucesso = ""

# Dicionário para guardar os campos extras criados por você
if "campos_extras" not in st.session_state:
    st.session_state.campos_extras = {
        "Cutter": {"ativo": True},
        "Coleção": {"ativo": False}
    }

# Ordem de exibição das linhas na etiqueta
if "ordem_linhas" not in st.session_state:
    st.session_state.ordem_linhas = ["Classificação", "Cutter", "Edição", "Exemplar", "Coleção"]

# Controles de visibilidade dos campos padrões
if "ver_cdd" not in st.session_state: st.session_state.ver_cdd = True
if "ver_ed" not in st.session_state: st.session_state.ver_ed = True
if "ver_ex" not in st.session_state: st.session_state.ver_ex = True

# ==========================================================
# TELA PRINCIPAL: ENTRADA DE DADOS
# ==========================================================
if st.session_state.tela == "entrada":
    
    # Cabeçalho Simples
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 20px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
            <div style="font-size: 18px; font-weight: bold; color: #1e3a8a;">📚 BIBLIOKHAN SMART</div>
            <div style="font-size: 12px; color: #64748b; font-weight: 500;">Modo: Administrador ⚙️</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.mensagem_sucesso:
        st.success(st.session_state.mensagem_sucesso)
        st.session_state.mensagem_sucesso = ""

    # Criando duas colunas mestras na proporção perfeita para tablets
    col_dados, col_controle = st.columns([1.1, 0.9], gap="large")
    
    # ------------------------------------------------------
    # COLUNA DA ESQUERDA: FORMULÁRIO OU FILE UPLOADER
    # ------------------------------------------------------
    with col_dados:
        # Sistema de abas para alternar entre cadastro manual e upload sem afetar o preview lateral
        aba_manual, aba_upload = st.tabs(["📝 Cadastro Manual", "📥 Upload de Arquivos (CSV/Excel)"])
        
        with aba_manual:
            st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
            st.markdown("### 📝 Propriedades do Livro")
            
            titulo_input = st.text_input("Título do Livro *", placeholder="Ex: O Senhor dos Anéis")
            cdd_input = st.text_input("Classificação (CDD/CDU) *", placeholder="Ex: 823.91")
            
            c1, c2 = st.columns(2)
            paginas_input = c1.number_input("Páginas", min_value=1, value=100)
            dimensao_input = c2.text_input("Dimensão", placeholder="Ex: 23 cm")
            
            c3, c4 = st.columns(2)
            edicao_input = c3.text_input("Edição", value="1.ed.")
            exemplar_input = c4.text_input("Exemplar", value="Ex.1")
            
            # Coleta os valores digitados nos campos extras dinâmicos ativos
            valores_extras = {}
            for nome_campo, info in st.session_state.campos_extras.items():
                if info["ativo"]:
                    valores_extras[nome_campo] = st.text_input(f"{nome_campo}", placeholder=f"Digite o valor de {nome_campo.lower()}")
                else:
                    valores_extras[nome_campo] = ""
                    
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SUB-BLOCO: ADICIONAR NOVOS CAMPOS EXTRAS
            st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
            st.markdown("### ➕ Adicionar Opção de Mais Campos")
            
            c_novo_nome, c_novo_btn = st.columns([1.3, 0.7])
            novo_campo = c_novo_nome.text_input("Nome do novo campo:", placeholder="Ex: Volume, ISBN, Editora...", label_visibility="collapsed")
            
            if c_novo_btn.button("Criar Campo", use_container_width=True):
                nome_limpo = novo_campo.strip()
                if nome_limpo and nome_limpo not in st.session_state.campos_extras:
                    st.session_state.campos_extras[nome_limpo] = {"ativo": True}
                    st.session_state.ordem_linhas.append(nome_limpo)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with aba_upload:
            st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
            st.markdown("### 📥 Importação em Lote")
            st.info("O arquivo deve conter pelo menos as colunas **titulo** e **cdd**.")
            
            arquivo_carregado = st.file_uploader("Selecione um arquivo CSV ou Excel", type=["csv", "xlsx"])
            
            if arquivo_carregado is not None:
                try:
                    # Carrega dependendo da extensão
                    if arquivo_carregado.name.endswith('.csv'):
                        df = pd.read_csv(arquivo_carregado)
                    else:
                        df = pd.read_excel(arquivo_carregado)
                    
                    # Padroniza as colunas em minúsculo para evitar conflitos de sintaxe
                    df.columns = df.columns.str.lower()
                    
                    if 'titulo' in df.columns and 'cdd' in df.columns:
                        st.write("📊 **Prévia dos dados identificados:**")
                        st.dataframe(df[['titulo', 'cdd']].head(5), use_container_width=True)
                        
                        if st.button("Confirmar Importação de Livros", type="primary", use_container_width=True):
                            contador = 0
                            for _, linha in df.iterrows():
                                titulo_lote = str(linha['titulo']).strip()
                                cdd_lote = str(linha['cdd']).strip()
                                
                                if titulo_lote and cdd_lote and titulo_lote != "nan" and cdd_lote != "nan":
                                    paginas_lote = int(linha['paginas']) if 'paginas' in df.columns and pd.notna(linha['paginas']) else 100
                                    calc_lombada = (paginas_lote / 2) * 0.1 + 2.0
                                    
                                    novo_livro = {
                                        "titulo": titulo_lote,
                                        "cdd": cdd_lote,
                                        "paginas": str(paginas_lote),
                                        "dimensao": str(linha['dimensao']).strip() if 'dimensao' in df.columns and pd.notna(linha['dimensao']) else "",
                                        "ed": str(linha['edicao']).strip() if 'edicao' in df.columns and pd.notna(linha['edicao']) else "1.ed.",
                                        "ex": str(linha['exemplar']).strip() if 'exemplar' in df.columns and pd.notna(linha['exemplar']) else "Ex.1",
                                        "ajuste": min(calc_lombada, 50.0)
                                    }
                                    
                                    # Mapeia colunas extras se baterem com o nome dos criados no sistema
                                    for extra in st.session_state.campos_extras.keys():
                                        extra_lower = extra.lower()
                                        if extra_lower in df.columns and pd.notna(linha[extra_lower]):
                                            novo_livro[extra] = str(linha[extra_lower]).strip()
                                        else:
                                            novo_livro[extra] = ""
                                            
                                    st.session_state.livros.append(novo_livro)
                                    contador += 1
                                    
                            st.session_state.mensagem_sucesso = f"🎉 Sucesso! {contador} livros foram adicionados via arquivo à fila!"
                            st.rerun()
                    else:
                        st.error("Erro estrutural: Certifique-se de que sua tabela possui as colunas 'titulo' e 'cdd'.")
                except Exception as e:
                    st.error(f"Não foi possível processar o arquivo: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # COLUNA DA DIREITA: PREVIEW E CONTROLES DE LAYOUT
    # ------------------------------------------------------
    with col_controle:
        st.markdown('<div class="bloco-branco" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight: bold; margin-top: 0; color: #475569;'>👁️ PRÉ-VISUALIZAÇÃO EM TEMPO REAL</p>", unsafe_allow_html=True)
        
        # Garante que variáveis existam mesmo se o usuário estiver olhando a aba de upload
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
        
        html_etiqueta = f"""
        <div style="font-size: {tam_fonte}; font-weight: bold; border-bottom: 1px solid #cbd5e1; margin-bottom: 6px; padding-bottom: 2px; width: 100%; word-wrap: break-word; line-height: 1.1;">
            {t_preview.upper() if t_preview else "TÍTULO DO LIVRO"}
        </div>
        """
        
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
                <div style="width: 130px; min-height: 145px; background: white; color: black; border: 2px solid #64748b; font-family: 'Courier New', monospace; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); border-radius: 4px;">
                    {html_etiqueta}
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SUB-BLOCO: CONFIGURAÇÕES DE EXIBIÇÃO
        st.markdown('<div class="bloco-branco">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Ativar/Desativar Linhas")
        
        st.session_state.ver_cdd = st.checkbox("Exibir Classificação (CDD)", value=st.session_state.ver_cdd)
        st.session_state.ver_ed = st.checkbox("Exibir Edição", value=st.session_state.ver_ed)
        st.session_state.ver_ex = st.checkbox("Exibir Exemplar", value=st.session_state.ver_ex)
        
        for nome_campo in list(st.session_state.campos_extras.keys()):
            is_ativo = st.checkbox(f"Exibir {nome_campo}", value=st.session_state.campos_extras[nome_campo]["ativo"], key=f"chk_{nome_campo}")
            st.session_state.campos_extras[nome_campo]["ativo"] = is_ativo
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # BASE DA TELA: BOTÕES DE SALVAMENTO
    # ------------------------------------------------------
    st.markdown("---")
    c_salvar, c_fila_info = st.columns([1.5, 0.5])
    
    with c_salvar:
        if st.button("📥 Adicionar Este Livro Manual e Gerar Etiqueta", type="primary", use_container_width=True):
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
                st.session_state.mensagem_sucesso = f"✔️ Livro '{titulo_input.strip()}' foi para a fila com sucesso!"
                st.rerun()
            else:
                st.error("Por favor, preencha os dados manuais na aba ao lado antes de salvar!")
                
    with c_fila_info:
        if st.button(f"📋 Ver Estante (Fila: {len(st.session_state.livros)}) ➡️", use_container_width=True):
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
