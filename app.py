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
if "mensagem_sucesso" not in st.session_state:
    st.session_state.mensagem_sucesso = ""

# --- CONFIGURAÇÕES DE EXIBIÇÃO E ORDEM PERMANENTE ---
if "cfg_exibir_cdd" not in st.session_state: st.session_state.cfg_exibir_cdd = True
if "cfg_exibir_ed" not in st.session_state: st.session_state.cfg_exibir_ed = True
if "cfg_exibir_ex" not in st.session_state: st.session_state.cfg_exibir_ex = True
if "cfg_usar_extra1" not in st.session_state: st.session_state.cfg_usar_extra1 = False
if "cfg_nome_extra1" not in st.session_state: st.session_state.cfg_nome_extra1 = "Cutter"
if "cfg_usar_extra2" not in st.session_state: st.session_state.cfg_usar_extra2 = False
if "cfg_nome_extra2" not in st.session_state: st.session_state.cfg_nome_extra2 = "Coleção"

if "cfg_ordem_linhas" not in st.session_state:
    st.session_state.cfg_ordem_linhas = ["Classificação", "Extra 1", "Edição", "Exemplar", "Extra 2"]

def mudar_tela(nova_tela):
    st.session_state.tela = nova_tela

# ==========================================================
# TELA 1: ENTRADA DE DADOS E CONFIGURAÇÃO
# ==========================================================
if st.session_state.tela == "entrada":
    st.title("📝 BiblioKhan | Entrada de Dados")
    
    # Alerta Fixo de Sucesso Limpo
    if st.session_state.mensagem_sucesso:
        st.success(st.session_state.mensagem_sucesso)
        st.session_state.mensagem_sucesso = ""

    # --- ABAS DE INTERFACE TOTALMENTE SEPARADAS ---
    aba_manual, aba_lote, aba_config = st.tabs([
        "📝 Cadastro Manual", 
        "📁 Importar via CSV ou Planilha Excel", 
        "⚙️ Configurar Layout da Etiqueta"
    ])

    # ABA 1: CADASTRO MANUAL (Foco e Velocidade)
    with aba_manual:
        col_form, col_preview = st.columns([1.2, 1])
        
        with col_form:
            st.subheader("Dados do Livro")
            titulo = st.text_input("Título *", key="manual_titulo")
            classificacao = st.text_input("Classificação *", key="manual_cdd")
            
            c1, c2 = st.columns(2)
            paginas = c1.number_input("Páginas", min_value=1, value=100, key="manual_pags")
            dimensao = c2.text_input("Dimensão (ex: 23 cm)", key="manual_dim")
            
            c3, c4 = st.columns(2)
            edicao = c3.text_input("Edição", value="1.ed.", key="manual_ed")
            exemplar = c4.text_input("Exemplar", value="Ex.1", key="manual_ex")
            
            # Blocos condicionais rápidos baseados no Layout Salvo
            val_extra1 = ""
            if st.session_state.cfg_usar_extra1:
                val_extra1 = st.text_input(f"{st.session_state.cfg_nome_extra1}", key="manual_extra1")
                
            val_extra2 = ""
            if st.session_state.cfg_usar_extra2:
                val_extra2 = st.text_input(f"{st.session_state.cfg_nome_extra2}", key="manual_extra2")
            
            st.write(" ")
            if st.button("➕ Adicionar Livro à Lista", type="primary", use_container_width=True, key="btn_add_manual"):
                if titulo.strip() and classificacao.strip():
                    ajuste = (paginas / 2) * 0.1 + 2.0
                    novo_livro = {
                        "titulo": titulo.strip(), "cdd": classificacao.strip(), "paginas": str(paginas),
                        "dimensao": dimensao.strip(), "ed": edicao.strip(), "ex": exemplar.strip(),
                        "extra1": val_extra1.strip(), "extra2": val_extra2.strip(), "ajuste": min(ajuste, 50.0)
                    }
                    
                    if not st.session_state.livros or st.session_state.livros[-1] != novo_livro:
                        st.session_state.livros.append(novo_livro)
                        st.session_state.mensagem_sucesso = f"📖 Livro '{titulo.strip()}' adicionado com sucesso à lista!"
                        st.rerun()
                else: 
                    st.error("Preencha os campos obrigatórios (Título e Classificação).")

        with col_preview:
            st.subheader("📋 Etiqueta em Tempo Real")
            st.caption("Visualização instantânea baseada nas suas regras de layout:")
            
            dados_reais_digitados = {
                "Classificação": classificacao if classificacao else "---",
                "Extra 1": val_extra1 if val_extra1 else "---",
                "Edição": edicao if edicao else "---",
                "Exemplar": exemplar if exemplar else "---",
                "Extra 2": val_extra2 if val_extra2 else "---"
            }
            
            html_preview_linhas = ""
            for tag in st.session_state.cfg_ordem_linhas:
                estilo_linha = "font-weight: bold; font-size: 15px;" if tag in ["Classificação", "Extra 1"] else "font-size: 13px;"
                if (tag == "Classificação" and st.session_state.cfg_exibir_cdd) or \
                   (tag == "Extra 1" and st.session_state.cfg_usar_extra1) or \
                   (tag == "Edição" and st.session_state.cfg_exibir_ed) or \
                   (tag == "Exemplar" and st.session_state.cfg_exibir_ex) or \
                   (tag == "Extra 2" and st.session_state.cfg_usar_extra2):
                    html_preview_linhas += f'<div style="{estilo_linha}">{dados_reais_digitados[tag]}</div>'
                
            st.markdown(f"""
            <div style="display: flex; justify-content: center; background: #f0f2f6; padding: 25px; border-radius: 8px; border: 1px solid #dcdfe6; margin-top: 15px;">
                <div style="width: 140px; min-height: 160px; background: white; color: black; border: 2px dashed #4B0082; font-family: 'Courier New', monospace; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 12px; box-shadow: 2px 4px 12px rgba(0,0,0,0.15); line-height: 1.4;">
                    {html_preview_linhas}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ABA 2: IMPORTAÇÃO EM LOTE
    with aba_lote:
        st.subheader("Importar em Lote")
        info_lote = f"O arquivo enviado deve conter as colunas básicas: `titulo`, `cdd`, `paginas`, `dimensao`, `ed`, `ex`."
        if st.session_state.cfg_usar_extra1: info_lote += f" Inclua também a coluna: `{st.session_state.cfg_nome_extra1.lower()}`"
        if st.session_state.cfg_usar_extra2: info_lote += f" Inclua também a coluna: `{st.session_state.cfg_nome_extra2.lower()}`"
        st.info(info_lote)
        
        file = st.file_uploader("Subir arquivo de acervo (CSV ou Planilha Excel)", type=["csv", "xlsx", "xls"], key="uploader_lote")
        
        if file:
            try:
                if file.name.endswith('.csv'): df = pd.read_csv(file)
                else: df = pd.read_excel(file)
                
                df.columns = df.columns.str.lower()
                contador_sucesso = 0
                
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
                    contador_sucesso += 1
                    
                st.session_state.mensagem_sucesso = f"📊 Sucesso! {contador_sucesso} livros importados do arquivo."
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {e}.")

    # ABA 3: PAINEL DE CONFIGURAÇÕES ISOLADO (Evita lentidão no app)
    with aba_config:
        st.subheader("⚙️ Configurações Estruturais da Etiqueta")
        st.caption("Altere os parâmetros globais e a ordem das linhas abaixo:")
        
        c_cfg1, c_cfg2 = st.columns(2)
        with c_cfg1:
            exibir_cdd = st.checkbox("Exibir Classificação (CDD/CDU)", value=st.session_state.cfg_exibir_cdd)
            exibir_ed = st.checkbox("Exibir Edição", value=st.session_state.cfg_exibir_ed)
            exibir_ex = st.checkbox("Exibir Exemplar", value=st.session_state.cfg_exibir_ex)
        
        with c_cfg2:
            usar_extra1 = st.checkbox("Ativar Campo Extra 1 (Ex: Cutter)", value=st.session_state.cfg_usar_extra1)
            nome_extra1 = st.text_input("Nome Personalizado do Campo 1:", value=st.session_state.cfg_nome_extra1)
            usar_extra2 = st.checkbox("Ativar Campo Extra 2 (Ex: Coleção)", value=st.session_state.cfg_usar_extra2)
            nome_extra2 = st.text_input("Nome Personalizado do Campo 2:", value=st.session_state.cfg_nome_extra2)

        st.markdown("---")
        st.markdown("#### Definir Sequência de Linhas:")
        
        nomes_mapeados = {
            "Classificação": "Classificação" if exibir_cdd else None,
            "Extra 1": f"Extra 1 ({nome_extra1})" if usar_extra1 else None,
            "Edição": "Edição" if exibir_ed else None,
            "Exemplar": "Exemplar" if exibir_ex else None,
            "Extra 2": f"Extra 2 ({nome_extra2})" if usar_extra2 else None,
        }
        itens_ativos = [k for k, v in nomes_mapeados.items() if v is not None]
        
        ordem_atual = [x for x in st.session_state.cfg_ordem_linhas if x in itens_ativos]
        for item in itens_ativos:
            if item not in ordem_atual: ordem_atual.append(item)
                
        nova_ordem_escolhida = []
        for rank in range(len(itens_ativos)):
            opcoes_disponiveis = [x for x in itens_ativos if x not in nova_ordem_escolhida]
            default_index = 0
            if rank < len(ordem_atual) and ordem_atual[rank] in opcoes_disponiveis:
                default_index = opcoes_disponiveis.index(ordem_atual[rank])
                
            escolha_linha = st.selectbox(f"Linha {rank + 1}:", opcoes_disponiveis, index=default_index, key=f"cfg_order_{rank}")
            nova_ordem_escolhida.append(escolha_linha)

        st.write(" ")
        if st.button("💾 Salvar Modificações de Layout", type="primary", use_container_width=True):
            st.session_state.cfg_exibir_cdd = exibir_cdd
            st.session_state.cfg_exibir_ed = exibir_ed
            st.session_state.cfg_exibir_ex = exibir_ex
            st.session_state.cfg_usar_extra1 = usar_extra1
            st.session_state.cfg_nome_extra1 = nome_extra1
            st.session_state.cfg_usar_extra2 = usar_extra2
            st.session_state.cfg_nome_extra2 = nome_extra2
            st.session_state.cfg_ordem_linhas = nova_ordem_escolhida
            st.session_state.mensagem_sucesso = "Layout de etiqueta atualizado com sucesso para todo o acervo!"
            st.rerun()

    # --- BARRA GLOBAL INFERIOR ---
    st.write("---")
    st.metric(label="Livros na Fila Atual", value=len(st.session_state.livros))
    
    if st.button("Ir para Estante de Calibragem ➡️", type="primary", use_container_width=True):
        mudar_tela("calibragem")
        st.rerun()

# ==========================================================
# TELA 2: ESTANTE DE CALIBRAGEM (Intocada e Segura)
# ==========================================================
elif st.session_state.tela == "calibragem":
    st.title("📚 Estante de Calibragem")
    if st.button("⬅️ Voltar para Entrada"):
        st.session_state.mostrar_3d = False
        mudar_tela("entrada")
        st.rerun()
    
    st.write("---")
    ordem_linhas_ativa = st.session_state.cfg_ordem_linhas

    if not st.session_state.livros:
        st.warning("Nenhum livro cadastrado na estante virtual no momento.")
    else:
        st.write("👉 **Toque no botão do livro para abrir a calibragem detalhada e opções:**")
        cols_botoes = st.columns(len(st.session_state.livros))
        for i, livro in enumerate(st.session_state.livros):
            with cols_botoes[i]:
                if st.button(f"👁️ {livro.get('titulo')[:12]}...", key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                    st.session_state.mostrar_3d = True
                    st.rerun()
        
        # --- ESTANTE DIGITAL CONTÍNUA ---
        html_estante = "<div style='display: flex; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 25px; min-height: 260px; background-color: #f9f9f9; border-radius: 10px; overflow-x: auto;'>"
        
        for i, livro in enumerate(st.session_state.livros):
            largura_lombada = max(livro.get('ajuste', 15.0) * 4, 85) 
            borda_selecao = "outline: 3px solid #4B0082;" if (st.session_state.mostrar_3d and st.session_state.livro_ativo == i) else ""
            t_tit = livro.get('titulo', 'Livro')
            
            mapa_valores = {
                "Classificação": f'<div style="font-weight: bold; font-size: 10px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; padding: 0 1px;">{livro.get("cdd", "")}</div>',
                "Extra 1": f'<div style="font-size: 9px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #1E3A8A; font-weight: bold;">{livro.get("extra1", "")}</div>' if livro.get("extra1") else "",
                "Edição": f'<div style="font-size: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{livro.get("ed", "")}</div>',
                "Exemplar": f'<div style="font-size: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{livro.get("ex", "")}</div>',
                "Extra 2": f'<div style="font-size: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #065F46;">{livro.get("extra2", "")}</div>' if livro.get("extra2") else ""
            }
            
            linhas_etiqueta = "".join([mapa_valores[chave] for chave in ordem_linhas_ativa if chave in mapa_valores])
            altura_etiqueta_estante = "68px" if len(ordem_linhas_ativa) > 3 else "55px"

            html_estante += f'<div style="flex: 0 0 {largura_lombada}px; width: {largura_lombada}px; height: 210px; background: #A084E8; border-radius: 3px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; color: white; box-shadow: 4px 4px 8px rgba(0,0,0,0.2); position: relative; {borda_selecao} padding: 8px 2px 0 2px; box-sizing: border-box;"><div style="font-size: 10px; font-weight: bold; text-align: center; width: 100%; word-wrap: break-word; overflow: hidden; max-height: 50px; line-height: 1.1;">{t_tit}</div><div style="width: 100%; background: white; color: black; font-family: \'Courier New\', monospace; font-size: 10px; border-top: 1px solid #ccc; padding: 4px 0; text-align: center; box-sizing: border-box; line-height: 1.1; min-height: {altura_etiqueta_estante}; display: flex; flex-direction: column; justify-content: center;">{linhas_etiqueta}</div></div>'
            
        html_estante += "</div>"
        st.markdown(html_estante, unsafe_allow_html=True)
        
        st.write(" ")
        st.write("---")
        
        # INTERFACE INFERIOR DE DETALHES E REMOÇÃO
        if st.session_state.mostrar_3d:
            idx = st.session_state.livro_ativo
            if idx >= len(st.session_state.livros):
                st.session_state.mostrar_3d = False
                st.rerun()
                
            livro_sel = st.session_state.livros[idx]
            col_ajustes, col_3d = st.columns([1.2, 1])
            
            with col_ajustes:
                st.subheader(f"⚙️ Painel do Livro: {livro_sel.get('titulo')}")
                st.markdown(f"**Páginas:** {livro_sel.get('paginas')} | **Dimensão:** {livro_sel.get('dimensao')}")
                
                if st.session_state.cfg_usar_extra1 or st.session_state.cfg_usar_extra2:
                    st.write("**Campos Adicionais:**")
                    if st.session_state.cfg_usar_extra1:
                        st.session_state.livros[idx]["extra1"] = st.text_input(f"Editar {st.session_state.cfg_nome_extra1}:", value=livro_sel.get("extra1", ""), key=f"edit_ex1_{idx}")
                    if st.session_state.cfg_usar_extra2:
                        st.session_state.livros[idx]["extra2"] = st.text_input(f"Editar {st.session_state.cfg_nome_extra2}:", value=livro_sel.get("extra2", ""), key=f"edit_ex2_{idx}")
                
                st.write("---")
                novo_val = st.slider("Largura da Lombada (mm)", 1.0, 50.0, float(livro_sel.get('ajuste', 15.0)), 0.5, key=f"slider_lombada_{idx}")
                st.session_state.livros[idx]['ajuste'] = novo_val
                
                st.write(" ")
                if st.button("❌ Remover este Livro do Acervo", type="secondary", use_container_width=True, key=f"del_book_{idx}"):
                    titulo_removido = st.session_state.livros[idx].get('titulo', 'Livro')
                    st.session_state.livros.pop(idx)
                    st.session_state.mostrar_3d = False
                    st.session_state.livro_ativo = 0
                    st.toast(f"🗑️ '{titulo_removido}' foi removido com sucesso!", icon="🗑️")
                    st.rerun()
            
            with col_3d:
                st.subheader("🔍 Lombada Detalhada")
                val_atual = st.session_state.livros[idx]['ajuste']
                cor_borda = "#EF4444" if val_atual < 5.0 else "#22C55E"
                esp_3d = max(val_atual * 6, 60)
                
                mapa_3d = {
                    "Classificação": f'<div style="text-align: center; font-weight: bold; font-size: 11px; width: 100%; word-wrap: break-word;">{livro_sel.get("cdd", "")}</div>',
                    "Extra 1": f'<div style="text-align: center; font-size: 10px; margin-top: 2px; font-weight: bold; color: #1E3A8A;">{livro_sel.get("extra1", "")}</div>' if livro_sel.get("extra1") else "",
                    "Edição": f'<div style="text-align: center; font-size: 10px; margin-top: 2px;">{livro_sel.get("ed", "")}</div>',
                    "Exemplar": f'<div style="text-align: center; font-size: 10px;">{livro_sel.get("ex", "")}</div>',
                    "Extra 2": f'<div style="text-align: center; font-size: 10px; color: #065F46; font-weight: bold;">{livro_sel.get("extra2", "")}</div>' if livro_sel.get("extra2") else ""
                }
                linhas_3d = "".join([mapa_3d[chave] for chave in ordem_linhas_ativa if chave in mapa_3d])
                altura_etiqueta_3d = "115px" if len(ordem_linhas_ativa) > 3 else "95px"

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
