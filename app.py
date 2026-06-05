import streamlit as st
import pandas as pd

# Configuração de página com layout amplo
st.set_page_config(layout="wide", page_title="BiblioKhan Pro", page_icon="📚")

# ==========================================================
# INJEÇÃO DE INFORMAÇÕES VISUAIS PREMIUM (CSS)
# ==========================================================
st.markdown("""
    <style>
        /* Fundo geral da aplicação mais suave */
        .stApp {
            background-color: #f8fafc;
        }
        
        /* Estilização dos blocos principais (Cards) */
        .custom-card {
            background-color: #ffffff;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
        }
        
        /* Cabeçalhos internos dos Cards */
        .card-title {
            color: #1e293b;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Inputs customizados mais discretos */
        .stTextInput input, .stNumberInput input, .stSelectbox div {
            border-radius: 8px !important;
            border: 1px solid #cbd5e1 !important;
        }
        
        /* Área customizada simulando o Drag & Drop moderno */
        .upload-dropzone {
            border: 2px dashed #3b82f6;
            background-color: #eff6ff;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            color: #1e40af;
            font-weight: 500;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO ESTADO ---
if "tela" not in st.session_state: 
    st.session_state.tela = "entrada"
if "livros" not in st.session_state: 
    st.session_state.livros = []
if "livro_ativo" not in st.session_state: 
    st.session_state.livro_ativo = 0
if "mostrar_3d" not in st.session_state:
    st.session_state.mostrar_3d = False
if "mensagem_sucesso" not in st.session_state:
    st.session_state.mensagem_sucesso = ""

# --- CONFIGURAÇÕES DE EXIBIÇÃO E ORDEM PERMANENTE ---
if "cfg_exibir_cdd" not in st.session_state: st.session_state.cfg_exibir_cdd = True
if "cfg_exibir_ed" not in st.session_state: st.session_state.cfg_exibir_ed = True
if "cfg_exibir_ex" not in st.session_state: st.session_state.cfg_exibir_ex = True
if "cfg_usar_extra1" not in st.session_state: st.session_state.cfg_usar_extra1 = True
if "cfg_nome_extra1" not in st.session_state: st.session_state.cfg_nome_extra1 = "Cutter"
if "cfg_usar_extra2" not in st.session_state: st.session_state.cfg_usar_extra2 = False
if "cfg_nome_extra2" not in st.session_state: st.session_state.cfg_nome_extra2 = "Coleção"

if "cfg_ordem_linhas" not in st.session_state:
    st.session_state.cfg_ordem_linhas = ["Classificação", "Extra 1", "Edição", "Exemplar", "Extra 2"]

def mudar_tela(nova_tela):
    st.session_state.tela = nova_tela

# ==========================================================
# TELA 1: ENTRADA DE DADOS (ABAS + DESIGN PROFISSIONAL)
# ==========================================================
if st.session_state.tela == "entrada":
    
    # Barra de Navegação Superior
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 24px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 25px;">
            <div style="font-size: 20px; font-weight: bold; color: #1e3a8a; display: flex; align-items: center; gap: 8px;">
                📚 BIBLIOKHAN SMART
            </div>
            <div style="font-size: 14px; color: #64748b; font-weight: 500;">
                Modo: Administrador do Acervo ⚙️
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Gerenciar e Calibrar Etiquetas de Livros")
    
    if st.session_state.mensagem_sucesso:
        st.success(st.session_state.mensagem_sucesso)
        st.session_state.mensagem_sucesso = ""

    # Divisão em duas colunas mestras: Esquerda (Painel Operacional) e Direita (Fila de Processamento)
    col_esquerda, col_direita = st.columns([1.6, 0.7], gap="medium")
    
    with col_esquerda:
        # Duas abas limpas e focadas
        aba_manual, aba_lote = st.tabs([
            "📝 Cadastro Manual & Configurações", 
            "📥 Importação em Lote"
        ])
        
        # --- ABA 1: CADASTRO MANUAL ---
        with aba_manual:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            
            # INICIALIZAÇÃO DE SEGURANÇA (Evita o NameError independente da ordem das colunas)
            titulo = ""
            classificacao = ""
            edicao = "1.ed."
            exemplar = "Ex.1"
            val_extra1 = ""
            val_extra2 = ""
            paginas = 100
            dimensao = ""

            subcol_dados, subcol_layout = st.columns([1, 1], gap="large")
            
            # Subcoluna Esquerda: Cadastro de Dados Básicos do livro
            with subcol_dados:
                st.markdown('<div style="font-size:15px; font-weight:600; color:#1e293b; margin-bottom:12px;">Propriedades do Livro</div>', unsafe_allow_html=True)
                titulo = st.text_input("Título do Livro *", key="manual_titulo", placeholder="Ex: O Senhor dos Anéis")
                classificacao = st.text_input("Classificação (CDD/CDU) *", key="manual_cdd", placeholder="Ex: 823.91")
                
                c1, c2 = st.columns(2)
                paginas = c1.number_input("Páginas", min_value=1, value=100, key="manual_pags")
                dimensao = c2.text_input("Dimensão do Livro", placeholder="Ex: 23 cm", key="manual_dim")
                
                c3, c4 = st.columns(2)
                edicao = c3.text_input("Edição", value="1.ed.", key="manual_ed")
                exemplar = c4.text_input("Exemplar", value="Ex.1", key="manual_ex")
                
                if st.session_state.cfg_usar_extra1:
                    val_extra1 = st.text_input(f"{st.session_state.cfg_nome_extra1}", key="manual_extra1", placeholder="Ex: C891l")
                    
                if st.session_state.cfg_usar_extra2:
                    val_extra2 = st.text_input(f"{st.session_state.cfg_nome_extra2}", key="manual_extra2")
            
            # Subcoluna Direita: Gerenciamento do Layout dos Campos e Pré-visualização Instantânea
            with subcol_layout:
                st.markdown('<div style="font-size:15px; font-weight:600; color:#1e293b; margin-bottom:12px;">Configuração da Etiqueta</div>', unsafe_allow_html=True)
                
                # Checkboxes rápidos para ocultar/exibir
                st.session_state.cfg_exibir_cdd = st.checkbox("Exibir Classificação", value=st.session_state.cfg_exibir_cdd)
                st.session_state.cfg_usar_extra1 = st.checkbox("Ativar Campo Extra 1 (Cutter)", value=st.session_state.cfg_usar_extra1)
                st.session_state.cfg_exibir_ed = st.checkbox("Exibir Edição", value=st.session_state.cfg_exibir_ed)
                st.session_state.cfg_exibir_ex = st.checkbox("Exibir Exemplar", value=st.session_state.cfg_exibir_ex)
                st.session_state.cfg_usar_extra2 = st.checkbox("Ativar Campo Extra 2", value=st.session_state.cfg_usar_extra2)
                
                # Montagem dinâmica da ordem das linhas baseada nas escolhas ativas
                nomes_mapeados = {
                    "Classificação": "Classificação" if st.session_state.cfg_exibir_cdd else None,
                    "Extra 1": f"Extra 1 ({st.session_state.cfg_nome_extra1})" if st.session_state.cfg_usar_extra1 else None,
                    "Edição": "Edição" if st.session_state.cfg_exibir_ed else None,
                    "Exemplar": "Exemplar" if st.session_state.cfg_exibir_ex else None,
                    "Extra 2": f"Extra 2 ({st.session_state.cfg_nome_extra2})" if st.session_state.cfg_usar_extra2 else None,
                }
                itens_ativos = [k for k, v in nomes_mapeados.items() if v is not None]
                
                # Filtra e atualiza a ordem do estado
                ordem_filtrada = [x for x in st.session_state.cfg_ordem_linhas if x in itens_ativos]
                for item in itens_ativos:
                    if item not in ordem_filtrada: 
                        ordem_filtrada.append(item)
                st.session_state.cfg_ordem_linhas = ordem_filtrada

                # Renderização da Ordem das linhas (Apenas se houver itens ativos)
                if itens_ativos:
                    st.markdown("<div style='font-size:12px; font-weight:600; color:#475569; margin-top:8px;'>Ordem das Linhas:</div>", unsafe_allow_html=True)
                    nova_ordem = []
                    for rank in range(len(itens_ativos)):
                        opcoes_disponiveis = [x for x in itens_ativos if x not in nova_ordem]
                        default_idx = 0
                        if rank < len(st.session_state.cfg_ordem_linhas) and st.session_state.cfg_ordem_linhas[rank] in opcoes_disponiveis:
                            default_idx = opcoes_disponiveis.index(st.session_state.cfg_ordem_linhas[rank])
                        
                        escolha = st.selectbox(f"Linha {rank+1}", opcoes_disponiveis, index=default_idx, key=f"reorder_live_{rank}", label_visibility="collapsed")
                        nova_ordem.append(escolha)
                    st.session_state.cfg_ordem_linhas = nova_ordem

                # --- CONTAINER DA PRÉ-VISUALIZAÇÃO DA ETIQUETA ---
                st.markdown("<div style='font-weight: 600; font-size:13px; color:#475569; margin-top:14px;'>Pré-visualização em Tempo Real:</div>", unsafe_allow_html=True)
                dados_reais_digitados = {
                    "Classificação": classification if classification else "---",
                    "Extra 1": val_extra1 if val_extra1 else "---",
                    "Edição": edicao if edicao else "---",
                    "Exemplar": exemplar if exemplar else "---",
                    "Extra 2": val_extra2 if val_extra2 else "---"
                }
                
                tamanho_fonte_titulo = "11px" if len(titulo) < 20 else ("9px" if len(titulo) < 40 else "8px")
                html_preview_linhas = f'<div style="font-size: {tamanho_fonte_titulo}; font-weight: bold; border-bottom: 1px solid #cbd5e1; margin-bottom: 4px; padding-bottom: 2px; width: 100%; word-wrap: break-word; line-height: 1.1;">{titulo.upper() if titulo else "TÍTULO DO LIVRO"}</div>'
                
                for tag in st.session_state.cfg_ordem_linhas:
                    estilo_linha = "font-weight: bold; font-size: 13px;" if tag in ["Classificação", "Extra 1"] else "font-size: 11px;"
                    html_preview_linhas += f'<div style="{estilo_linha}">{dados_reais_digitados[tag]}</div>'
                    
                st.markdown(f"""
                    <div style="display: flex; background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; margin-top: 5px; justify-content: center;">
                        <div style="width: 125px; min-height: 135px; background: white; color: black; border: 1px solid #94a3b8; font-family: 'Courier New', monospace; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            {html_preview_linhas}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # Botão de ação que engloba a soma dos dois lados
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Criar e Adicionar Etiqueta ao Sistema", type="primary", use_container_width=True, key="btn_add_manual"):
                if titulo.strip() and classificacao.strip():
                    ajuste = (paginas / 2) * 0.1 + 2.0
                    novo_livro = {
                        "titulo": titulo.strip(), "cdd": classificacao.strip(), "paginas": str(paginas),
                        "dimensao": dimensao.strip(), "ed": edicao.strip(), "ex": exemplar.strip(),
                        "extra1": val_extra1.strip(), "extra2": val_extra2.strip(), "ajuste": min(ajuste, 50.0)
                    }
                    if not st.session_state.livros or st.session_state.livros[-1] != novo_livro:
                        st.session_state.livros.append(novo_livro)
                        st.session_state.mensagem_sucesso = f"🎉 Livro '{titulo.strip()}' adicionado com sucesso!"
                        st.rerun()
                else: 
                    st.error("Por favor, preencha obrigatoriamente os campos de Título e Classificação.")
                    
            st.markdown('</div>', unsafe_allow_html=True)

        # --- ABA 2: IMPORTAÇÃO EM LOTE ---
        with aba_lote:
            st.markdown('<div class="custom-card"><div class="card-title">Processamento em Lote</div>', unsafe_allow_html=True)
            st.markdown("""
                <div class="upload-dropzone">
                    <span style="font-size: 24px;">☁️</span><br>
                    Arraste o arquivo aqui ou clique para procurar
                    <div style="font-size: 11px; color: #64748b; font-weight: normal; margin-top:4px;">Formatos suportados: CSV, XLSX. Máximo de 10.000 registros</div>
                </div>
            """, unsafe_allow_html=True)
            
            file = st.file_uploader("Subir arquivo de acervo", type=["csv", "xlsx", "xls"], label_visibility="collapsed", key="uploader_lote")
            
            if file:
                try:
                    if file.name.endswith('.csv'): df = pd.read_csv(file)
                    else: df = pd.read_excel(file)
                    df.columns = df.columns.str.lower()
                    contador = 0
                    for _, row in df.iterrows():
                        pags = str(row.get('paginas', '100'))
                        try: qtd_pags = int(float(pags)) if pags.replace('.','',1).isdigit() else 100
                        except: qtd_pags = 100
                        ajuste = (qtd_pags / 2) * 0.1 + 2.0
                        st.session_state.livros.append({
                            "titulo": str(row.get('titulo', 'Sem título')).strip(), 
                            "cdd": str(row.get('cdd', row.get('classificacao', ''))).strip(), 
                            "paginas": str(qtd_pags), "dimensao": str(row.get('dimensao', '')).strip(),
                            "ed": str(row.get('ed', row.get('edicao', '1.ed.'))).strip(), 
                            "ex": str(row.get('ex', row.get('exemplar', 'Ex.1'))).strip(),
                            "extra1": str(row.get(st.session_state.cfg_nome_extra1.lower(), '')).strip(), 
                            "extra2": str(row.get(st.session_state.cfg_nome_extra2.lower(), '')).strip(),
                            "ajuste": min(ajuste, 50.0)
                        })
                        contador += 1
                    st.session_state.mensagem_sucesso = f"📊 Sucesso! {contador} livros importados em lote."
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao ler arquivo: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- COLUNA DIREITA: STATUS E NAVEGAÇÃO DA FILA ---
    with col_direita:
        st.markdown('<div class="custom-card"><div class="card-title">📋 Fila de Processamento</div>', unsafe_allow_html=True)
        st.metric(label="Total de Livros Prontos", value=len(st.session_state.livros))
        
        st.write(" ")
        if st.button("Processar Fila e Ver Estante Virtual ➡️", type="primary", use_container_width=True):
            mudar_tela("calibragem")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM (FÍSICA E 3D PRESERVADAS)
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.markdown("""
        <div style="background: white; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 15px; display: flex; align-items: center; gap: 15px;">
            <h3 style="margin: 0; color: #1e293b;">📚 Estante de Calibragem & Modelagem 3D</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ Voltar para a Tela de Entrada"):
        st.session_state.mostrar_3d = False
        mudar_tela("entrada")
        st.rerun()
    
    ordem_linhas_ativa = st.session_state.cfg_ordem_linhas

    if not st.session_state.livros:
        st.warning("Nenhum livro disponível na fila para calibragem.")
    else:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.write("👉 **Selecione um livro abaixo para projetar a lombada tridimensionalmente:**")
        
        cols_botoes = st.columns(min(len(st.session_state.livros), 10))
        for i, livro in enumerate(st.session_state.livros[:10]):
            with cols_botoes[i]:
                if st.button(f"📖 {livro.get('titulo')[:8]}...", key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                    st.session_state.mostrar_3d = True
                    st.rerun()
                    
        # --- MOTOR DA ESTANTE DIGITAL ---
        html_estante = "<div style='display: flex; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 20px; min-height: 260px; background-color: #f1f5f9; border-radius: 10px; overflow-x: auto;'>"
        for i, livro in enumerate(st.session_state.livros):
            largura_lombada = max(livro.get('ajuste', 15.0) * 4, 85) 
            borda_selecao = "outline: 3px solid #3b82f6;" if (st.session_state.mostrar_3d and st.session_state.livro_ativo == i) else ""
            t_tit = livro.get('titulo', 'Livro')
            
            tamanho_fonte_estante = "8px" if len(t_tit) < 18 else ("7px" if len(t_tit) < 35 else "6px")
            linhas_etiqueta = f'<div style="font-size: {tamanho_fonte_estante}; font-weight: bold; border-bottom: 1px solid #ddd; margin-bottom: 3px; word-wrap: break-word; width: 100%; padding-bottom: 1px; line-height: 1.1; max-height: 35px; overflow: hidden;">{t_tit.upper()}</div>'
            
            mapa_valores = {
                "Classificação": f'<div style="font-weight: bold; font-size: 10px;">{livro.get("cdd", "")}</div>',
                "Extra 1": f'<div style="font-size: 9px; color: #1E3A8A; font-weight: bold;">{livro.get("extra1", "")}</div>' if livro.get("extra1") else "",
                "Edição": f'<div style="font-size: 8px;">{livro.get("ed", "")}</div>',
                "Exemplar": f'<div style="font-size: 8px;">{livro.get("ex", "")}</div>',
                "Extra 2": f'<div style="font-size: 8px; color: #065F46;">{livro.get("extra2", "")}</div>' if livro.get("extra2") else ""
            }
            linhas_etiqueta += "".join([mapa_valores[chave] for chave in ordem_linhas_ativa if chave in mapa_valores])
            altura_etiqueta_estante = "85px" if len(ordem_linhas_ativa) > 3 else "72px"

            html_estante += f'<div style="flex: 0 0 {largura_lombada}px; width: {largura_lombada}px; height: 210px; background: #3b82f6; border-radius: 3px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; color: white; box-shadow: 4px 4px 8px rgba(0,0,0,0.15); position: relative; {borda_selecao} padding: 8px 2px 0 2px; box-sizing: border-box;"><div style="font-size: 10px; font-weight: bold; text-align: center; width: 100%; word-wrap: break-word; overflow: hidden; max-height: 40px; line-height: 1.1;">{t_tit[:12]}..</div><div style="width: 100%; background: white; color: black; font-family: \'Courier New\', monospace; font-size: 10px; border-top: 1px solid #ccc; padding: 4px 2px; text-align: center; box-sizing: border-box; line-height: 1.1; min-height: {altura_etiqueta_estante}; display: flex; flex-direction: column; justify-content: center;">{linhas_etiqueta}</div></div>'
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # INTERFACE INFERIOR DE DETALHES & MOTOR 3D
        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            if idx >= len(st.session_state.livros):
                st.session_state.mostrar_3d = False
                st.rerun()
                
            livro_sel = st.session_state.livros[idx]
            col_ajustes, col_3d = st.columns([1.2, 1])
            
            with col_ajustes:
                st.markdown('<div class="custom-card"><div class="card-title">⚙️ Calibrador de Espessura</div>', unsafe_allow_html=True)
                st.markdown(f"**Livro em Foco:** {livro_sel.get('titulo')}")
                
                novo_val = st.slider("Ajuste da Espessura da Lombada (mm)", 1.0, 50.0, float(livro_sel.get('ajuste', 15.0)), 0.5, key=f"slider_lombada_{idx}")
                st.session_state.livros[idx]['ajuste'] = novo_val
                
                if st.button("Remover Livro da Fila", type="secondary", use_container_width=True):
                    st.session_state.livros.pop(idx)
                    st.session_state.mostrar_3d = False
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_3d:
                st.markdown('<div class="custom-card"><div class="card-title">🔍 Visualização Tridimensional (3D)</div>', unsafe_allow_html=True)
                val_atual = st.session_state.livros[idx]['ajuste']
                
                cor_borda = "#3b82f6" 
                esp_3d = max(val_atual * 6, 60)
                
                t_tit_sel = livro_sel.get("titulo", "")
                tamanho_fonte_3d = "10px" if len(t_tit_sel) < 20 else ("8px" if len(t_tit_sel) < 40 else "7px")

                linhas_3d = f'<div style="text-align: center; font-size: {tamanho_fonte_3d}; font-weight: bold; border-bottom: 1px solid #ddd; margin-bottom: 4px; width: 100%; word-wrap: break-word; padding-bottom: 2px; line-height: 1.1; max-height: 50px; overflow: hidden;">{t_tit_sel.upper()}</div>'
                mapa_3d = {
                    "Classificação": f'<div style="text-align: center; font-weight: bold; font-size: 11px;">{livro_sel.get("cdd", "")}</div>',
                    "Extra 1": f'<div style="text-align: center; font-size: 10px; font-weight: bold; color: #1E3A8A;">{livro_sel.get("extra1", "")}</div>' if livro_sel.get("extra1") else "",
                    "Edição": f'<div style="text-align: center; font-size: 10px;">{livro_sel.get("ed", "")}</div>',
                    "Exemplar": f'<div style="text-align: center; font-size: 10px;">{livro_sel.get("ex", "")}</div>',
                    "Extra 2": f'<div style="text-align: center; font-size: 10px; color: #065F46; font-weight: bold;">{livro_sel.get("extra2", "")}</div>' if livro_sel.get("extra2") else ""
                }
                linhas_3d += "".join([mapa_3d[chave] for chave in ordem_linhas_ativa if chave in mapa_3d])
                altura_etiqueta_3d = "135px" if len(ordem_linhas_ativa) > 3 else "115px"

                html_renderizado = f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; height: 300px; margin-top:10px;">
                    <div style="width: {esp_3d}px; height: 260px; background: #3b82f6; border: 4px solid {cor_borda}; transform: rotateY(-20deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.2); display: flex; flex-direction: column; justify-content: flex-end; position: relative;">
                        <div style="width: 100%; min-height: {altura_etiqueta_3d}; background: white; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: 'Courier New', monospace; font-size: 11px; color: black; border-top: 1px solid #ccc; padding: 4px 2px; line-height: 1.2; overflow: hidden; box-sizing: border-box;">
                            {linhas_3d}
                        </div>
                    </div>
                    <div style="width: 130px; height: 260px; background: #cbd5e1; transform-origin: left; transform: rotateY(30deg); box-shadow: 15px 10px 25px rgba(0,0,0,0.15); display: flex; justify-content: center; align-items: center; color: #475569; font-size: 12px; font-weight: bold;">CAPA</div>
                </div>
                """
                st.markdown(html_renderizado, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                 
