import streamlit as st
import pandas as pd

# Configuração de página com layout amplo
st.set_page_config(layout="wide", page_title="BiblioKhan Pro", page_icon="📚")

# ==========================================================
# INJEÇÃO DE INFORMAÇÕES VISUAIS PREMIUM (CSS)
# ==========================================================
st.markdown("""
    <style>
        .stApp {
            background-color: #f8fafc;
        }
        .custom-card {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }
        .card-title {
            color: #1e293b;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO STATE ---
if "tela" not in st.session_state: st.session_state.tela = "entrada"
if "livros" not in st.session_state: st.session_state.livros = []
if "livro_ativo" not in st.session_state: st.session_state.livro_ativo = 0
if "mostrar_3d" not in st.session_state: st.session_state.mostrar_3d = False
if "mensagem_sucesso" not in st.session_state: st.session_state.mensagem_sucesso = ""

# Dicionário dinâmico para os campos extras personalizados criados pelo usuário
if "campos_extras_dinamicos" not in st.session_state:
    st.session_state.campos_extras_dinamicos = {
        "Cutter": {"ativo": True, "valor": ""},
        "Coleção": {"ativo": False, "valor": ""}
    }

# Ordem base das linhas na etiqueta
if "cfg_ordem_linhas" not in st.session_state:
    st.session_state.cfg_ordem_linhas = ["Classificação", "Cutter", "Edição", "Exemplar", "Coleção"]

# Configurações de exibição fixas
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
        <div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 24px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 25px;">
            <div style="font-size: 20px; font-weight: bold; color: #1e3a8a;">📚 BIBLIOKHAN SMART</div>
            <div style="font-size: 14px; color: #64748b; font-weight: 500;">Modo: Administrador do Acervo ⚙️</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Gerenciar e Calibrar Etiquetas de Livros")
    
    if st.session_state.mensagem_sucesso:
        st.success(st.session_state.mensagem_sucesso)
        st.session_state.mensagem_sucesso = ""

    # Distribuição da tela: Formulários/Preview (Esquerda) e Fila (Direita)
    col_esquerda, col_direita = st.columns([1.7, 0.6], gap="medium")
    
    with col_esquerda:
        aba_manual, aba_lote = st.tabs(["📝 Cadastro Manual & Configurações", "📥 Importação em Lote"])
        
        with aba_manual:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            
            # AQUI ESTÁ O SEGREDO: Colunas lado a lado reais para o Form (60%) e para o Preview (40%)
            col_form, col_preview = st.columns([1.2, 0.8], gap="large")
            
            with col_form:
                st.markdown('### Propriedades do Livro')
                titulo_input = st.text_input("Título do Livro *", placeholder="Ex: O Senhor dos Anéis")
                cdd_input = st.text_input("Classificação (CDD/CDU) *", placeholder="Ex: 823.91")
                
                c1, c2 = st.columns(2)
                paginas_input = c1.number_input("Páginas", min_value=1, value=100)
                dimensao_input = c2.text_input("Dimensão do Livro", placeholder="Ex: 23 cm")
                
                c3, c4 = st.columns(2)
                edicao_input = c3.text_input("Edição", value="1.ed.")
                exemplar_input = c4.text_input("Exemplar", value="Ex.1")
                
                # Renderiza os campos extras que estão marcados como ativos
                valores_extras = {}
                for nome_campo, info in st.session_state.campos_extras_dinamicos.items():
                    if info["ativo"]:
                        valores_extras[nome_campo] = st.text_input(nome_campo, placeholder=f"Digite o(a) {nome_campo.lower()}")
                    else:
                        valores_extras[nome_campo] = ""

                st.markdown("---")
                # SEÇÃO PARA ADICIONAR NOVOS CAMPOS EXTRAS
                st.markdown('### ➕ Gerenciar Campos Extras')
                novo_nome_campo = st.text_input("Nome do novo campo extra:", placeholder="Ex: Volume, Editora, ISBN...", key="input_novo_campo")
                
                if st.button("Criar Novo Campo", use_container_width=True):
                    nome_limpo = novo_nome_campo.strip()
                    if nome_limpo and nome_limpo not in st.session_state.campos_extras_dinamicos:
                        # Adiciona no dicionário de estados ativos
                        st.session_state.campos_extras_dinamicos[nome_limpo] = {"ativo": True, "valor": ""}
                        # Adiciona no fim da lista de ordem de exibição
                        st.session_state.cfg_ordem_linhas.append(nome_limpo)
                        st.success(f"Campo '{nome_limpo}' adicionado!")
                        st.rerun()
                    elif nome_limpo in st.session_state.campos_extras_dinamicos:
                        # Se já existia mas estava desativado, reativa
                        st.session_state.campos_extras_dinamicos[nome_limpo]["ativo"] = True
                        st.rerun()

            with col_preview:
                st.markdown('### Configuração & Preview (Lado a Lado)')
                
                st.session_state.cfg_exibir_cdd = st.checkbox("Exibir Classificação", value=st.session_state.cfg_exibir_cdd)
                st.session_state.cfg_exibir_ed = st.checkbox("Exibir Edição", value=st.session_state.cfg_exibir_ed)
                st.session_state.cfg_exibir_ex = st.checkbox("Exibir Exemplar", value=st.session_state.cfg_exibir_ex)
                
                # Checkboxes dinâmicos para ativar/desativar os campos criados pelo usuário
                for nome_campo in list(st.session_state.campos_extras_dinamicos.keys()):
                    is_ativo = st.checkbox(f"Ativar {nome_campo}", value=st.session_state.campos_extras_dinamicos[nome_campo]["ativo"], key=f"chk_{nome_campo}")
                    st.session_state.campos_extras_dinamicos[nome_campo]["ativo"] = is_ativo

                # Mapeia quais itens devem realmente ir para a ordenação visual
                nomes_mapeados = {
                    "Classificação": "Classificação" if st.session_state.cfg_exibir_cdd else None,
                    "Edição": "Edição" if st.session_state.cfg_exibir_ed else None,
                    "Exemplar": "Exemplar" if st.session_state.cfg_exibir_ex else None,
                }
                # Adiciona os extras criados à lista de verificação se estiverem ativos
                for nome_campo, info in st.session_state.campos_extras_dinamicos.items():
                    if info["ativo"]:
                        nomes_mapeados[nome_campo] = nome_campo

                itens_ativos = [k for k, v in nomes_mapeados.items() if v is not None]
                
                # Reconstrói a lista de reordenação
                nova_ordem_vistas = []
                if itens_ativos:
                    st.markdown("**Ordem das Linhas:**")
                    for rank in range(len(itens_ativos)):
                        opcoes_disponiveis = [x for x in itens_ativos if x not in nova_ordem_vistas]
                        
                        default_idx = 0
                        if rank < len(st.session_state.cfg_ordem_linhas) and st.session_state.cfg_ordem_linhas[rank] in opcoes_disponiveis:
                            default_idx = opcoes_disponiveis.index(st.session_state.cfg_ordem_linhas[rank])
                        
                        escolha = st.selectbox(f"Linha {rank+1}:", opcoes_disponiveis, index=default_idx, key=f"sel_ordem_{rank}", label_visibility="collapsed")
                        nova_ordem_vistas.append(escolha)
                    st.session_state.cfg_ordem_linhas = nova_ordem_vistas

                # --- CONTAINER DA PRÉ-VISUALIZAÇÃO EM TEMPO REAL ---
                st.markdown("<div style='font-weight: 600; font-size:13px; color:#475569; margin-top:15px;'>Visualização Impressa Estabilizada:</div>", unsafe_allow_html=True)
                
                dados_etiqueta = {
                    "Classificação": cdd_input if cdd_input else "---",
                    "Edição": edicao_input if edicao_input else "---",
                    "Exemplar": exemplar_input if exemplar_input else "---"
                }
                # Mescla os valores dos campos extras coletados no form
                dados_etiqueta.update(valores_extras)
                
                tamanho_fonte_titulo = "11px" if len(titulo_input) < 20 else ("9px" if len(titulo_input) < 40 else "8px")
                html_preview = f'<div style="font-size: {tamanho_fonte_titulo}; font-weight: bold; border-bottom: 1px solid #cbd5e1; margin-bottom: 4px; padding-bottom: 2px; width: 100%; word-wrap: break-word; line-height: 1.1;">{titulo_input.upper() if titulo_input else "TÍTULO DO LIVRO"}</div>'
                
                for tag in st.session_state.cfg_ordem_linhas:
                    if tag in dados_etiqueta:
                        estilo_linha = "font-weight: bold; font-size: 13px;" if tag in ["Classificação"] or tag in st.session_state.campos_extras_dinamicos else "font-size: 11px;"
                        html_preview += f'<div style="{estilo_linha}">{dados_etiqueta[tag] if dados_etiqueta[tag] else "---"}</div>'
                    
                st.markdown(f"""
                    <div style="display: flex; background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; justify-content: center;">
                        <div style="width: 130px; min-height: 145px; background: white; color: black; border: 1px solid #94a3b8; font-family: 'Courier New', monospace; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            {html_preview}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Botão de Salvar estendido na base do Card
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Criar e Adicionar Etiqueta à Fila", type="primary", use_container_width=True):
                if titulo_input.strip() and cdd_input.strip():
                    ajuste = (paginas_input / 2) * 0.1 + 2.0
                    
                    # Salva o registro completo incluindo os dados extras correspondentes
                    novo_livro = {
                        "titulo": titulo_input.strip(), "cdd": cdd_input.strip(), "paginas": str(paginas_input),
                        "dimensao": dimensao_input.strip(), "ed": edicao_input.strip(), "ex": exemplar_input.strip(),
                        "ajuste": min(ajuste, 50.0)
                    }
                    for k, v in valores_extras.items():
                        novo_livro[k] = v.strip() if v else ""
                        
                    st.session_state.livros.append(novo_livro)
                    st.session_state.mensagem_sucesso = f"🎉 '{titulo_input.strip()}' inserido com sucesso!"
                    st.rerun()
                else:
                    st.error("Campos com * são obrigatórios!")
                    
            st.markdown('</div>', unsafe_allow_html=True)

        with aba_lote:
            st.markdown('<div class="custom-card"><div class="card-title">Processamento em Lote</div>', unsafe_allow_html=True)
            file = st.file_uploader("Upload CSV ou Excel", type=["csv", "xlsx"])
            if file:
                try:
                    df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
                    df.columns = df.columns.str.lower()
                    for _, row in df.iterrows():
                        st.session_state.livros.append({
                            "titulo": str(row.get('titulo', 'Sem título')), "cdd": str(row.get('cdd', '')),
                            "paginas": "100", "dimensao": "", "ed": "1.ed.", "ex": "Ex.1", "ajuste": 15.0
                        })
                    st.session_state.mensagem_sucesso = f"📊 {len(df)} livros importados!"
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao processar lote: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

    with col_direita:
        st.markdown('<div class="custom-card"><div class="card-title">📋 Fila</div>', unsafe_allow_html=True)
        st.metric(label="Livros na Fila", value=len(st.session_state.livros))
        if st.button("Ver Estante Virtual ➡️", type="primary", use_container_width=True):
            mudar_tela("calibragem")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM (Física e 3D)
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.markdown('<div class="custom-card"><h3>📚 Estante de Calibragem & Modelagem 3D</h3></div>', unsafe_allow_html=True)
    if st.button("⬅️ Voltar"):
        st.session_state.mostrar_3d = False
        mudar_tela("entrada")
        st.rerun()
        
    if not st.session_state.livros:
        st.warning("Nenhum livro na fila.")
    else:
        # Renderizador da Estante Física
        html_estante = "<div style='display: flex; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 15px; background: #f1f5f9; overflow-x: auto;'>"
        for i, libro in enumerate(st.session_state.livros):
            largura = max(libro.get('ajuste', 15.0) * 4, 85)
            borda = "outline: 3px solid #3b82f6;" if (st.session_state.mostrar_3d and st.session_state.livro_ativo == i) else ""
            
            html_estante += f"""
            <div style="flex: 0 0 {largura}px; width: {largura}px; height: 200px; background: #3b82f6; color: white; display: flex; flex-direction: column; justify-content: space-between; padding: 5px; text-align: center; {borda}">
                <div style="font-size: 10px; font-weight: bold;">{libro['titulo'][:12]}</div>
                <div style="background: white; color: black; font-size: 10px; font-family: monospace; padding: 2px;">
                    <div><b>{libro['cdd']}</b></div>
                    <div>{libro.get('Cutter', '')}</div>
                </div>
            </div>
            """
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)
        
        # Painel Inferior de ajuste fino do livro ativo
        st.markdown("<br>", unsafe_allow_html=True)
        opcoes_livros = [f"{idx} - {l['titulo']}" for idx, l in enumerate(st.session_state.livros)]
        escolha_livro = st.selectbox("Selecione um livro para ajustar a lombada:", opcoes_livros)
        idx_sel = int(escolha_livro.split(" - ")[0])
        st.session_state.livro_ativo = idx_sel
        st.session_state.mostrar_3d = True
        
        c_ajuste, c_render = st.columns(2)
        livro_foco = st.session_state.livros[idx_sel]
        
        with c_ajuste:
            novo_ajuste = st.slider("Espessura da Lombada (mm)", 1.0, 50.0, float(livro_foco['ajuste']))
            st.session_state.livros[idx_sel]['ajuste'] = novo_ajuste
            if st.button("Remover Livro", use_container_width=True):
                st.session_state.livros.pop(idx_sel)
                st.session_state.mostrar_3d = False
                st.rerun()
                
        with c_render:
            esp_3d = max(livro_foco['ajuste'] * 6, 60)
            st.markdown(f"""
            <div style="perspective: 1000px; display: flex; justify-content: center; height: 220px;">
                <div style="width: {esp_3d}px; height: 200px; background: #3b82f6; border: 3px solid #1e3a8a; transform: rotateY(-20deg); display: flex; flex-direction: column; justify-content: flex-end; box-shadow: -5px 5px 15px rgba(0,0,0,0.3);">
                    <div style="background: white; color: black; font-family: monospace; font-size: 11px; padding: 5px; text-align: center;">
                        <div style="font-weight: bold; border-bottom: 1px solid #ccc; margin-bottom: 2px;">{livro_foco['titulo'][:15].upper()}</div>
                        <div><b>{livro_foco['cdd']}</b></div>
                        <div>{livro_foco.get('Cutter', '')}</div>
                    </div>
                </div>
                <div style="width: 100px; height: 200px; background: #cbd5e1; transform: rotateY(30deg); transform-origin: left; display: flex; align-items: center; justify-content: center; color: #475569; font-weight: bold;">CAPA</div>
            </div>
            """, unsafe_allow_html=True)
        
