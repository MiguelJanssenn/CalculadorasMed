def pagina_dados_paciente():
    """Página de entrada de dados. Escreve em st.session_state."""
    st.title("Prontuário do Paciente")
    st.markdown("Insira os dados do paciente abaixo. Os resultados serão calculados automaticamente nas páginas de especialidade.")

    st.subheader("Dados Demográficos e Vitais")
    col1, col2 = st.columns(2)
    with col1:
        st.radio("Sexo Biológico", ["Feminino", "Masculino"], horizontal=True, key="sex")
        st.number_input("Idade (anos)", min_value=18, max_value=120, step=1, key="age", placeholder="Ex: 55")
    with col2:
        st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, step=0.1, format="%.1f", key="weight", placeholder="Ex: 70.0")
        st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, step=0.1, format="%.1f", key="height_cm", placeholder="Ex: 170.0")

    st.subheader("Dados Laboratoriais Unificados")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Creatinina Sérica (mg/dL)", min_value=0.1, max_value=20.0, step=0.1, format="%.1f", key="creatinine", placeholder="Ex: 1.0")
        st.number_input("Bilirrubina Total (mg/dL)", min_value=0.1, max_value=50.0, step=0.1, format="%.1f", key="bilirubin", placeholder="Ex: 1.2")
        st.number_input("Albumina Sérica (g/dL)", min_value=1.0, max_value=6.0, step=0.1, format="%.1f", key="albumin", placeholder="Ex: 4.0")
    with col2:
        st.number_input("Sódio Sérico (mEq/L)", min_value=100, max_value=180, step=1, key="sodium", placeholder="Ex: 140")
        st.number_input("INR", min_value=0.5, max_value=10.0, step=0.1, format="%.1f", key="inr", placeholder="Ex: 1.1")
        st.number_input("Plaquetas (x10³/µL)", min_value=10, max_value=1000, step=1, key="platelets", placeholder="Ex: 250")
    with col3:
        st.number_input("AST (TGO) (U/L)", min_value=1, max_value=1000, step=1, key="ast", placeholder="Ex: 25")
        st.number_input("ALT (TGP) (U/L)", min_value=1, max_value=1000, step=1, key="alt", placeholder="Ex: 25")

    st.subheader("Dados Metabólicos e de Risco")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Colesterol Total (mg/dL)", min_value=100, max_value=400, step=1, key="tc", placeholder="Ex: 200")
        st.number_input("Colesterol HDL (mg/dL)", min_value=15, max_value=150, step=1, key="hdl", placeholder="Ex: 50")
        st.number_input("Pressão Arterial Sistólica (PAS) (mm Hg)", min_value=80, max_value=250, step=1, key="sbp", placeholder="Ex: 120")
    with col2:
        st.number_input("Glicose de Jejum (mg/dL)", min_value=40, max_value=500, step=1, key="glucose_fasting", placeholder="Ex: 90")
        st.number_input("Insulina de Jejum (µU/mL)", min_value=1.0, max_value=300.0, step=0.1, format="%.1f", key="insulin_fasting", placeholder="Ex: 8.0")
        st.number_input("Relação Albumina/Creatinina Urinária (RAC) (mg/g)", min_value=0.0, max_value=5000.0, step=0.1, format="%.1f", key="uacr_val", placeholder="Opcional")
        st.number_input("Hemoglobina Glicada (HbA1c) (%)", min_value=3.0, max_value=20.0, step=0.1, format="%.1f", key="hba1c_val", placeholder="Opcional: Ex: 5.7")

    st.subheader("Histórico Clínico e Questionários")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Comorbidades e Hábitos**")
        st.checkbox("Diabetes Mellitus?", key="dm")
        st.checkbox("Fumante atual?", key="smoking")
        st.checkbox("Em uso de anti-hipertensivo?", key="bptreat")
        st.checkbox("Em uso de estatina?", key="statin")
        st.checkbox("Em diálise (2x na última semana)?", key="dialise")
    
    with col2:
        st.markdown("**Sintomas (Gastro/Pneumo)**")
        ascites_options = ["Ausente", "Leve", "Moderada/Grave"]
        st.selectbox("Ascite (Child-Pugh)", ascites_options, key="ascites")
        
        enceph_options = ["Ausente", "Grau 1-2", "Grau 3-4"]
        st.selectbox("Encefalopatia (Child-Pugh)", enceph_options, key="encephalopathy")
        
        mmrc_options = [
            "Grau 0: Dispneia apenas com exercício intenso",
            "Grau 1: Dispneia ao andar apressado ou subir ladeira leve",
            "Grau 2: Anda mais devagar ou precisa parar para respirar",
            "Grau 3: Para para respirar após ~100m",
            "Grau 4: Tanta dispneia que não sai de casa"
        ]
        st.selectbox("Dispneia (mMRC)", mmrc_options, key="mmrc_score")

    with col3:
        st.markdown("**Questionário CAT (DPOC)**")
        st.caption("Responda de 0 (Nunca) a 5 (Sempre):")
        st.slider("1. Tusso muito?", 0, 5, key="cat_1")
        st.slider("2. Tenho muito catarro?", 0, 5, key="cat_2")
        st.slider("3. Sinto o peito apertado?", 0, 5, key="cat_3")
        st.slider("4. Sinto falta de ar ao subir escadas?", 0, 5, key="cat_4")
        st.slider("5. Limitado(a) em casa?", 0, 5, key="cat_5")
        st.slider("6. Confiante para sair de casa?", 0, 5, key="cat_6")
        st.slider("7. Durmo profundamente?", 0, 5, key="cat_7")
        st.slider("8. Tenho muita energia?", 0, 5, key="cat_8")
