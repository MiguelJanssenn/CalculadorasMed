import streamlit as st
import math
import numpy as np

# --- INÍCIO: SEÇÃO DA CALCULADORA PREVENT ---

# --- FUNÇÕES AUXILIARES (Portadas do R) ---
def mmol_conversion_py(cholesterol):
    """ Porta da função mmol_conversion do R """
    if cholesterol is None or math.isnan(cholesterol):
        return np.nan
    return 0.02586 * cholesterol

def adjust_py(uacr):
    """ Porta da função adjust do R """
    if uacr is None or math.isnan(uacr):
        return np.nan  # Propaga o valor ausente
    if uacr >= 0.1:
        return uacr
    elif 0 <= uacr < 0.1:
        return 0.1
    return np.nan  # Valores negativos são inválidos

# --- FUNÇÕES DE CÁLCULO (UMA PARA CADA MODELO DO R) ---

def calcular_prevent_base_py(sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin):
    """ Porta da função 'pred_risk_base' do R """
    logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
    
    if sex == 1: # Feminino
        logor_10yr_CVD = -3.307728 + \
            0.7939329*(age - 55)/10 + \
            0.0305239*(mmol_conversion_py(tc - hdl) - 3.5) - \
            0.1606857*(mmol_conversion_py(hdl) - 1.3)/(0.3) - \
            0.2394003*(min(sbp, 110) - 110)/20 + \
            0.360078*(max(sbp, 110) - 130)/20 + \
            0.8667604*(dm) + \
            0.5360739*(smoking) + \
            0.6045917*(min(egfr, 60) - 60)/(-15) + \
            0.0433769*(max(egfr, 60) - 90)/(-15) + \
            0.3151672*(bptreat) - \
            0.1477655*(statin) - \
            0.0663612*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1197879*(statin)*(mmol_conversion_py(tc - hdl) - 3.5) - \
            0.0819715*(age - 55)/10*(mmol_conversion_py(tc - hdl) - 3.5) + \
            0.0306769*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/(0.3) - \
            0.0946348*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.27057*(age - 55)/10*(dm) - \
            0.078715*(age - 55)/10*(smoking) - \
            0.1637806*(age - 55)/10*(min(egfr, 60) - 60)/(-15)

        logor_10yr_ASCVD = -3.819975 + \
            0.719883*(age - 55)/10 + \
            0.1176967*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.151185*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0835358*(min(sbp, 110) - 110)/20 + \
            0.3592852*(max(sbp, 110) - 130)/20 + \
            0.8348585*(dm) + 0.4831078*(smoking) + \
            0.4864619*(min(egfr, 60) - 60)/(-15) + \
            0.0397779*(max(egfr, 60)  - 90)/(-15) + \
            0.2265309*(bptreat) - \
            0.0592374*(statin) - \
            0.0395762*(bptreat)*(max(sbp, 110) - 130)/20  + \
            0.0844423*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0567839*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0325692*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.1035985*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2417542*(age - 55)/10*(dm) - \
            0.0791142*(age - 55)/10*(smoking) - \
            0.1671492*(age - 55)/10*(min(egfr, 60) - 60)/(-15)

        logor_10yr_HF = -4.310409 + \
            0.8998235*(age - 55)/10 - \
            0.4559771*(min(sbp, 110) - 110)/20 + \
            0.3576505*(max(sbp, 110) - 130)/20 + \
            1.038346*(dm) + \
            0.583916*(smoking) - \
            0.0072294*(min(bmi, 30) - 25)/5 + \
            0.2997706*(max(bmi, 30) - 30)/5 + \
            0.7451638*(min(egfr, 60) - 60)/(-15) + \
            0.0557087*(max(egfr, 60)  - 90)/(-15) + \
            0.3534442*(bptreat) - \
            0.0981511*(bptreat)*(max(sbp, 110) - 130)/20  - \
            0.0946663*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.3581041*(age - 55)/10*(dm) - \
            0.1159453*(age - 55)/10*(smoking) - \
            0.003878*(age - 55)/10*(max(bmi, 30) - 30)/5 - \
            0.1884289*(age - 55)/10*(min(egfr, 60) - 60)/(-15)

    else: # Masculino
        logor_10yr_CVD = -3.031168 + \
            0.7688528*(age - 55)/10 + \
            0.0736174*(mmol_conversion_py(tc - hdl) - 3.5) - \
            0.0954431*(mmol_conversion_py(hdl) - 1.3)/(0.3) - \
            0.4347345*(min(sbp, 110) - 110)/20 + \
            0.3362658*(max(sbp, 110) - 130)/20 + \
            0.7692857*(dm) + \
            0.4386871*(smoking) + \
            0.5378979*(min(egfr, 60) - 60)/(-15) + \
            0.0164827*(max(egfr, 60) - 90)/(-15) + \
            0.288879*(bptreat) - \
            0.1337349*(statin) - \
            0.0475924*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.150273*(statin)*(mmol_conversion_py(tc - hdl) - 3.5) - \
            0.0517874*(age - 55)/10*(mmol_conversion_py(tc - hdl) - 3.5) + \
            0.0191169*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/(0.3) - \
            0.1049477*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2251948*(age - 55)/10*(dm) - \
            0.0895067*(age - 55)/10*(smoking) - \
            0.1543702*(age - 55)/10*(min(egfr, 60) - 60)/(-15)
        
        logor_10yr_ASCVD = -3.500655 + \
            0.7099847*(age - 55)/10 + \
            0.1658663*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1144285*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2837212*(min(sbp, 110) - 110)/20 + \
            0.3239977*(max(sbp, 110) - 130)/20 + \
            0.7189597*(dm) + \
            0.3956973*(smoking) + \
            0.3690075*(min(egfr, 60) - 60)/(-15) + \
            0.0203619*(max(egfr, 60)  - 90)/(-15) + \
            0.2036522*(bptreat) - \
            0.0865581*(statin) - \
            0.0322916*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.114563*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0300005*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0232747*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0927024*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2018525*(age - 55)/10*(dm) - \
            0.0970527*(age - 55)/10*(smoking) - \
            0.1217081*(age - 55)/10*(min(egfr, 60) - 60)/(-15)

        logor_10yr_HF = -3.946391 + \
            0.8972642*(age - 55)/10 - \
            0.6811466*(min(sbp, 110) - 110)/20 + \
            0.3634461*(max(sbp, 110) - 130)/20 + \
            0.923776*(dm) + \
            0.5023736*(smoking) - \
            0.0485841*(min(bmi, 30) - 25)/5 + \
            0.3726929*(max(bmi, 30) - 30)/5 + \
            0.6926917*(min(egfr, 60) - 60)/(-15) + \
            0.0251827*(max(egfr, 60)  - 90)/(-15) + \
            0.2980922*(bptreat) - \
            0.0497731*(bptreat)*(max(sbp, 110) - 130)/20 - \
            0.1289201*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.3040924*(age - 55)/10*(dm) - \
            0.1401688*(age - 55)/10*(smoking) + \
            0.0068126*(age - 55)/10*(max(bmi, 30) - 30)/5 - \
            0.1797778*(age - 55)/10*(min(egfr, 60) - 60)/(-15)
    
    return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

def calcular_prevent_uacr_py(sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, uacr):
    """ Porta da função 'pred_risk_uacr' do R """
    logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
    adj_uacr = adjust_py(uacr)
    log_uacr = math.log(adj_uacr) if not math.isnan(adj_uacr) else np.nan
    
    if sex == 1: # Feminino
        uacr_term_cvd = 0.0132073 if math.isnan(log_uacr) else 0.1793037*log_uacr
        uacr_term_ascvd = 0.0050257 if math.isnan(log_uacr) else 0.1501217*log_uacr
        uacr_term_hf = 0.0326667 if math.isnan(log_uacr) else 0.2197281*log_uacr

        logor_10yr_CVD = -3.738341 + 0.7969249*((age - 55)/10) + \
            0.0256635*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1588107*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.2255701*(min(sbp, 110) - 110)/20 + 0.3396649*(max(sbp, 110) - 130)/20 + \
            0.8047515*(dm) + 0.5285338*(smoking) + \
            0.4803511*(min(egfr, 60) - 60)/(-15) + 0.0434472*(max(egfr, 60) - 90)/(-15) + \
            0.2985207*(bptreat) - 0.1497787*(statin) - \
            0.0742889*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.106756*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0778126*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0306768*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0907168*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2705122*(age - 55)/10*(dm) - 0.0830564*(age - 55)/10*(smoking) - \
            0.1389249*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_cvd

        logor_10yr_ASCVD = -4.174614 + 0.7201999*((age - 55)/10) + \
            0.1135771*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1493506*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0726677*(min(sbp, 110) - 110)/20 + 0.3436259*(max(sbp, 110) - 130)/20 + \
            0.7773094*(dm) + 0.4746662*(smoking) + \
            0.3824646*(min(egfr, 60) - 60)/(-15) + 0.0394178*(max(egfr, 60) - 90)/(-15) + \
            0.2125182*(bptreat) - 0.0603046*(statin) - \
            0.0466053*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.0733118*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0534262*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0325689*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0999887*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2411762*(age - 55)/10*(dm) - 0.0826941*(age - 55)/10*(smoking) - \
            0.1444737*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_ascvd

        logor_10yr_HF = -4.841506 + 0.9145975*((age - 55)/10) - \
            0.4441346*(min(sbp, 110) - 110)/20 + 0.3260323*(max(sbp, 110) - 130)/20 + \
            0.9611365*(dm) + 0.5755787*(smoking) + \
            0.0008831*(min(bmi, 30) - 25)/5 + 0.2988964*(max(bmi, 30) - 30)/5 + \
            0.5915291*(min(egfr, 60) - 60)/(-15) + 0.0556823*(max(egfr, 60) - 90)/(-15) + \
            0.3314097*(bptreat) - 0.1078596*(bptreat)*(max(sbp, 110) - 130)/20 - \
            0.0875231*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.356859*(age - 55)/10*(dm) - 0.1220248*(age - 55)/10*(smoking) - \
            0.0053637*(age - 55)/10*(max(bmi, 30) - 30)/5 - \
            0.1610389*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_hf

    else: # Masculino
        uacr_term_cvd = 0.0916979 if math.isnan(log_uacr) else 0.1887974*log_uacr
        uacr_term_ascvd = 0.0556 if math.isnan(log_uacr) else 0.1510073*log_uacr
        uacr_term_hf = 0.1472194 if math.isnan(log_uacr) else 0.2306299*log_uacr

        logor_10yr_CVD = -3.510705 + 0.7768655*((age - 55)/10) + \
            0.0659949*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0951111*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.420667*(min(sbp, 110) - 110)/20 + 0.3120151*(max(sbp, 110) - 130)/20 + \
            0.698521*(dm) + 0.4314669*(smoking) + \
            0.3841364*(min(egfr, 60) - 60)/(-15) + 0.009384*(max(egfr, 60) - 90)/(-15) + \
            0.2676494*(bptreat) - 0.1390966*(statin) - \
            0.0579315*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1383719*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0488332*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0200406*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.102454*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2236355*(age - 55)/10*(dm) - 0.089485*(age - 55)/10*(smoking) - \
            0.1321848*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_cvd
        
        logor_10yr_ASCVD = -3.85146 + 0.7141718*((age - 55)/10) + \
            0.1602194*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1139086*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.2719456*(min(sbp, 110) - 110)/20 + 0.3058719*(max(sbp, 110) - 130)/20 + \
            0.6600631*(dm) + 0.3884022*(smoking) + \
            0.2466316*(min(egfr, 60) - 60)/(-15) + 0.0151852*(max(egfr, 60) - 90)/(-15) + \
            0.186167*(bptreat) - 0.0894395*(statin) - \
            0.0411884*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1058212*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.028089*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0240427*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0912325*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2004894*(age - 55)/10*(dm) - 0.096936*(age - 55)/10*(smoking) - \
            0.1022867*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_ascvd

        logor_10yr_HF = -4.556907 + 0.9111795*((age - 55)/10) - \
            0.6693649*(min(sbp, 110) - 110)/20 + 0.3290082*(max(sbp, 110) - 130)/20 + \
            0.8377655*(dm) + 0.4978917*(smoking) - \
            0.042749*(min(bmi, 30) - 25)/5 + \
            0.3624165*(max(bmi, 30) - 30)/5 + \
            0.5075796*(min(egfr, 60) - 60)/(-15) + 0.0137716*(max(egfr, 60) - 90)/(-15) + \
            0.2739963*(bptreat) - 0.0645712*(bptreat)*(max(sbp, 110) - 130)/20 - \
            0.1230039*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.3013297*(age - 55)/10*(dm) - 0.1410318*(age - 55)/10*(smoking) + \
            0.0021531*(age - 55)/10*(max(bmi, 30) - 30)/5 - \
            0.1548018*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_hf
    
    return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

def calcular_prevent_hba1c_py(sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, hba1c):
    """ Porta da função 'pred_risk_hba1c' do R """
    logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
    hba1c_val = hba1c if (hba1c is not None and not math.isnan(hba1c)) else np.nan
    
    if sex == 1: # Feminino
        hba1c_term_cvd = -0.0142496 if math.isnan(hba1c_val) else (0.1338348*(hba1c_val-5.3)*(dm) + 0.1622409*(hba1c_val-5.3)*(1-dm))
        hba1c_term_ascvd = 0.0015678 if math.isnan(hba1c_val) else (0.1339055*(hba1c_val-5.3)*(dm) + 0.1596461*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0143112 if math.isnan(hba1c_val) else (0.1856442*(hba1c_val-5.3)*(dm) + 0.1833083*(hba1c_val-5.3)*(1-dm))

        logor_10yr_CVD = -3.306162 + 0.7858178*((age - 55)/10) + \
            0.0194438*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1521964*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.2296681*(min(sbp, 110) - 110)/20 + 0.3465777*(max(sbp, 110) - 130)/20 + \
            0.5366241*(dm) + 0.5411682*(smoking) + \
            0.5931898*(min(egfr, 60) - 60)/(-15) + 0.0472458*(max(egfr, 60) - 90)/(-15) + \
            0.3158567*(bptreat) - 0.1535174*(statin) - \
            0.0687752*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1054746*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0761119*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0307469*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0905966*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2241857*(age - 55)/10*(dm) - 0.080186*(age - 55)/10*(smoking) - \
            0.1667286*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_cvd
        
        logor_10yr_ASCVD = -3.838746 + 0.7111831*((age - 55)/10) + \
            0.106797*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1425745*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0736824*(min(sbp, 110) - 110)/20 + 0.3480844*(max(sbp, 110) - 130)/20 + \
            0.5112951*(dm) + 0.4880292*(smoking) + \
            0.4754997*(min(egfr, 60) - 60)/(-15) + 0.0438132*(max(egfr, 60) - 90)/(-15) + \
            0.2259093*(bptreat) - 0.0648872*(statin) - \
            0.0437645*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.0697082*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0506382*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0327475*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0996442*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.1924338*(age - 55)/10*(dm) - 0.0803539*(age - 55)/10*(smoking) - \
            0.1682586*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_ascvd

        logor_10yr_HF = -4.288225 + 0.8997391*((age - 55)/10) - \
            0.4422749*(min(sbp, 110) - 110)/20 + 0.3378691*(max(sbp, 110) - 130)/20 + \
            0.681284*(dm) + 0.5886005*(smoking) - \
            0.0148657*(min(bmi, 30) - 25)/5 + 0.2958374*(max(bmi, 30) - 30)/5 + \
            0.73447*(min(egfr, 60) - 60)/(-15) + 0.05926*(max(egfr, 60) - 90)/(-15) + \
            0.3543475*(bptreat) - \
            0.1002139*(bptreat)*(max(sbp, 110) - 130)/20 - \
            0.0878765*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.303684*(age - 55)/10*(dm) - 0.1178943*(age - 55)/10*(smoking) - \
            0.008345*(age - 55)/10*(max(bmi, 30) - 30)/5 - \
            0.1912183*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_hf
    
    else: # Masculino
        hba1c_term_cvd = -0.0128373 if math.isnan(hba1c_val) else (0.13159*(hba1c_val-5.3)*(dm) + 0.1295185*(hba1c_val-5.3)*(1-dm))
        hba1c_term_ascvd = -0.0010001 if math.isnan(hba1c_val) else (0.1157161*(hba1c_val-5.3)*(dm) + 0.1288303*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0113444 if math.isnan(hba1c_val) else (0.1652857*(hba1c_val-5.3)*(dm) + 0.1505859*(hba1c_val-5.3)*(1-dm))

        logor_10yr_CVD = -3.040901 + 0.7699177*((age - 55)/10) + \
            0.0605093*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0888525*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.417713*(min(sbp, 110) - 110)/20 + 0.3288657*(max(sbp, 110) - 130)/20 + \
            0.4759471*(dm) + 0.4385663*(smoking) + \
            0.5334616*(min(egfr, 60) - 60)/(-15) + 0.0206431*(max(egfr, 60) - 90)/(-15) + \
            0.2917524*(bptreat) - 0.1383313*(statin) - \
            0.0482622*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1393796*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0463501*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0205926*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.1037717*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.1737697*(age - 55)/10*(dm) - 0.0915839*(age - 55)/10*(smoking) - \
            0.1637039*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_cvd
        
        logor_10yr_ASCVD = -3.51835 + 0.7064146*((age - 55)/10) + \
            0.1532267*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1082166*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.2675288*(min(sbp, 110) - 110)/20 + 0.3173809*(max(sbp, 110) - 130)/20 + \
            0.432604*(dm) + 0.3958842*(smoking) + \
            0.3665014*(min(egfr, 60) - 60)/(-15) + 0.0250243*(max(egfr, 60) - 90)/(-15) + \
            0.2061158*(bptreat) - 0.0899988*(statin) - \
            0.0334959*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1034168*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0255406*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0247538*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0917441*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.1499195*(age - 55)/10*(dm) - 0.098089*(age - 55)/10*(smoking) - \
            0.1305231*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_ascvd

        logor_10yr_HF = -3.961954 + 0.911787*((age - 55)/10) - \
            0.6568071*(min(sbp, 110) - 110)/20 + 0.3524645*(max(sbp, 110) - 130)/20 + \
            0.5849752*(dm) + 0.5014014*(smoking) - \
            0.0512352*(min(bmi, 30) - 25)/5 + \
            0.365294*(max(bmi, 30) - 30)/5 + \
            0.6892219*(min(egfr, 60) - 60)/(-15) + 0.0292377*(max(egfr, 60) - 90)/(-15) + \
            0.3038296*(bptreat) - \
            0.0515032*(bptreat)*(max(sbp, 110) - 130)/20 - \
            0.1262343*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2449514*(age - 55)/10*(dm) - 0.1392217*(age - 55)/10*(smoking) + \
            0.0009592*(age - 55)/10*(max(bmi, 30) - 30)/5 - \
            0.1917105*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_hf

    return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

def calcular_prevent_full_py(sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, uacr, hba1c):
    """ Porta da função 'pred_risk_full' do R, SEM SDI """
    logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
    adj_uacr = adjust_py(uacr)
    log_uacr = math.log(adj_uacr) if not math.isnan(adj_uacr) else np.nan
    hba1c_val = hba1c if (hba1c is not None and not math.isnan(hba1c)) else np.nan
    
    # Coeficiente "ausente" para SDI (já que o removemos)
    sdi_term_cvd_f = 0.1804508
    sdi_term_ascvd_f = 0.1588908
    sdi_term_hf_f = 0.1819138
    sdi_term_cvd_m = 0.144759
    sdi_term_ascvd_m = 0.1388492
    sdi_term_hf_m = 0.1694628
    
    if sex == 1: # Feminino
        uacr_term_cvd = 0.0198413 if math.isnan(log_uacr) else 0.1645922*log_uacr
        uacr_term_ascvd = 0.0061613 if math.isnan(log_uacr) else 0.1371824*log_uacr
        uacr_term_hf = 0.0395368 if math.isnan(log_uacr) else 0.1948135*log_uacr
        hba1c_term_cvd = -0.0031658 if math.isnan(hba1c_val) else (0.1298513*(hba1c_val-5.3)*(dm) + 0.1412555*(hba1c_val-5.3)*(1 - dm))
        hba1c_term_ascvd = 0.005866 if math.isnan(hba1c_val) else (0.123192*(hba1c_val-5.3)*(dm) + 0.1410572*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0010583 if math.isnan(hba1c_val) else (0.176668*(hba1c_val-5.3)*(dm) + 0.1614911*(hba1c_val-5.3)*(1-dm))

        logor_10yr_CVD = -3.860385 + 0.7716794*((age - 55)/10) + \
            0.0062109*(mmol_conversion_py(tc - hdl) - 3.5) - \
            0.1547756*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.1933123*(min(sbp, 110) - 110)/20 + 0.3071217*(max(sbp, 110) - 130)/20 + \
            0.496753*(dm) + 0.466605*(smoking) + \
            0.4780697*(min(egfr, 60) - 60)/(-15) + 0.0529077*(max(egfr, 60) - 90)/(-15) + \
            0.3034892*(bptreat) - 0.1556524*(statin) - \
            0.0667026*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1061825*(statin)*(mmol_conversion_py(tc - hdl) - 3.5) - \
            0.0742271*(age - 55)/10*(mmol_conversion_py(tc - hdl) - 3.5) + \
            0.0288245*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0875188*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2267102*(age - 55)/10*(dm) - 0.0676125*(age - 55)/10*(smoking) - \
            0.1493231*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + \
            sdi_term_cvd_f + uacr_term_cvd + hba1c_term_cvd

        logor_10yr_ASCVD = -4.291503 + 0.7023067*((age - 55)/10) + \
            0.0898765*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1407316*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0256648*(min(sbp, 110) - 110)/20 + 0.314511*(max(sbp, 110) - 130)/20 + \
            0.4799217*(dm) + 0.4062049*(smoking) + \
            0.3847744*(min(egfr, 60) - 60)/(-15) + 0.0495174*(max(egfr, 60) - 90)/(-15) + \
            0.2133861*(bptreat) - 0.0678552*(statin) - \
            0.0451416*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.0788187*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0535985*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0291762*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0961839*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2001466*(age - 55)/10*(dm) - 0.0586472*(age - 55)/10*(smoking) - \
            0.1537791*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + \
            sdi_term_ascvd_f + uacr_term_ascvd + hba1c_term_ascvd

        logor_10yr_HF = -4.896524 + 0.884209*((age - 55)/10) - \
            0.421474*(min(sbp, 110) - 110)/20 + 0.3002919*(max(sbp, 110) - 130)/20 + \
            0.6170359*(dm) + 0.5380269*(smoking) - \
            0.0191335*(min(bmi, 30) - 25)/5 + 0.2764302*(max(bmi, 30) - 30)/5 + \
            0.5975847*(min(egfr, 60) - 60)/(-15) + 0.0654197*(max(egfr, 60) - 90)/(-15) + \
            0.3313614*(bptreat) - 0.1002304*(bptreat)*(max(sbp, 110) - 130)/20 - \
            0.0845363*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2989062*(age - 55)/10*(dm) - 0.1111354*(age - 55)/10*(smoking) + \
            0.0008104*(age - 55)/10*(max(bmi, 30) - 30)/5 - \
            0.1666635*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + \
            sdi_term_hf_f + uacr_term_hf + hba1c_term_hf

    else: # Masculino
        uacr_term_cvd = 0.1095674 if math.isnan(log_uacr) else 0.1772853*log_uacr
        uacr_term_ascvd = 0.0652944 if math.isnan(log_uacr) else 0.1375837*log_uacr
        uacr_term_hf = 0.1702805 if math.isnan(log_uacr) else 0.2164607*log_uacr
        hba1c_term_cvd = -0.0230072 if math.isnan(hba1c_val) else (0.1165698*(hba1c_val-5.3)*(dm) + 0.1048297*(hba1c_val-5.3)*(1 - dm))
        hba1c_term_ascvd = -0.0112852 if math.isnan(hba1c_val) else (0.101282*(hba1c_val-5.3)*(dm) + 0.1092726*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0234637 if math.isnan(hba1c_val) else (0.148297*(hba1c_val-5.3)*(dm) + 0.1234088*(hba1c_val-5.3)*(1-dm))
        
        logor_10yr_CVD = -3.631387 + 0.7847578*((age - 55)/10) + \
            0.0534485*(mmol_conversion_py(tc - hdl) - 3.5) - \
            0.0911282*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.4921973*(min(sbp, 110) - 110)/20 + 0.2972415*(max(sbp, 110) - 130)/20 + \
            0.4527054*(dm) + 0.3726641*(smoking) + \
            0.3886854*(min(egfr, 60) - 60)/(-15) + 0.0081661*(max(egfr, 60) - 90)/(-15) + \
            0.2508052*(bptreat) - 0.1538484*(statin) - \
            0.0474695*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1415382*(statin)*(mmol_conversion_py(tc - hdl) - 3.5) - \
            0.0436455*(age - 55)/10*(mmol_conversion_py(tc - hdl) - 3.5) + \
            0.0199549*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.1022686*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.1762507*(age - 55)/10*(dm) - 0.0715873*(age - 55)/10*(smoking) - \
            0.1428668*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + \
            sdi_term_cvd_m + uacr_term_cvd + hba1c_term_cvd
        
        logor_10yr_ASCVD = -3.969788 + 0.7128741*((age - 55)/10) + \
            0.1465201*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.1125794*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.3387216*(min(sbp, 110) - 110)/20 + 0.2980252*(max(sbp, 110) - 130)/20 + \
            0.399583*(dm) + 0.3379111*(smoking) + \
            0.2582604*(min(egfr, 60) - 60)/(-15) + 0.0147769*(max(egfr, 60) - 90)/(-15) + \
            0.1686621*(bptreat) - 0.1073619*(statin) - \
            0.0381038*(bptreat)*(max(sbp, 110) - 130)/20 + \
            0.1034169*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - \
            0.0228755*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + \
            0.0267453*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - \
            0.0897449*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.1497464*(age - 55)/10*(dm) - 0.077206*(age - 55)/10*(smoking) - \
            0.1198368*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + \
            sdi_term_ascvd_m + uacr_term_ascvd + hba1c_term_ascvd

        logor_10yr_HF = -4.663513 + 0.9095703*((age - 55)/10) - \
            0.6765184*(min(sbp, 110) - 110)/20 + 0.3111651*(max(sbp, 110) - 130)/20 + \
            0.5535052*(dm) + 0.4326811*(smoking) - \
            0.0854286*(min(bmi, 30) - 25)/5 + 0.3551736*(max(bmi, 30) - 30)/5 + \
            0.5102245*(min(egfr, 60) - 60)/(-15) + 0.015472*(max(egfr, 60) - 90)/(-15) + \
            0.2570964*(bptreat) - 0.0591177*(bptreat)*(max(sbp, 110) - 130)/20 - \
            0.1219056*(age - 55)/10*(max(sbp, 110) - 130)/20 - \
            0.2437577*(age - 55)/10*(dm) - 0.105363*(age - 55)/10*(smoking) + \
            0.0037907*(age - 55)/10*(max(bmi, 30) - 30)/5 - \
            0.1660207*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + \
            sdi_term_hf_m + uacr_term_hf + hba1c_term_hf
    
    return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

# --- FUNÇÃO HELPER (Comum a todos) ---
def calcular_riscos_finais(logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF, age, tc, hdl, statin, bmi):
    
    def inv_logit(logor):
        if math.isnan(logor):
            return np.nan
        return 100 * math.exp(logor) / (1 + math.exp(logor))

    prevent_10yr_CVD = inv_logit(logor_10yr_CVD)
    prevent_10yr_ASCVD = inv_logit(logor_10yr_ASCVD)
    prevent_10yr_HF = inv_logit(logor_10yr_HF)
    
    # --- Aplicar Regras de Validação (do código R) ---
    if (tc is None or tc < 130 or tc > 320) or \
       (hdl is None or hdl < 20 or hdl > 100) or \
       (statin is None):
        prevent_10yr_CVD = np.nan
        prevent_10yr_ASCVD = np.nan

    if (bmi is None or bmi < 18.5 or bmi >= 40):
        prevent_10yr_HF = np.nan
        
    return prevent_10yr_CVD, prevent_10yr_ASCVD, prevent_10yr_HF

# --- INTERFACE GRÁFICA DA PÁGINA PREVENT ---
def pagina_prevent():
    st.title("Calculadora de Risco PREVENT™ da AHA")
    st.markdown("""
    Esta calculadora implementa os modelos PREVENT da American Heart Association.
    Ela estima o risco de 10 anos para **Doença Cardiovascular Total (DCV)**, 
    Doença Cardiovascular Aterosclerótica (ASCVD) e Insuficiência Cardíaca (IC).
    Destina-se a adultos de 30 a 79 anos sem DCV conhecida.
    """)

    col1, col2 = st.columns(2)
    modelo_utilizado = "" # Variável para mostrar qual modelo foi usado

    with col1:
        st.subheader("Parâmetros do Paciente")
        
        # --- REMOVIDO O st.form ---
        
        sexo_str = st.radio("Sexo Biológico", ["Feminino", "Masculino"], horizontal=True, key="sex")
        age = st.number_input("Idade (anos)", min_value=30, max_value=79, value=55, step=1, key="age")
        bmi = st.number_input("Índice de Massa Corporal (IMC) (kg/m²)", min_value=15.0, max_value=60.0, value=25.0, step=0.1, format="%.1f", key="bmi")
        tc = st.number_input("Colesterol Total (mg/dL)", min_value=100, max_value=400, value=200, step=1, key="tc")
        hdl = st.number_input("Colesterol HDL (mg/dL)", min_value=15, max_value=150, value=50, step=1, key="hdl")
        sbp = st.number_input("Pressão Arterial Sistólica (PAS) (mm Hg)", min_value=80, max_value=250, value=120, step=1, key="sbp")
        egfr = st.number_input("Taxa de Filtração Glomerular (eGFR) (mL/min/1.73 m²)", min_value=10, max_value=150, value=90, step=1, key="egfr")
        
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            dm_bool = st.checkbox("Diabetes Mellitus?", value=False, key="dm")
            smoking_bool = st.checkbox("Fumante atual?", value=False, key="smoking")
        with c2:
            bptreat_bool = st.checkbox("Em uso de anti-hipertensivo?", value=False, key="bptreat")
            statin_bool = st.checkbox("Em uso de estatina?", value=False, key="statin")
        
        st.divider()

        with st.expander("Parâmetros Opcionais (para refinar o risco)"):
            st.info("O modelo de cálculo será ajustado com base nos parâmetros que você fornecer.")
            
            use_uacr = st.checkbox("Informar RAC (UACR)?", key="use_uacr")
            uacr_val_input = st.number_input("Relação Albumina/Creatinina Urinária (RAC) (mg/g)", 
                                       min_value=0.0, max_value=5000.0, value=10.0, step=0.1, format="%.1f",
                                       disabled=not use_uacr, key="uacr_val")

            use_hba1c = st.checkbox("Informar Hemoglobina Glicada (HbA1c)?", key="use_hba1c")
            hba1c_val_input = st.number_input("Hemoglobina Glicada (HbA1c) (%)", 
                                        min_value=3.0, max_value=20.0, value=5.7, step=0.1, format="%.1f",
                                        disabled=not use_hba1c, key="hba1c_val")
        
        # --- REMOVIDO O submit_button ---

    # --- LÓGICA DE SELEÇÃO E EXIBIÇÃO ---
    # Esta parte agora roda a cada mudança de widget
    with col2:
        st.subheader("Resultados do Risco em 10 Anos")

        sex_numeric = 1 if sexo_str == "Feminino" else 0
        dm_numeric = 1 if dm_bool else 0
        smoking_numeric = 1 if smoking_bool else 0
        bptreat_numeric = 1 if bptreat_bool else 0
        statin_numeric = 1 if statin_bool else 0

        # --- LÓGICA DE SELEÇÃO DO MODELO (CORRIGIDA) ---
        uacr_fornecido = use_uacr
        hba1c_fornecido = use_hba1c
        
        uacr_a_passar = uacr_val_input if uacr_fornecido else None
        hba1c_a_passar = hba1c_val_input if hba1c_fornecido else None

        logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = np.nan, np.nan, np.nan

        if not uacr_fornecido and not hba1c_fornecido:
            modelo_utilizado = "Modelo 'Base' utilizado."
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_base_py(
                sex=sex_numeric, age=age, tc=tc, hdl=hdl, sbp=sbp, dm=dm_numeric, 
                smoking=smoking_numeric, bmi=bmi, egfr=egfr, bptreat=bptreat_numeric, 
                statin=statin_numeric
            )
        
        elif uacr_fornecido and not hba1c_fornecido:
            modelo_utilizado = "Modelo 'Base + RAC (UACR)' utilizado."
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_uacr_py(
                sex=sex_numeric, age=age, tc=tc, hdl=hdl, sbp=sbp, dm=dm_numeric, 
                smoking=smoking_numeric, bmi=bmi, egfr=egfr, bptreat=bptreat_numeric, 
                statin=statin_numeric, uacr=uacr_a_passar
            )

        elif not uacr_fornecido and hba1c_fornecido:
            modelo_utilizado = "Modelo 'Base + HbA1c' utilizado."
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_hba1c_py(
                sex=sex_numeric, age=age, tc=tc, hdl=hdl, sbp=sbp, dm=dm_numeric, 
                smoking=smoking_numeric, bmi=bmi, egfr=egfr, bptreat=bptreat_numeric, 
                statin=statin_numeric, hba1c=hba1c_a_passar
            )
        
        else: # (uacr_fornecido AND hba1c_fornecido)
            modelo_utilizado = "Modelo 'Full' (RAC + HbA1c) utilizado."
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_full_py(
                sex=sex_numeric, age=age, tc=tc, hdl=hdl, sbp=sbp, dm=dm_numeric, 
                smoking=smoking_numeric, bmi=bmi, egfr=egfr, bptreat=bptreat_numeric, 
                statin=statin_numeric, uacr=uacr_a_passar, hba1c=hba1c_a_passar
            )

        risco_dcv_total, risco_ascvd, risco_hf = calcular_riscos_finais(
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF,
            age, tc, hdl, statin_numeric, bmi
        )
        
        def formatar_risco(risco):
            if risco is None or math.isnan(risco):
                return "N/A"
            return f"{risco:.1f}%"

        st.metric("Risco de DCV Total", formatar_risco(risco_dcv_total))
        st.metric("Risco de ASCVD", formatar_risco(risco_ascvd))
        st.metric("Risco de Insuficiência Cardíaca", formatar_risco(risco_hf))
        st.caption(modelo_utilizado)
        
        if math.isnan(risco_dcv_total) or math.isnan(risco_hf):
            st.warning("Um ou mais riscos são 'N/A' devido a dados de entrada ausentes ou fora do intervalo (ex: Colesterol/Estatinas são necessários para DCV/ASCVD; IMC é necessário para IC).")

        st.divider()

        st.markdown("#### Interpretação do Risco (DCV Total)")
        if risco_dcv_total is not None and not math.isnan(risco_dcv_total):
            if risco_dcv_total < 5:
                st.success("Risco Baixo: < 5%")
            elif risco_dcv_total < 7.5:
                st.info("Risco Limítrofe: 5% a 7.4%")
            elif risco_dcv_total < 20:
                st.warning("Risco Intermediário: 7.5% a 19.9%")
            else:
                st.error("Risco Alto: ≥ 20%")
        else:
            st.info("Interpretação indisponível.")

# --- FIM: SEÇÃO DA CALCULADORA PREVENT ---


# --- INÍCIO: SEÇÃO DA CALCULADORA MELD 3.0 ---
def pagina_meld():
    st.title("Calculadora MELD 3.0")
    st.info("Em breve...")
# --- FIM: SEÇÃO DA CALCULADORA MELD 3.0 ---


# --- FUNÇÃO PRINCIPAL DA PLATAFORMA (GERENCIADOR DE PÁGINAS) ---
def main():
    st.set_page_config(layout="wide", page_title="Calculadoras Médicas")
    
    st.sidebar.title("Plataforma de Scores 🩺")
    st.sidebar.markdown("---")
    
    paginas = {
        "Risco Cardiovascular (PREVENT)": pagina_prevent,
        "MELD 3.0": pagina_meld,
    }
    
    selecao = st.sidebar.radio("Selecione a Calculadora:", list(paginas.keys()))
    
    pagina_selecionada = paginas[selecao]
    pagina_selecionada()

if __name__ == "__main__":
    main()
