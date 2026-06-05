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

# Gerenciamento dinâmico de campos
if "campos_personalizados" not in st.session_state:
    st.session_state.campos_personalizados = []
if "ordem_campos" not in st.session_state:
    st.session_state.ordem_campos = ["cdd", "ed", "ex"] # Ordem padrão inicial

def mudar_tela(nova_tela):
    st.session_state.tela = nova_tela

# ==========================================================
# TELA 1: ENTRADA DE DADOS E CONFIGURAÇÃO
# ==========================================================
if st.session_state.tela == "entrada":
    st.title("📝 BiblioKhan | Entrada de Dados")
    
    # Criando as 3 Abas solicitadas
    aba_manual, aba_upload, aba_config = st.tabs(["📝 Cadastro Manual", "📥 Upload CSV", "⚙️ Configurar Etiqueta"])
    
    # ------------------ ABA 3: CONFIGURAÇÃO ------------------
    with aba_config:
        st.subheader("Configuração da Etiqueta")
        st.write("Crie novos campos (ex: Cutter, Volume) e defina a ordem em que aparecem na lombada.")
        
        c_novo_campo, c_btn_campo = st.columns([3, 1])
        with c_novo_campo:
            novo_campo = st.text_input("Nome do Novo Campo:", placeholder="Ex: Cutter")
        with c_btn_campo:
            st.write("") # Alinhamento
            st.write("")
            if st.button("Adicionar Campo", use_container_width=True):
                campo_limpo = novo_campo.strip()
                if campo_limpo and campo_limpo not in ["cdd", "ed", "ex"] and campo_limpo not in st.session_state.campos_personalizados:
                    st.session_state.campos_personalizados.append(campo_limpo)
                    st.session_state.ordem_campos.append(campo_limpo)
                    st.rerun()
                    
        st.write("---")
        # Dicionário de tradução para exibir nomes bonitos no multiselect
        nomes_exibicao = {"cdd": "Classificação", "ed": "Edição", "ex": "Exemplar"}
        for c in st.session_state.campos_personalizados:
            nomes_exibicao[c] = c
            
        st.session_state.ordem_campos = st.multiselect(
            "Ordem de exibição na Etiqueta (Selecione na ordem desejada ou remova os que não quer):",
            options=list(nomes_exibicao.keys()),
            default=[c for c in st.session_state.ordem_campos if c in nomes_exibicao],
            format_func=lambda x: nomes_exibicao.get(x, x)
        )

    # ------------------ ABA 1: MANUAL ------------------
    with aba_manual:
        with st.form("manual"):
            titulo = st.text_input("Título *")
            classificacao = st.text_input("Classificação *")
            
            c1, c2 = st.columns(2)
            paginas = c1.number_input("Páginas", min_value=1, value=100)
            dimensao = c2.text_input("Dimensão (ex: 23 cm)")
            
            c3, c4 = st.columns(2)
            edicao = c3.text_input("Edição", value="1.ed.")
            exemplar = c4.text_input("Exemplar", value="Ex.1")
            
            # Renderiza os campos dinâmicos criados na aba de configuração
            valores_dinamicos = {}
            if st.session_state.campos_personalizados:
                st.write("**Campos Extras:**")
                cols_extras = st.columns(min(len(st.session_state.campos_personalizados), 4))
                for idx, campo in enumerate(st.session_state.campos_personalizados):
                    with cols_extras[idx % len(cols_extras)]:
                        valores_dinamicos[campo] = st.text_input(campo)
            
            if st.form_submit_button("Adicionar à Lista"):
                if titulo and classificacao:
                    ajuste = (paginas / 2) * 0.1 + 2.0
                    novo_livro = {
                        "titulo": titulo.strip(), 
                        "cdd": classificacao.strip(), 
                        "paginas": str(paginas),
                        "dimensao": dimensao.strip(),
                        "ed": edicao.strip(),
                        "ex": exemplar.strip(),
                        "ajuste": min(ajuste, 50.0)
                    }
                    for k, v in valores_dinamicos.items():
                        novo_livro[k] = v.strip()
                        
                    st.session_state.livros.append(novo_livro)
                    st.success(f"'{titulo}' adicionado!")
                else:
                    st.error("Por favor, preencha Título e Classificação.")
    
    # ------------------ ABA 2: UPLOAD ------------------
    with aba_upload:
        st.info("O arquivo CSV deve conter: titulo, cdd, paginas, dimensao, ed, ex. Campos extras criados também serão lidos se existirem como colunas.")
        file = st.file_uploader("Subir arquivo (CSV ou XLSX)", type=["csv", "xlsx"])
        if file:
            try:
                df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
                df.columns = df.columns.str.lower()
                
                for _, row in df.iterrows():
                    pags = str(row.get('paginas', '100'))
                    try:
                        qtd_pags = int(float(pags)) if pags.replace('.','',1).isdigit() else 100
                    except:
                        qtd_pags = 100
                    ajuste = (qtd_pags / 2) * 0.1 + 2.0
                    
                    livro_imp = {
                        "titulo": str(row.get('titulo', 'Sem título')).strip(), 
                        "cdd": str(row.get('cdd', row.get('classificacao', ''))).strip(), 
                        "paginas": str(qtd_pags),
                        "dimensao": str(row.get('dimensao', '')).strip(),
                        "ed": str(row.get('ed', row.get('edicao', '1.ed.'))).strip(),
                        "ex": str(row.get('ex', row.get('exemplar', 'Ex.1'))).strip(),
                        "ajuste": min(ajuste, 50.0)
                    }
                    
                    # Lê os campos personalizados da planilha
                    for campo in st.session_state.campos_personalizados:
                        col_nome = campo.lower()
                        if col_nome in df.columns and pd.notna(row.get(col_nome)):
                            livro_imp[campo] = str(row.get(col_nome)).strip()
                        else:
                            livro_imp[campo] = ""
                            
                    st.session_state.livros.append(livro_imp)
                st.success("Dados importados com sucesso!")
            except Exception as e:
                st.error(f"Erro na importação: {e}")

    st.write("---")
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
        
        # Botões nativos estáveis para seleção
        cols_botoes = st.columns(len(st.session_state.livros))
        for i, livro in enumerate(st.session_state.livros):
            with cols_botoes[i]:
                if st.button(f"👁️ {livro.get('titulo')[:12]}...", key=f"btn_{i}"):
                    st.session_state.livro_ativo = i
                    st.session_state.mostrar_3d = True
                    st.rerun()
        
        # --- ESTANTE DIGITAL COMPACTADA ---
        html_estante = "<div style='display: flex; align-items: flex-end; border-bottom: 20px solid #5D4037; padding: 20px; gap: 25px; min-height: 260px; background-color: #f9f9f9; border-radius: 10px; overflow-x: auto;'>"
        
        for i, livro in enumerate(st.session_state.livros):
            largura_lombada = max(livro.get('ajuste', 15.0) * 4, 80) 
            borda_selecao = "outline: 3px solid #4B0082;" if (st.session_state.mostrar_3d and st.session_state.livro_ativo == i) else ""
            t_tit = livro.get('titulo', 'Livro')
            
            # Gera as linhas da etiqueta dinamicamente de acordo com a ordem definida
            divs_etiqueta = ""
            for campo in st.session_state.ordem_campos:
                valor = livro.get(campo, '')
                if valor:
                    if campo == 'cdd':
                        divs_etiqueta += f'<div style="font-weight: bold; font-size: 10px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; padding: 0 1px;">{valor}</div>'
                    else:
                        divs_etiqueta += f'<div style="font-size: 9px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{valor}</div>'
            
            html_estante += f'<div style="flex: 0 0 {largura_lombada}px; width: {largura_lombada}px; height: 210px; background: #A084E8; border-radius: 3px; display: flex; flex-direction: column; justify-content: space-between; align-items: center; color: white; box-shadow: 4px 4px 8px rgba(0,0,0,0.2); position: relative; {borda_selecao} padding: 8px 2px 0 2px; box-sizing: border-box;"><div style="font-size: 10px; font-weight: bold; text-align: center; width: 100%; word-wrap: break-word; overflow: hidden; max-height: 50px; line-height: 1.1;">{t_tit}</div><div style="width: 100%; background: white; color: black; font-family: \'Courier New\', monospace; font-size: 10px; border-top: 1px solid #bbb; padding: 4px 0; text-align: center; box-sizing: border-box; line-height: 1.1;">{divs_etiqueta}</div></div>'
            
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
                * **Classificação:** {livro_sel.get('cdd', 'Sem Classificação')}
                * **Páginas:** {pags_txt} pág.
                * **Dimensão:** {dim_txt if dim_txt and dim_txt != 'nan' else 'Não informada'}
                """)
                
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
                
                # Gera as linhas dinâmicas para a visualização 3D detalhada
                divs_3d = ""
                for campo in st.session_state.ordem_campos:
                    valor = livro_sel.get(campo, '')
                    if valor:
                        peso_fonte = "bold" if campo == 'cdd' else "normal"
                        tam_fonte = "11px" if campo == 'cdd' else "10px"
                        margem = "margin-top: 2px;" if campo != 'cdd' else ""
                        divs_3d += f'<div style="text-align: center; font-weight: {peso_fonte}; font-size: {tam_fonte}; {margem} width: 100%; word-wrap: break-word;">{valor}</div>'
                
                html_renderizado = f"""
                <div style="perspective: 1000px; display: flex; justify-content: center; margin-top: 20px; height: 320px;">
                    <div style="width: {esp_3d}px; height: 280px; background: #A084E8; border: 5px solid {cor_borda}; transform: rotateY(-20deg); box-shadow: -10px 10px 20px rgba(0,0,0,0.4); display: flex; flex-direction: column; justify-content: flex-end; position: relative;">
                        <div style="width: 100%; min-height: 95px; background: white; display: flex; flex-direction: column; justify-content: center; align-items: center; font-family: 'Courier New', monospace; color: black; border-top: 1px solid #ccc; padding: 4px 2px; line-height: 1.2; overflow: hidden;">
                            {divs_3d}
                        </div>
                    </div>
                    <div style="width: 140px; height: 280px; background: #D1D5DB; transform-origin: left; transform: rotateY(30deg); box-shadow: 20px 10px 30px rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; color: #4B5563; font-size: 12px; font-weight: bold;">CAPA</div>
                </div>
                """
                st.markdown(html_renderizado, unsafe_allow_html=True)
