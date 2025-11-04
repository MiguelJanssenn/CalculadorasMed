import streamlit as st
import math
import numpy as np

# --- 1. FUNÇÕES DE CÁLCULO (LÓGICA) ---
# Todas as nossas funções de cálculo puras (sem UI) ficam aqui.

# --- FUNÇÕES AUXILIARES PREVENT ---
def mmol_conversion_py(cholesterol):
    if cholesterol is None or math.isnan(cholesterol): return np.nan
    return 0.02586 * cholesterol

def adjust_py(uacr):
    if uacr is None or math.isnan(uacr): return np.nan
    if uacr >= 0.1: return uacr
    elif 0 <= uacr < 0.1: return 0.1
    return np.nan

# --- FUNÇÕES DE CÁLCULO PREVENT ---
def calcular_prevent_base_py(sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin):
    """ Porta da função 'pred_risk_base' do R """
    logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
    if sex == 1: # Feminino
        logor_10yr_CVD = -3.307728 + 0.7939329*(age - 55)/10 + 0.0305239*(mmol_conversion_py(tc - hdl) - 3.5) - 0.1606857*(mmol_conversion_py(hdl) - 1.3)/(0.3) - 0.2394003*(min(sbp, 110) - 110)/20 + 0.360078*(max(sbp, 110) - 130)/20 + 0.8667604*(dm) + 0.5360739*(smoking) + 0.6045917*(min(egfr, 60) - 60)/(-15) + 0.0433769*(max(egfr, 60) - 90)/(-15) + 0.3151672*(bptreat) - 0.1477655*(statin) - 0.0663612*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1197879*(statin)*(mmol_conversion_py(tc - hdl) - 3.5) - 0.0819715*(age - 55)/10*(mmol_conversion_py(tc - hdl) - 3.5) + 0.0306769*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/(0.3) - 0.0946348*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.27057*(age - 55)/10*(dm) - 0.078715*(age - 55)/10*(smoking) - 0.1637806*(age - 55)/10*(min(egfr, 60) - 60)/(-15)
        logor_10yr_ASCVD = -3.819975 + 0.719883*(age - 55)/10 + 0.1176967*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.151185*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0835358*(min(sbp, 110) - 110)/20 + 0.3592852*(max(sbp, 110) - 130)/20 + 0.8348585*(dm) + 0.4831078*(smoking) + 0.4864619*(min(egfr, 60) - 60)/(-15) + 0.0397779*(max(egfr, 60)  - 90)/(-15) + 0.2265309*(bptreat) - 0.0592374*(statin) - 0.0395762*(bptreat)*(max(sbp, 110) - 130)/20  + 0.0844423*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0567839*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0325692*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.1035985*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2417542*(age - 55)/10*(dm) - 0.0791142*(age - 55)/10*(smoking) - 0.1671492*(age - 55)/10*(min(egfr, 60) - 60)/(-15)
        logor_10yr_HF = -4.310409 + 0.8998235*(age - 55)/10 - 0.4559771*(min(sbp, 110) - 110)/20 + 0.3576505*(max(sbp, 110) - 130)/20 + 1.038346*(dm) + 0.583916*(smoking) - 0.0072294*(min(bmi, 30) - 25)/5 + 0.2997706*(max(bmi, 30) - 30)/5 + 0.7451638*(min(egfr, 60) - 60)/(-15) + 0.0557087*(max(egfr, 60)  - 90)/(-15) + 0.3534442*(bptreat) - 0.0981511*(bptreat)*(max(sbp, 110) - 130)/20  - 0.0946663*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.3581041*(age - 55)/10*(dm) - 0.1159453*(age - 55)/10*(smoking) - 0.003878*(age - 55)/10*(max(bmi, 30) - 30)/5 - 0.1884289*(age - 55)/10*(min(egfr, 60) - 60)/(-15)
    else: # Masculino
        logor_10yr_CVD = -3.031168 + 0.7688528*(age - 55)/10 + 0.0736174*(mmol_conversion_py(tc - hdl) - 3.5) - 0.0954431*(mmol_conversion_py(hdl) - 1.3)/(0.3) - 0.4347345*(min(sbp, 110) - 110)/20 + 0.3362658*(max(sbp, 110) - 130)/20 + 0.7692857*(dm) + 0.4386871*(smoking) + 0.5378979*(min(egfr, 60) - 60)/(-15) + 0.0164827*(max(egfr, 60) - 90)/(-15) + 0.288879*(bptreat) - 0.1337349*(statin) - 0.0475924*(bptreat)*(max(sbp, 110) - 130)/20 + 0.150273*(statin)*(mmol_conversion_py(tc - hdl) - 3.5) - 0.0517874*(age - 55)/10*(mmol_conversion_py(tc - hdl) - 3.5) + 0.0191169*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/(0.3) - 0.1049477*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2251948*(age - 55)/10*(dm) - 0.0895067*(age - 55)/10*(smoking) - 0.1543702*(age - 55)/10*(min(egfr, 60) - 60)/(-15)
        logor_10yr_ASCVD = -3.500655 + 0.7099847*(age - 55)/10 + 0.1658663*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1144285*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2837212*(min(sbp, 110) - 110)/20 + 0.3239977*(max(sbp, 110) - 130)/20 + 0.7189597*(dm) + 0.3956973*(smoking) + 0.3690075*(min(egfr, 60) - 60)/(-15) + 0.0203619*(max(egfr, 60)  - 90)/(-15) + 0.2036522*(bptreat) - 0.0865581*(statin) - 0.0322916*(bptreat)*(max(sbp, 110) - 130)/20 + 0.114563*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0300005*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0232747*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0927024*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2018525*(age - 55)/10*(dm) - 0.0970527*(age - 55)/10*(smoking) - 0.1217081*(age - 55)/10*(min(egfr, 60) - 60)/(-15)
        logor_10yr_HF = -3.946391 + 0.8972642*(age - 55)/10 - 0.6811466*(min(sbp, 110) - 110)/20 + 0.3634461*(max(sbp, 110) - 130)/20 + 0.923776*(dm) + 0.5023736*(smoking) - 0.0485841*(min(bmi, 30) - 25)/5 + 0.3726929*(max(bmi, 30) - 30)/5 + 0.6926917*(min(egfr, 60) - 60)/(-15) + 0.0251827*(max(egfr, 60)  - 90)/(-15) + 0.2980922*(bptreat) - 0.0497731*(bptreat)*(max(sbp, 110) - 130)/20 - 0.1289201*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.3040924*(age - 55)/10*(dm) - 0.1401688*(age - 55)/10*(smoking) + 0.0068126*(age - 55)/10*(max(bmi, 30) - 30)/5 - 0.1797778*(age - 55)/10*(min(egfr, 60) - 60)/(-15)
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
        logor_10yr_CVD = -3.738341 + 0.7969249*((age - 55)/10) + 0.0256635*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1588107*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2255701*(min(sbp, 110) - 110)/20 + 0.3396649*(max(sbp, 110) - 130)/20 + 0.8047515*(dm) + 0.5285338*(smoking) + 0.4803511*(min(egfr, 60) - 60)/(-15) + 0.0434472*(max(egfr, 60) - 90)/(-15) + 0.2985207*(bptreat) - 0.1497787*(statin) - 0.0742889*(bptreat)*(max(sbp, 110) - 130)/20 + 0.106756*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0778126*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0306768*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0907168*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2705122*(age - 55)/10*(dm) - 0.0830564*(age - 55)/10*(smoking) - 0.1389249*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_cvd
        logor_10yr_ASCVD = -4.174614 + 0.7201999*((age - 55)/10) + 0.1135771*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1493506*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0726677*(min(sbp, 110) - 110)/20 + 0.3436259*(max(sbp, 110) - 130)/20 + 0.7773094*(dm) + 0.4746662*(smoking) + 0.3824646*(min(egfr, 60) - 60)/(-15) + 0.0394178*(max(egfr, 60) - 90)/(-15) + 0.2125182*(bptreat) - 0.0603046*(statin) - 0.0466053*(bptreat)*(max(sbp, 110) - 130)/20 + 0.0733118*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0534262*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0325689*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0999887*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2411762*(age - 55)/10*(dm) - 0.0826941*(age - 55)/10*(smoking) - 0.1444737*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_ascvd
        logor_10yr_HF = -4.841506 + 0.9145975*((age - 55)/10) - 0.4441346*(min(sbp, 110) - 110)/20 + 0.3260323*(max(sbp, 110) - 130)/20 + 0.9611365*(dm) + 0.5755787*(smoking) + 0.0008831*(min(bmi, 30) - 25)/5 + 0.2988964*(max(bmi, 30) - 30)/5 + 0.5915291*(min(egfr, 60) - 60)/(-15) + 0.0556823*(max(egfr, 60) - 90)/(-15) + 0.3314097*(bptreat) - 0.1078596*(bptreat)*(max(sbp, 110) - 130)/20 - 0.0875231*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.356859*(age - 55)/10*(dm) - 0.1220248*(age - 55)/10*(smoking) - 0.0053637*(age - 55)/10*(max(bmi, 30) - 30)/5 - 0.1610389*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_hf
    else: # Masculino
        uacr_term_cvd = 0.0916979 if math.isnan(log_uacr) else 0.1887974*log_uacr
        uacr_term_ascvd = 0.0556 if math.isnan(log_uacr) else 0.1510073*log_uacr
        uacr_term_hf = 0.1472194 if math.isnan(log_uacr) else 0.2306299*log_uacr
        logor_10yr_CVD = -3.510705 + 0.7768655*((age - 55)/10) + 0.0659949*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0951111*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.420667*(min(sbp, 110) - 110)/20 + 0.3120151*(max(sbp, 110) - 130)/20 + 0.698521*(dm) + 0.4314669*(smoking) + 0.3841364*(min(egfr, 60) - 60)/(-15) + 0.009384*(max(egfr, 60) - 90)/(-15) + 0.2676494*(bptreat) - 0.1390966*(statin) - 0.0579315*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1383719*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0488332*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0200406*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.102454*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2236355*(age - 55)/10*(dm) - 0.089485*(age - 55)/10*(smoking) - 0.1321848*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_cvd
        logor_10yr_ASCVD = -3.85146 + 0.7141718*((age - 55)/10) + 0.1602194*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1139086*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2719456*(min(sbp, 110) - 110)/20 + 0.3058719*(max(sbp, 110) - 130)/20 + 0.6600631*(dm) + 0.3884022*(smoking) + 0.2466316*(min(egfr, 60) - 60)/(-15) + 0.0151852*(max(egfr, 60) - 90)/(-15) + 0.186167*(bptreat) - 0.0894395*(statin) - 0.0411884*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1058212*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.028089*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0240427*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0912325*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2004894*(age - 55)/10*(dm) - 0.096936*(age - 55)/10*(smoking) - 0.1022867*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_ascvd
        logor_10yr_HF = -4.556907 + 0.9111795*((age - 55)/10) - 0.6693649*(min(sbp, 110) - 110)/20 + 0.3290082*(max(sbp, 110) - 130)/20 + 0.8377655*(dm) + 0.4978917*(smoking) - 0.042749*(min(bmi, 30) - 25)/5 + 0.3624165*(max(bmi, 30) - 30)/5 + 0.5075796*(min(egfr, 60) - 60)/(-15) + 0.0137716*(max(egfr, 60) - 90)/(-15) + 0.2739963*(bptreat) - 0.0645712*(bptreat)*(max(sbp, 110) - 130)/20 - 0.1230039*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.3013297*(age - 55)/10*(dm) - 0.1410318*(age - 55)/10*(smoking) + 0.0021531*(age - 55)/10*(max(bmi, 30) - 30)/5 - 0.1548018*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + uacr_term_hf
    return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

def calcular_prevent_hba1c_py(sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, hba1c):
    """ Porta da função 'pred_risk_hba1c' do R """
    logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
    hba1c_val = hba1c if (hba1c is not None and not math.isnan(hba1c)) else np.nan
    if sex == 1: # Feminino
        hba1c_term_cvd = -0.0142496 if math.isnan(hba1c_val) else (0.1338348*(hba1c_val-5.3)*(dm) + 0.1622409*(hba1c_val-5.3)*(1-dm))
        hba1c_term_ascvd = 0.0015678 if math.isnan(hba1c_val) else (0.1339055*(hba1c_val-5.3)*(dm) + 0.1596461*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0143112 if math.isnan(hba1c_val) else (0.1856442*(hba1c_val-5.3)*(dm) + 0.1833083*(hba1c_val-5.3)*(1-dm))
        logor_10yr_CVD = -3.306162 + 0.7858178*((age - 55)/10) + 0.0194438*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1521964*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2296681*(min(sbp, 110) - 110)/20 + 0.3465777*(max(sbp, 110) - 130)/20 + 0.5366241*(dm) + 0.5411682*(smoking) + 0.5931898*(min(egfr, 60) - 60)/(-15) + 0.0472458*(max(egfr, 60) - 90)/(-15) + 0.3158567*(bptreat) - 0.1535174*(statin) - 0.0687752*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1054746*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0761119*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0307469*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0905966*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2241857*(age - 55)/10*(dm) - 0.080186*(age - 55)/10*(smoking) - 0.1667286*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_cvd
        logor_10yr_ASCVD = -3.838746 + 0.7111831*((age - 55)/10) + 0.106797*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1425745*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0736824*(min(sbp, 110) - 110)/20 + 0.3480844*(max(sbp, 110) - 130)/20 + 0.5112951*(dm) + 0.4880292*(smoking) + 0.4754997*(min(egfr, 60) - 60)/(-15) + 0.0438132*(max(egfr, 60) - 90)/(-15) + 0.2259093*(bptreat) - 0.0648872*(statin) - 0.0437645*(bptreat)*(max(sbp, 110) - 130)/20 + 0.0697082*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0506382*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0327475*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0996442*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.1924338*(age - 55)/10*(dm) - 0.0803539*(age - 55)/10*(smoking) - 0.1682586*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_ascvd
        logor_10yr_HF = -4.288225 + 0.8997391*((age - 55)/10) - 0.4422749*(min(sbp, 110) - 110)/20 + 0.3378691*(max(sbp, 110) - 130)/20 + 0.681284*(dm) + 0.5886005*(smoking) - 0.0148657*(min(bmi, 30) - 25)/5 + 0.2958374*(max(bmi, 30) - 30)/5 + 0.73447*(min(egfr, 60) - 60)/(-15) + 0.05926*(max(egfr, 60) - 90)/(-15) + 0.3543475*(bptreat) - 0.1002139*(bptreat)*(max(sbp, 110) - 130)/20 - 0.0878765*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.303684*(age - 55)/10*(dm) - 0.1178943*(age - 55)/10*(smoking) - 0.008345*(age - 55)/10*(max(bmi, 30) - 30)/5 - 0.1912183*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_hf
    else: # Masculino
        hba1c_term_cvd = -0.0128373 if math.isnan(hba1c_val) else (0.13159*(hba1c_val-5.3)*(dm) + 0.1295185*(hba1c_val-5.3)*(1-dm))
        hba1c_term_ascvd = -0.0010001 if math.isnan(hba1c_val) else (0.1157161*(hba1c_val-5.3)*(dm) + 0.1288303*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0113444 if math.isnan(hba1c_val) else (0.1652857*(hba1c_val-5.3)*(dm) + 0.1505859*(hba1c_val-5.3)*(1-dm))
        logor_10yr_CVD = -3.040901 + 0.7699177*((age - 55)/10) + 0.0605093*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0888525*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.417713*(min(sbp, 110) - 110)/20 + 0.3288657*(max(sbp, 110) - 130)/20 + 0.4759471*(dm) + 0.4385663*(smoking) + 0.5334616*(min(egfr, 60) - 60)/(-15) + 0.0206431*(max(egfr, 60) - 90)/(-15) + 0.2917524*(bptreat) - 0.1383313*(statin) - 0.0482622*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1393796*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0463501*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0205926*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.1037717*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.1737697*(age - 55)/10*(dm) - 0.0915839*(age - 55)/10*(smoking) - 0.1637039*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_cvd
        logor_10yr_ASCVD = -3.51835 + 0.7064146*((age - 55)/10) + 0.1532267*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1082166*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2675288*(min(sbp, 110) - 110)/20 + 0.3173809*(max(sbp, 110) - 130)/20 + 0.432604*(dm) + 0.3958842*(smoking) + 0.3665014*(min(egfr, 60) - 60)/(-15) + 0.0250243*(max(egfr, 60) - 90)/(-15) + 0.2061158*(bptreat) - 0.0899988*(statin) - 0.0334959*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1034168*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0255406*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0247538*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0917441*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.1499195*(age - 55)/10*(dm) - 0.098089*(age - 55)/10*(smoking) - 0.1305231*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_ascvd
        logor_10yr_HF = -3.961954 + 0.911787*((age - 55)/10) - 0.6568071*(min(sbp, 110) - 110)/20 + 0.3524645*(max(sbp, 110) - 130)/20 + 0.5849752*(dm) + 0.5014014*(smoking) - 0.0512352*(min(bmi, 30) - 25)/5 + 0.365294*(max(bmi, 30) - 30)/5 + 0.6892219*(min(egfr, 60) - 60)/(-15) + 0.0292377*(max(egfr, 60) - 90)/(-15) + 0.3038296*(bptreat) - 0.0515032*(bptreat)*(max(sbp, 110) - 130)/20 - 0.1262343*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2449514*(age - 55)/10*(dm) - 0.1392217*(age - 55)/10*(smoking) + 0.0009592*(age - 55)/10*(max(bmi, 30) - 30)/5 - 0.1917105*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + hba1c_term_hf
    return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

def calcular_prevent_full_py(sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, uacr, hba1c):
    """ Porta da função 'pred_risk_full' do R, SEM SDI """
    logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
    adj_uacr = adjust_py(uacr)
    log_uacr = math.log(adj_uacr) if not math.isnan(adj_uacr) else np.nan
    hba1c_val = hba1c if (hba1c is not None and not math.isnan(hba1c)) else np.nan
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
        logor_10yr_CVD = -3.860385 + 0.7716794*((age - 55)/10) + 0.0062109*(mmol_conversion_py(tc - hdl) - 3.5) - 0.1547756*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.1933123*(min(sbp, 110) - 110)/20 + 0.3071217*(max(sbp, 110) - 130)/20 + 0.496753*(dm) + 0.466605*(smoking) + 0.4780697*(min(egfr, 60) - 60)/(-15) + 0.0529077*(max(egfr, 60) - 90)/(-15) + 0.3034892*(bptreat) - 0.1556524*(statin) - 0.0667026*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1061825*(statin)*(mmol_conversion_py(tc - hdl) - 3.5) - 0.0742271*(age - 55)/10*(mmol_conversion_py(tc - hdl) - 3.5) + 0.0288245*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0875188*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2267102*(age - 55)/10*(dm) - 0.0676125*(age - 55)/10*(smoking) - 0.1493231*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + sdi_term_cvd_f + uacr_term_cvd + hba1c_term_cvd
        logor_10yr_ASCVD = -4.291503 + 0.7023067*((age - 55)/10) + 0.0898765*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1407316*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0256648*(min(sbp, 110) - 110)/20 + 0.314511*(max(sbp, 110) - 130)/20 + 0.4799217*(dm) + 0.4062049*(smoking) + 0.3847744*(min(egfr, 60) - 60)/(-15) + 0.0495174*(max(egfr, 60) - 90)/(-15) + 0.2133861*(bptreat) - 0.0678552*(statin) - 0.0451416*(bptreat)*(max(sbp, 110) - 130)/20 + 0.0788187*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0535985*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0291762*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0961839*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2001466*(age - 55)/10*(dm) - 0.0586472*(age - 55)/10*(smoking) - 0.1537791*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + sdi_term_ascvd_f + uacr_term_ascvd + hba1c_term_ascvd
        logor_10yr_HF = -4.896524 + 0.884209*((age - 55)/10) - 0.421474*(min(sbp, 110) - 110)/20 + 0.3002919*(max(sbp, 110) - 130)/20 + 0.6170359*(dm) + 0.5380269*(smoking) - 0.0191335*(min(bmi, 30) - 25)/5 + 0.2764302*(max(bmi, 30) - 30)/5 + 0.5975847*(min(egfr, 60) - 60)/(-15) + 0.0654197*(max(egfr, 60) - 90)/(-15) + 0.3313614*(bptreat) - 0.1002304*(bptreat)*(max(sbp, 110) - 130)/20 - 0.0845363*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2989062*(age - 55)/10*(dm) - 0.1111354*(age - 55)/10*(smoking) + 0.0008104*(age - 55)/10*(max(bmi, 30) - 30)/5 - 0.1666635*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + sdi_term_hf_f + uacr_term_hf + hba1c_term_hf
    else: # Masculino
        uacr_term_cvd = 0.1095674 if math.isnan(log_uacr) else 0.1772853*log_uacr
        uacr_term_ascvd = 0.0652944 if math.isnan(log_uacr) else 0.1375837*log_uacr
        uacr_term_hf = 0.1702805 if math.isnan(log_uacr) else 0.2164607*log_uacr
        hba1c_term_cvd = -0.0230072 if math.isnan(hba1c_val) else (0.1165698*(hba1c_val-5.3)*(dm) + 0.1048297*(hba1c_val-5.3)*(1 - dm))
        hba1c_term_ascvd = -0.0112852 if math.isnan(hba1c_val) else (0.101282*(hba1c_val-5.3)*(dm) + 0.1092726*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0234637 if math.isnan(hba1c_val) else (0.148297*(hba1c_val-5.3)*(dm) + 0.1234088*(hba1c_val-5.3)*(1-dm))
        logor_10yr_CVD = -3.631387 + 0.7847578*((age - 55)/10) + 0.0534485*(mmol_conversion_py(tc - hdl) - 3.5) - 0.0911282*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.4921973*(min(sbp, 110) - 110)/20 + 0.2972415*(max(sbp, 110) - 130)/20 + 0.4527054*(dm) + 0.3726641*(smoking) + 0.3886854*(min(egfr, 60) - 60)/(-15) + 0.0081661*(max(egfr, 60) - 90)/(-15) + 0.2508052*(bptreat) - 0.1538484*(statin) - 0.0474695*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1415382*(statin)*(mmol_conversion_py(tc - hdl) - 3.5) - 0.0436455*(age - 55)/10*(mmol_conversion_py(tc - hdl) - 3.5) + 0.0199549*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.1022686*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.1762507*(age - 55)/10*(dm) - 0.0715873*(age - 55)/10*(smoking) - 0.1428668*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + sdi_term_cvd_m + uacr_term_cvd + hba1c_term_cvd
        logor_10yr_ASCVD = -3.969788 + 0.7128741*((age - 55)/10) + 0.1465201*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1125794*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.3387216*(min(sbp, 110) - 110)/20 + 0.2980252*(max(sbp, 110) - 130)/20 + 0.399583*(dm) + 0.3379111*(smoking) + 0.2582604*(min(egfr, 60) - 60)/(-15) + 0.0147769*(max(egfr, 60) - 90)/(-15) + 0.1686621*(bptreat) - 0.1073619*(statin) - 0.0381038*(bptreat)*(max(sbp, 110) - 130)/20 + 0.1034169*(statin)*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0228755*(age - 55)/10*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) + 0.0267453*(age - 55)/10*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0897449*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.1497464*(age - 55)/10*(dm) - 0.077206*(age - 55)/10*(smoking) - 0.1198368*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + sdi_term_ascvd_m + uacr_term_ascvd + hba1c_term_ascvd
        logor_10yr_HF = -4.663513 + 0.9095703*((age - 55)/10) - 0.6765184*(min(sbp, 110) - 110)/20 + 0.3111651*(max(sbp, 110) - 130)/20 + 0.5535052*(dm) + 0.4326811*(smoking) - 0.0854286*(min(bmi, 30) - 25)/5 + 0.3551736*(max(bmi, 30) - 30)/5 + 0.5102245*(min(egfr, 60) - 60)/(-15) + 0.015472*(max(egfr, 60) - 90)/(-15) + 0.2570964*(bptreat) - 0.0591177*(bptreat)*(max(sbp, 110) - 130)/20 - 0.1219056*(age - 55)/10*(max(sbp, 110) - 130)/20 - 0.2437577*(age - 55)/10*(dm) - 0.105363*(age - 55)/10*(smoking) + 0.0037907*(age - 55)/10*(max(bmi, 30) - 30)/5 - 0.1660207*(age - 55)/10*(min(egfr, 60) - 60)/(-15) + sdi_term_hf_m + uacr_term_hf + hba1c_term_hf
    return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

def calcular_riscos_finais(logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF, age, tc, hdl, statin, bmi):
    def inv_logit(logor):
        if math.isnan(logor): return np.nan
        return 100 * math.exp(logor) / (1 + math.exp(logor))
    prevent_10yr_CVD = inv_logit(logor_10yr_CVD)
    prevent_10yr_ASCVD = inv_logit(logor_10yr_ASCVD)
    prevent_10yr_HF = inv_logit(logor_10yr_HF)
    if (tc is None or tc < 130 or tc > 320) or \
       (hdl is None or hdl < 20 or hdl > 100) or \
       (statin is None):
        prevent_10yr_CVD = np.nan
        prevent_10yr_ASCVD = np.nan
    if (bmi is None or bmi < 18.5 or bmi >= 40):
        prevent_10yr_HF = np.nan
    return prevent_10yr_CVD, prevent_10yr_ASCVD, prevent_10yr_HF

# --- FUNÇÕES DE CÁLCULO GASTROENTEROLOGIA ---

def calcular_meld_3_0(sex_str, bilirubin, inr, creatinine, sodium, albumin, dialise):
    """ Calcula o score MELD 3.0 """
    # Aplicar limites
    bilirubin = max(1.0, min(bilirubin, 32.0))
    inr = max(1.0, min(inr, 3.5))
    creatinine_calc = max(1.0, min(creatinine, 4.0))
    sodium = max(125.0, min(sodium, 137.0))
    albumin = max(1.5, min(albumin, 3.5))
    
    # Se fez diálise 2x+ nos últimos 7 dias OU Creatinina >= 4.0, a creatinina usada é 4.0
    if dialise or creatinine >= 4.0:
        creatinine_calc = 4.0
    
    sex_female = 1.33 if sex_str == "Feminino" else 0
    
    # Fórmula MELD 3.0
    score = (
        1.33 * sex_female
        + 4.56 * math.log(bilirubin)
        + 0.82 * (137 - sodium)
        - (0.24 * (137 - sodium) * math.log(bilirubin))
        + 9.09 * math.log(inr)
        + 11.14 * math.log(creatinine_calc)
        + 1.85 * (3.5 - albumin)
        - (0.05 * (3.5 - albumin) * math.log(creatinine_calc))
        + 6.0
    )
    
    score = math.floor(score) # Arredonda para baixo
    return min(max(6, score), 40) # O score MELD é limitado entre 6 e 40

def calcular_child_pugh(bilirubin, inr, albumin, ascites, encephalopathy):
    """ Calcula o score Child-Pugh """
    score = 0
    
    # Bilirrubina
    if bilirubin < 2.0: score += 1
    elif 2.0 <= bilirubin <= 3.0: score += 2
    else: score += 3
        
    # INR
    if inr < 1.7: score += 1
    elif 1.7 <= inr <= 2.3: score += 2
    else: score += 3
    
    # Albumina
    if albumin > 3.5: score += 1
    elif 2.8 <= albumin <= 3.5: score += 2
    else: score += 3
        
    # Ascite
    if ascites == "Ausente": score += 1
    elif ascites == "Leve": score += 2
    elif ascites == "Moderada/Grave": score += 3
        
    # Encefalopatia
    if encephalopathy == "Ausente": score += 1
    elif encephalopathy == "Grau 1-2": score += 2
    elif encephalopathy == "Grau 3-4": score += 3
        
    return score

def calcular_fib4(age, ast, alt, platelets):
    """ Calcula o score FIB4 """
    # Fórmula: (Idade * AST) / (Plaquetas * sqrt(ALT))
    if alt <= 0 or platelets <= 0:
        return np.nan
    
    # A fórmula usa plaquetas em 10^9/L. O input é em 10^3/µL, que é o mesmo que 10^9/L.
    score = (age * ast) / (platelets * math.sqrt(alt))
    return score

# --- FUNÇÕES DE CÁLCULO ENDOCRINOLOGIA ---

def calcular_imc(weight, height_cm):
    """ Calcula o Índice de Massa Corporal (IMC) """
    if height_cm is None or height_cm == 0 or weight is None:
        return np.nan
    height_m = height_cm / 100
    imc = weight / (height_m ** 2)
    return imc

def calcular_homa_ir(glucose_mg_dl, insulin):
    """ Calcula o HOMA-IR """
    # Fórmula padrão: (Glicose (mg/dL) * Insulina (µU/mL)) / 405
    score = (glucose_mg_dl * insulin) / 405
    return score

def calcular_homa_beta(glucose_mg_dl, insulin):
    """ Calcula o HOMA-BETA """
    # Fórmula padrão: (360 * Insulina (µU/mL)) / (Glicose (mg/dL) - 63)
    if (glucose_mg_dl - 63) == 0:
        return np.nan
    score = (360 * insulin) / (glucose_mg_dl - 63)
    return score

# --- FUNÇÕES DE CÁLCULO NEFROLOGIA ---
def calcular_egfr_ckd_epi(creatinine, age, sex_str):
    """ Calcula eGFR usando a fórmula CKD-EPI 2021 """
    
    # Parâmetros da fórmula CKD-EPI 2021
    kappa = 0.7 if sex_str == "Feminino" else 0.9
    alpha = -0.241 if sex_str == "Feminino" else -0.302
    sex_factor = 1.012 if sex_str == "Feminino" else 1.0
    
    # Fórmula
    egfr = 142 * (min(creatinine / kappa, 1) ** alpha) * \
                 (max(creatinine / kappa, 1) ** -1.200) * \
                 (0.9938 ** age) * sex_factor
                 
    return egfr

# --- FUNÇÕES UTILITÁRIAS DE FORMATAÇÃO E ESTRATIFICAÇÃO ---
def formatar_risco(risco):
    if risco is None or math.isnan(risco):
        return "N/A"
    return f"{risco:.1f}%"

def formatar_score(score, casas_decimais=1):
    if score is None or math.isnan(score):
        return "N/A"
    return f"{score:.{casas_decimais}f}"

def exibir_interpretacao_prevent(risco_dcv_total):
    st.markdown("#### Interpretação (PREVENT)")
    if risco_dcv_total is not None and not math.isnan(risco_dcv_total):
        if risco_dcv_total < 5:
            st.success(f"**{formatar_risco(risco_dcv_total)}:** Risco Baixo")
        elif risco_dcv_total < 7.5:
            st.info(f"**{formatar_risco(risco_dcv_total)}:** Risco Limítrofe")
        elif risco_dcv_total < 20:
            st.warning(f"**{formatar_risco(risco_dcv_total)}:** Risco Intermediário")
        else:
            st.error(f"**{formatar_risco(risco_dcv_total)}:** Risco Alto")
    else:
        st.info("Interpretação indisponível.")

def exibir_interpretacao_child_pugh(score):
    st.markdown("#### Interpretação (Child-Pugh)")
    if score is None or math.isnan(score):
        st.info("Cálculo indisponível.")
        return

    score = int(score)
    if 5 <= score <= 6:
        st.success(f"**Classe A ({score} pontos):** Doença hepática compensada.")
        st.markdown("*Sobrevida em 1 ano: 100%*")
    elif 7 <= score <= 9:
        st.warning(f"**Classe B ({score} pontos):** Comprometimento funcional significativo.")
        st.markdown("*Sobrevida em 1 ano: 81%*")
    elif 10 <= score <= 15:
        st.error(f"**Classe C ({score} pontos):** Doença hepática descompensada.")
        st.markdown("*Sobrevida em 1 ano: 45%*")

def exibir_interpretacao_meld(score):
    st.markdown("#### Interpretação (Mortalidade em 90 dias)")
    if score is None or math.isnan(score):
        st.info("Cálculo indisponível.")
        return

    score = int(score)
    if score <= 9:
        st.success(f"**Score {score} (≤ 9):** Mortalidade de 1.9%")
    elif 10 <= score <= 19:
        st.info(f"**Score {score} (10-19):** Mortalidade de 6.0%")
    elif 20 <= score <= 29:
        st.warning(f"**Score {score} (20-29):** Mortalidade de 19.6%")
    elif 30 <= score <= 39:
        st.error(f"**Score {score} (30-39):** Mortalidade de 52.6%")
    else: # >= 40
        st.error(f"**Score {score} (≥ 40):** Mortalidade de 71.3%")

def exibir_interpretacao_fib4(score, age):
    st.markdown("#### Interpretação (FIB-4)")
    if score is None or math.isnan(score):
        st.info("Cálculo indisponível.")
        return
    
    low_cutoff = 1.45
    high_cutoff = 3.25
    
    if age is not None and age > 65:
        low_cutoff = 2.0
        
    if score < low_cutoff:
        st.success(f"**Score {score:.2f} (< {low_cutoff}):** Baixo risco de fibrose avançada (VPN > 90%).")
    elif score > high_cutoff:
        st.error(f"**Score {score:.2f} (> {high_cutoff}):** Alto risco de fibrose avançada (VPP > 65%).")
    else:
        st.warning(f"**Score {score:.2f} ({low_cutoff}-{high_cutoff}):** Risco indeterminado. Considere avaliação adicional.")

def exibir_interpretacao_imc(score):
    st.markdown("#### Interpretação (IMC - OMS)")
    if score is None or math.isnan(score):
        st.info("Cálculo indisponível.")
        return

    if score < 18.5:
        st.warning(f"**IMC {score:.1f}:** Abaixo do peso")
    elif 18.5 <= score < 25:
        st.success(f"**IMC {score:.1f}:** Peso normal")
    elif 25 <= score < 30:
        st.warning(f"**IMC {score:.1f}:** Sobrepeso")
    elif 30 <= score < 35:
        st.error(f"**IMC {score:.1f}:** Obesidade Grau I")
    elif 35 <= score < 40:
        st.error(f"**IMC {score:.1f}:** Obesidade Grau II")
    else: # >= 40
        st.error(f"**IMC {score:.1f}:** Obesidade Grau III (Mórbida)")

def exibir_interpretacao_homa_ir(score):
    st.markdown("#### Interpretação (HOMA-IR)")
    if score is None or math.isnan(score):
        st.info("Cálculo indisponível.")
        return
    
    if score < 2.0:
        st.success(f"**HOMA-IR {score:.2f}:** Geralmente considerado normal.")
    else:
        st.warning(f"**HOMA-IR {score:.2f}:** Sugestivo de resistência à insulina (Cutoff comum > 2.0).")

def exibir_interpretacao_egfr(score):
    st.markdown("#### Interpretação (Estágios DRC)")
    if score is None or math.isnan(score):
        st.info("Cálculo indisponível.")
        return
        
    score = round(score)
    if score >= 90:
        st.success(f"**eGFR {score}:** Estágio 1 - Normal ou aumentado (≥ 90)")
    elif 60 <= score <= 89:
        st.info(f"**eGFR {score}:** Estágio 2 - Levemente diminuído (60-89)")
    elif 45 <= score <= 59:
        st.warning(f"**eGFR {score}:** Estágio 3a - Leve a moderadamente diminuído (45-59)")
    elif 30 <= score <= 44:
        st.warning(f"**eGFR {score}:** Estágio 3b - Moderada a gravemente diminuído (30-44)")
    elif 15 <= score <= 29:
        st.error(f"**eGFR {score}:** Estágio 4 - Gravemente diminuído (15-29)")
    else: # < 15
        st.error(f"**eGFR {score}:** Estágio 5 - Falência renal (< 15)")
        
def exibir_interpretacao_cat(score):
    st.markdown("#### Interpretação (Impacto da DPOC)")
    if score is None or math.isnan(score):
        st.info("Cálculo indisponível.")
        return
    
    score = int(score)
    if score <= 10:
        st.success(f"**Score {score} (0-10):** Baixo Impacto")
    elif 11 <= score <= 20:
        st.info(f"**Score {score} (11-20):** Médio Impacto")
    elif 21 <= score <= 30:
        st.warning(f"**Score {score} (21-30):** Alto Impacto")
    else: # 31-40
        st.error(f"**Score {score} (31-40):** Muito Alto Impacto")

def exibir_interpretacao_mmrc(score):
    st.markdown("#### Interpretação (Escala de Dispneia)")
    if score is None or math.isnan(score):
        st.info("Cálculo indisponível.")
        return

    score = int(score)
    if score == 0:
        st.success(f"**Grau {score}:** Dispneia apenas com exercício intenso.")
    elif score == 1:
        st.info(f"**Grau {score}:** Dispneia ao andar apressado ou subir ladeira leve.")
    elif score == 2:
        st.warning(f"**Grau {score}:** Anda mais devagar ou precisa parar para respirar.")
    elif score == 3:
        st.error(f"**Grau {score}:** Para para respirar após ~100m.")
    elif score == 4:
        st.error(f"**Grau {score}:** Tanta dispneia que não sai de casa ou sente ao se vestir.")


# --- 2. FUNÇÕES DE PÁGINA (UI) ---
# Estas funções definem a aparência de cada página.

def pagina_dados_paciente():
    """Página de entrada de dados. Escreve em st.session_state."""
    st.title("Prontuário do Paciente")
    st.markdown("Insira os dados do paciente abaixo. Os resultados serão calculados automaticamente nas páginas de especialidade.")

    st.subheader("Dados Demográficos e Vitais")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.radio("Sexo Biológico", ["Feminino", "Masculino"], horizontal=True, key="sex", index=("Feminino", "Masculino").index(st.session_state.sex))
        st.number_input("Idade (anos)", min_value=18, max_value=120, value=st.session_state.age, step=1, key="age", placeholder="Ex: 55")
    with col2:
        st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=st.session_state.weight, step=0.1, format="%.1f", key="weight", placeholder="Ex: 70.0")
        st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=st.session_state.height_cm, step=0.1, format="%.1f", key="height_cm", placeholder="Ex: 170.0")
    with col3:
        st.number_input("Pressão Arterial Sistólica (PAS) (mm Hg)", min_value=80, max_value=250, value=st.session_state.sbp, step=1, key="sbp", placeholder="Ex: 120")

    st.subheader("Exames Laboratoriais")
    
    with st.expander("Painel Geral / Metabólico"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.number_input("Colesterol Total (mg/dL)", min_value=100, max_value=400, value=st.session_state.tc, step=1, key="tc", placeholder="Ex: 200")
            st.number_input("Colesterol HDL (mg/dL)", min_value=15, max_value=150, value=st.session_state.hdl, step=1, key="hdl", placeholder="Ex: 50")
            st.number_input("Glicose de Jejum (mg/dL)", min_value=40, max_value=500, value=st.session_state.glucose_fasting, step=1, key="glucose_fasting", placeholder="Ex: 90")
            st.number_input("Insulina de Jejum (µU/mL)", min_value=1.0, max_value=300.0, value=st.session_state.insulin_fasting, step=0.1, format="%.1f", key="insulin_fasting", placeholder="Ex: 8.0")
        with col2:
            st.number_input("Creatinina Sérica (mg/dL)", min_value=0.1, max_value=20.0, value=st.session_state.creatinine, step=0.1, format="%.1f", key="creatinine", placeholder="Ex: 1.0")
            st.number_input("AST (TGO) (U/L)", min_value=1, max_value=1000, value=st.session_state.ast, step=1, key="ast", placeholder="Ex: 25")
            st.number_input("ALT (TGP) (U/L)", min_value=1, max_value=1000, value=st.session_state.alt, step=1, key="alt", placeholder="Ex: 25")
            st.number_input("Plaquetas (x10³/µL)", min_value=10, max_value=1000, value=st.session_state.platelets, step=1, key="platelets", placeholder="Ex: 250")
        with col3:
            st.number_input("Bilirrubina Total (mg/dL)", min_value=0.1, max_value=50.0, value=st.session_state.bilirubin, step=0.1, format="%.1f", key="bilirubin", placeholder="Ex: 1.2")
            st.number_input("INR", min_value=0.5, max_value=10.0, value=st.session_state.inr, step=0.1, format="%.1f", key="inr", placeholder="Ex: 1.1")
            st.number_input("Sódio Sérico (mEq/L)", min_value=100, max_value=180, value=st.session_state.sodium, step=1, key="sodium", placeholder="Ex: 140")
            st.number_input("Albumina Sérica (g/dL)", min_value=1.0, max_value=6.0, value=st.session_state.albumin, step=0.1, format="%.1f", key="albumin", placeholder="Ex: 4.0")
    
    with st.expander("Painel PREVENT (Opcional)"):
        st.number_input("Relação Albumina/Creatinina Urinária (RAC) (mg/g)", min_value=0.0, max_value=5000.0, value=st.session_state.uacr_val, step=0.1, format="%.1f", key="uacr_val", placeholder="Opcional: Ex: 10.0")
        st.number_input("Hemoglobina Glicada (HbA1c) (%)", min_value=3.0, max_value=20.0, value=st.session_state.hba1c_val, step=0.1, format="%.1f", key="hba1c_val", placeholder="Opcional: Ex: 5.7")


    st.subheader("Histórico Clínico e Questionários")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Comorbidades e Hábitos**")
        st.checkbox("Diabetes Mellitus?", value=st.session_state.dm, key="dm")
        st.checkbox("Fumante atual?", value=st.session_state.smoking, key="smoking")
        st.checkbox("Em uso de anti-hipertensivo?", value=st.session_state.bptreat, key="bptreat")
        st.checkbox("Em uso de estatina?", value=st.session_state.statin, key="statin")
        st.checkbox("Em diálise (2x na última semana)?", value=st.session_state.dialise, key="dialise")
    
    with col2:
        st.markdown("**Sintomas (Gastro/Pneumo)**")
        st.selectbox("Ascite (Child-Pugh)", ["Ausente", "Leve", "Moderada/Grave"], key="ascites", index=["Ausente", "Leve", "Moderada/Grave"].index(st.session_state.ascites))
        st.selectbox("Encefalopatia (Child-Pugh)", ["Ausente", "Grau 1-2", "Grau 3-4"], key="encephalopathy", index=["Ausente", "Grau 1-2", "Grau 3-4"].index(st.session_state.encephalopathy))
        st.selectbox("Dispneia (mMRC)", [
            "Grau 0: Dispneia apenas com exercício intenso",
            "Grau 1: Dispneia ao andar apressado ou subir ladeira leve",
            "Grau 2: Anda mais devagar ou precisa parar para respirar",
            "Grau 3: Para para respirar após ~100m",
            "Grau 4: Tanta dispneia que não sai de casa"
        ], key="mmrc_score", index=["Grau 0: Dispneia apenas com exercício intenso", "Grau 1: Dispneia ao andar apressado ou subir ladeira leve", "Grau 2: Anda mais devagar ou precisa parar para respirar", "Grau 3: Para para respirar após ~100m", "Grau 4: Tanta dispneia que não sai de casa"].index(st.session_state.mmrc_score))

    with col3:
        st.markdown("**Questionário CAT (DPOC)**")
        st.caption("Responda de 0 (Nunca) a 5 (Sempre):")
        st.slider("1. Tusso muito?", 0, 5, value=st.session_state.cat_1, key="cat_1")
        st.slider("2. Tenho muito catarro?", 0, 5, value=st.session_state.cat_2, key="cat_2")
        st.slider("3. Sinto o peito apertado?", 0, 5, value=st.session_state.cat_3, key="cat_3")
        st.slider("4. Sinto falta de ar ao subir escadas?", 0, 5, value=st.session_state.cat_4, key="cat_4")
        st.slider("5. Limitado(a) em casa?", 0, 5, value=st.session_state.cat_5, key="cat_5")
        st.slider("6. Confiante para sair de casa?", 0, 5, value=st.session_state.cat_6, key="cat_6")
        st.slider("7. Durmo profundamente?", 0, 5, value=st.session_state.cat_7, key="cat_7")
        st.slider("8. Tenho muita energia?", 0, 5, value=st.session_state.cat_8, key="cat_8")
        
def pagina_cardiologia():
    """Página de resultados de Cardiologia. Apenas LÊ de st.session_state."""
    st.title("Scores de Cardiologia")
    
    st.header("Risco Cardiovascular (PREVENT)")
    st.markdown("O score PREVENT estima o risco em 10 anos de Doença Cardiovascular Total (DCV), Doença Aterosclerótica (ASCVD) e Insuficiência Cardíaca (IC) em adultos de 30 a 79 anos.")
    
    try:
        # 1. Calcular dependências primeiro
        bmi = calcular_imc(st.session_state.weight, st.session_state.height_cm)
        egfr = calcular_egfr_ckd_epi(st.session_state.creatinine, st.session_state.age, st.session_state.sex)
        
        # 2. Montar o dict de dados
        prevent_data = {
            "sex": 1 if st.session_state.sex == "Feminino" else 0,
            "age": st.session_state.age,
            "tc": st.session_state.tc,
            "hdl": st.session_state.hdl,
            "sbp": st.session_state.sbp,
            "dm": 1 if st.session_state.dm else 0,
            "smoking": 1 if st.session_state.smoking else 0,
            "bmi": bmi, # Usa o IMC calculado
            "egfr": egfr, # Usa o eGFR calculado
            "bptreat": 1 if st.session_state.bptreat else 0,
            "statin": 1 if st.session_state.statin else 0,
            "uacr": st.session_state.uacr_val,
            "hba1c": st.session_state.hba1c_val
        }
        
        # 3. Verificar campos obrigatórios
        required_prevent = [prevent_data[k] for k in ['age', 'tc', 'hdl', 'sbp', 'bmi', 'egfr']]
        if not all(v is not None for v in required_prevent):
            raise TypeError("Campos obrigatórios do PREVENT não preenchidos.")

        # 4. Lógica de seleção de modelo
        uacr_fornecido = prevent_data["uacr"] is not None
        hba1c_fornecido = prevent_data["hba1c"] is not None
        logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = np.nan, np.nan, np.nan
        modelo_utilizado = ""

        if not uacr_fornecido and not hba1c_fornecido:
            modelo_utilizado = "Modelo 'Base' utilizado."
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_base_py(**prevent_data)
        elif uacr_fornecido and not hba1c_fornecido:
            modelo_utilizado = "Modelo 'Base + RAC (UACR)' utilizado."
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_uacr_py(**prevent_data)
        elif not uacr_fornecido and hba1c_fornecido:
            modelo_utilizado = "Modelo 'Base + HbA1c' utilizado."
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_hba1c_py(**prevent_data)
        else:
            modelo_utilizado = "Modelo 'Full' (RAC + HbA1c) utilizado."
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_full_py(**prevent_data)

        # 5. Calcular e exibir
        risco_dcv_total, risco_ascvd, risco_hf = calcular_riscos_finais(
            logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF,
            prevent_data['age'], prevent_data['tc'], prevent_data['hdl'], prevent_data['statin'], prevent_data['bmi']
        )
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Risco de DCV Total", formatar_risco(risco_dcv_total))
        col2.metric("Risco de ASCVD", formatar_risco(risco_ascvd))
        col3.metric("Risco de Insuficiência Cardíaca", formatar_risco(risco_hf))
        st.caption(modelo_utilizado)
        exibir_interpretacao_prevent(risco_dcv_total)

    except Exception as e:
        st.warning(f"Por favor, preencha todos os dados obrigatórios na página 'Dados do Paciente' para calcular o risco PREVENT.")
        st.caption("(Campos obrigatórios: Idade, Peso, Altura, Col. Total, HDL, PAS, Creatinina Sérica, Sexo).")


def pagina_gastroenterologia():
    """Página de resultados de Gastroenterologia."""
    st.title("Scores de Gastroenterologia")

    # --- MELD 3.0 ---
    st.header("MELD 3.0")
    st.markdown("O 'Model for End-Stage Liver Disease 3.0' é usado para avaliar a gravidade da doença hepática crônica e priorizar pacientes para transplante de fígado.")
    try:
        meld_data = {
            "sex_str": st.session_state.sex,
            "bilirubin": st.session_state.bilirubin,
            "inr": st.session_state.inr,
            "creatinine": st.session_state.creatinine,
            "sodium": st.session_state.sodium,
            "albumin": st.session_state.albumin,
            "dialise": st.session_state.dialise
        }
        if not all(v is not None for v in [meld_data[k] for k in ['bilirubin', 'inr', 'creatinine', 'sodium', 'albumin']]):
            raise TypeError("Campos MELD não preenchidos.")
        
        score_meld = calcular_meld_3_0(**meld_data)
        st.metric("Score MELD 3.0", formatar_score(score_meld, 0))
        exibir_interpretacao_meld(score_meld)

    except Exception as e:
        st.warning("Por favor, preencha os dados na página 'Dados do Paciente' para calcular o MELD 3.0.")
        st.caption("(Campos obrigatórios: Sexo, Bilirrubina, INR, Creatinina, Sódio, Albumina, Diálise).")

    st.divider()

    # --- Child-Pugh ---
    st.header("Child-Pugh")
    st.markdown("O score de Child-Pugh (ou Child-Turcotte-Pugh) é usado para avaliar o prognóstico da doença hepática crônica, principalmente a cirrose.")
    try:
        cp_data = {
            "bilirubin": st.session_state.bilirubin,
            "inr": st.session_state.inr,
            "albumin": st.session_state.albumin,
            "ascites": st.session_state.ascites,
            "encephalopathy": st.session_state.encephalopathy
        }
        if not all(v is not None for v in [cp_data[k] for k in ['bilirubin', 'inr', 'albumin']]):
            raise TypeError("Campos Child-Pugh não preenchidos.")
            
        score_cp = calcular_child_pugh(**cp_data)
        st.metric("Score Child-Pugh", f"{score_cp} pontos")
        exibir_interpretacao_child_pugh(score_cp)

    except Exception as e:
        st.warning("Por favor, preencha os dados na página 'Dados do Paciente' para calcular o Child-Pugh.")
        st.caption("(Campos obrigatórios: Bilirrubina, INR, Albumina, Ascite, Encefalopatia).")
        
    st.divider()

    # --- FIB4 ---
    st.header("FIB-4 (Fibrosis-4 Index)")
    st.markdown("O índice FIB-4 é um score não invasivo para estimar a fibrose hepática em pacientes com doença hepática crônica (ex: Hepatite C, DHGNA).")
    try:
        fib4_data = {
            "age": st.session_state.age,
            "ast": st.session_state.ast,
            "alt": st.session_state.alt,
            "platelets": st.session_state.platelets
        }
        if not all(v is not None for v in fib4_data.values()):
            raise TypeError("Campos FIB4 não preenchidos.")
        
        score_fib4 = calcular_fib4(**fib4_data)
        st.metric("Score FIB-4", formatar_score(score_fib4, 2))
        exibir_interpretacao_fib4(score_fib4, fib4_data["age"])

    except Exception as e:
        st.warning("Por favor, preencha os dados na página 'Dados do Paciente' para calcular o FIB-4.")
        st.caption("(Campos obrigatórios: Idade, AST, ALT, Plaquetas).")

def pagina_endocrinologia():
    st.title("Scores de Endocrinologia")

    # --- IMC ---
    st.header("Índice de Massa Corporal (IMC)")
    st.markdown("O IMC é uma medida internacional usada para calcular se uma pessoa está no peso ideal.")
    try:
        imc_data = {
            "weight": st.session_state.weight,
            "height_cm": st.session_state.height_cm
        }
        if not all(v is not None for v in imc_data.values()):
            raise TypeError("Campos de IMC não preenchidos.")
        
        score_imc = calcular_imc(**imc_data)
        st.metric("IMC", f"{formatar_score(score_imc, 1)} kg/m²")
        exibir_interpretacao_imc(score_imc)

    except Exception as e:
        st.warning("Por favor, preencha os dados na página 'Dados do Paciente' para calcular o IMC.")
        st.caption("(Campos obrigatórios: Peso, Altura).")

    st.divider()
    
    # --- HOMA ---
    st.header("HOMA-IR e HOMA-BETA")
    st.markdown("O 'Homeostatic Model Assessment' (HOMA) é um método para quantificar a resistência à insulina (HOMA-IR) e a função das células beta pancreáticas (HOMA-BETA).")
    try:
        homa_data = {
            "glucose_mg_dl": st.session_state.glucose_fasting,
            "insulin": st.session_state.insulin_fasting
        }
        if not all(v is not None for v in homa_data.values()):
            raise TypeError("Campos HOMA não preenchidos.")
        
        score_homa_ir = calcular_homa_ir(**homa_data)
        score_homa_beta = calcular_homa_beta(**homa_data)
        
        col1, col2 = st.columns(2)
        col1.metric("HOMA-IR", formatar_score(score_homa_ir, 2))
        col2.metric("HOMA-BETA", f"{formatar_score(score_homa_beta, 1)}%")
        
        with col1:
            exibir_interpretacao_homa_ir(score_homa_ir)

    except Exception as e:
        st.warning("Por favor, preencha os dados na página 'Dados do Paciente' para calcular o HOMA.")
        st.caption("(Campos obrigatórios: Glicose de Jejum, Insulina de Jejum).")

def pagina_pneumologia():
    st.title("Scores de Pneumologia")

    # --- CAT ---
    st.header("CAT (COPD Assessment Test)")
    st.markdown("O Teste de Avaliação da DPOC (CAT) é um questionário para quantificar o impacto da DPOC na saúde e bem-estar do paciente.")
    try:
        cat_scores = [
            st.session_state.cat_1, st.session_state.cat_2, st.session_state.cat_3,
            st.session_state.cat_4, st.session_state.cat_5, st.session_state.cat_6,
            st.session_state.cat_7, st.session_state.cat_8
        ]
        score_cat = sum(cat_scores)
        
        st.metric("Score CAT Total", f"{score_cat} / 40")
        exibir_interpretacao_cat(score_cat)
        st.caption("Os valores do questionário são definidos na página 'Dados do Paciente'.")

    except Exception as e:
        st.error("Erro ao calcular o CAT. Verifique os dados de entrada.")

    st.divider()

    # --- mMRC ---
    st.header("Escala de Dispneia mMRC")
    st.markdown("A escala 'Modified Medical Research Council' (mMRC) classifica a gravidade da dispneia em pacientes com doenças respiratórias.")
    try:
        mmrc_str = st.session_state.mmrc_score
        # Extrai o grau (o primeiro caractere)
        score_mmrc = int(mmrc_str.split(":")[0].replace("Grau ", ""))
        
        st.metric("Score mMRC", f"Grau {score_mmrc}")
        exibir_interpretacao_mmrc(score_mmrc)
        st.caption("O grau de dispneia é definido na página 'Dados do Paciente'.")
        
    except Exception as e:
        st.error("Erro ao calcular o mMRC. Verifique os dados de entrada.")

def pagina_nefrologia():
    st.title("Scores de Nefrologia")

    # --- eGFR (CKD-EPI) ---
    st.header("eGFR (CKD-EPI 2021)")
    st.markdown("Calcula a Taxa de Filtração Glomerular estimada (eGFR) usando a fórmula CKD-EPI 2021, que não utiliza raça.")
    try:
        egfr_data = {
            "creatinine": st.session_state.creatinine,
            "age": st.session_state.age,
            "sex_str": st.session_state.sex
        }
        if not all(v is not None for v in egfr_data.values()):
            raise TypeError("Campos eGFR não preenchidos.")
        
        score_egfr = calcular_egfr_ckd_epi(**egfr_data)
        st.metric("eGFR (CKD-EPI 2021)", f"{formatar_score(score_egfr, 0)} mL/min/1.73 m²")
        exibir_interpretacao_egfr(score_egfr)

    except Exception as e:
        st.warning("Por favor, preencha os dados na página 'Dados do Paciente' para calcular o eGFR.")
        st.caption("(Campos obrigatórios: Creatinina Sérica, Idade, Sexo).")

def pagina_resumo():
    """Página que mostra todos os resultados agrupados."""
    st.title("Resumo Geral dos Scores")
    st.markdown("Todos os scores calculados com base nos dados do 'Prontuário do Paciente'.")

    with st.expander("Cardiologia", expanded=True):
        st.subheader("Risco Cardiovascular (PREVENT)")
        try:
            # Calcular dependências
            bmi = calcular_imc(st.session_state.weight, st.session_state.height_cm)
            egfr = calcular_egfr_ckd_epi(st.session_state.creatinine, st.session_state.age, st.session_state.sex)
            
            prevent_data = {
                "sex": 1 if st.session_state.sex == "Feminino" else 0, "age": st.session_state.age, "tc": st.session_state.tc,
                "hdl": st.session_state.hdl, "sbp": st.session_state.sbp, "dm": 1 if st.session_state.dm else 0,
                "smoking": 1 if st.session_state.smoking else 0, "bmi": bmi, "egfr": egfr,
                "bptreat": 1 if st.session_state.bptreat else 0, "statin": 1 if st.session_state.statin else 0,
                "uacr": st.session_state.uacr_val, "hba1c": st.session_state.hba1c_val
            }
            required_prevent = [prevent_data[k] for k in ['age', 'tc', 'hdl', 'sbp', 'bmi', 'egfr']]
            if not all(v is not None for v in required_prevent): raise Exception()
            
            uacr_fornecido = prevent_data["uacr"] is not None
            hba1c_fornecido = prevent_data["hba1c"] is not None
            if not uacr_fornecido and not hba1c_fornecido: logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_base_py(**prevent_data)
            elif uacr_fornecido and not hba1c_fornecido: logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_uacr_py(**prevent_data)
            elif not uacr_fornecido and hba1c_fornecido: logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_hba1c_py(**prevent_data)
            else: logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF = calcular_prevent_full_py(**prevent_data)
            risco_dcv_total, risco_ascvd, risco_hf = calcular_riscos_finais(logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF, prevent_data['age'], prevent_data['tc'], prevent_data['hdl'], prevent_data['statin'], prevent_data['bmi'])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Risco DCV Total", formatar_risco(risco_dcv_total))
            col2.metric("Risco ASCVD", formatar_risco(risco_ascvd))
            col3.metric("Risco IC", formatar_risco(risco_hf))
            exibir_interpretacao_prevent(risco_dcv_total)
        except:
            st.info("Dados insuficientes para calcular o score PREVENT.")

    with st.expander("Gastroenterologia", expanded=True):
        st.subheader("MELD 3.0")
        try:
            meld_data = {"sex_str": st.session_state.sex, "bilirubin": st.session_state.bilirubin, "inr": st.session_state.inr, "creatinine": st.session_state.creatinine, "sodium": st.session_state.sodium, "albumin": st.session_state.albumin, "dialise": st.session_state.dialise}
            if not all(v is not None for v in [meld_data[k] for k in ['bilirubin', 'inr', 'creatinine', 'sodium', 'albumin']]): raise Exception()
            score_meld = calcular_meld_3_0(**meld_data)
            st.metric("Score MELD 3.0", formatar_score(score_meld, 0))
            exibir_interpretacao_meld(score_meld)
        except:
            st.info("Dados insuficientes para calcular o MELD 3.0.")
        
        st.subheader("Child-Pugh")
        try:
            cp_data = {"bilirubin": st.session_state.bilirubin, "inr": st.session_state.inr, "albumin": st.session_state.albumin, "ascites": st.session_state.ascites, "encephalopathy": st.session_state.encephalopathy}
            if not all(v is not None for v in [cp_data[k] for k in ['bilirubin', 'inr', 'albumin']]): raise Exception()
            score_cp = calcular_child_pugh(**cp_data)
            st.metric("Score Child-Pugh", f"{score_cp} pontos")
            exibir_interpretacao_child_pugh(score_cp)
        except:
            st.info("Dados insuficientes para calcular o Child-Pugh.")

        st.subheader("FIB-4")
        try:
            fib4_data = {"age": st.session_state.age, "ast": st.session_state.ast, "alt": st.session_state.alt, "platelets": st.session_state.platelets}
            if not all(v is not None for v in fib4_data.values()): raise Exception()
            score_fib4 = calcular_fib4(**fib4_data)
            st.metric("Score FIB-4", formatar_score(score_fib4, 2))
            exibir_interpretacao_fib4(score_fib4, fib4_data["age"])
        except:
            st.info("Dados insuficientes para calcular o FIB-4.")

    with st.expander("Endocrinologia", expanded=True):
        st.subheader("IMC")
        try:
            imc_data = {"weight": st.session_state.weight, "height_cm": st.session_state.height_cm}
            if not all(v is not None for v in imc_data.values()): raise Exception()
            score_imc = calcular_imc(**imc_data)
            st.metric("IMC", f"{formatar_score(score_imc, 1)} kg/m²")
            exibir_interpretacao_imc(score_imc)
        except:
            st.info("Dados insuficientes para calcular o IMC.")

        st.subheader("HOMA-IR & HOMA-BETA")
        try:
            homa_data = {"glucose_mg_dl": st.session_state.glucose_fasting, "insulin": st.session_state.insulin_fasting}
            if not all(v is not None for v in homa_data.values()): raise Exception()
            score_homa_ir = calcular_homa_ir(**homa_data)
            score_homa_beta = calcular_homa_beta(**homa_data)
            col1, col2 = st.columns(2)
            col1.metric("HOMA-IR", formatar_score(score_homa_ir, 2))
            col2.metric("HOMA-BETA", f"{formatar_score(score_homa_beta, 1)}%")
            with col1:
                exibir_interpretacao_homa_ir(score_homa_ir)
        except:
            st.info("Dados insuficientes para calcular o HOMA.")

    with st.expander("Pneumologia", expanded=True):
        st.subheader("CAT (DPOC)")
        try:
            cat_scores = [st.session_state.cat_1, st.session_state.cat_2, st.session_state.cat_3, st.session_state.cat_4, st.session_state.cat_5, st.session_state.cat_6, st.session_state.cat_7, st.session_state.cat_8]
            score_cat = sum(cat_scores)
            st.metric("Score CAT Total", f"{score_cat} / 40")
            exibir_interpretacao_cat(score_cat)
        except:
            st.info("Questionário CAT não preenchido.")
        
        st.subheader("mMRC (Dispneia)")
        try:
            mmrc_str = st.session_state.mmrc_score
            score_mmrc = int(mmrc_str.split(":")[0].replace("Grau ", "")) # Extrai o número do "Grau X"
            st.metric("Score mMRC", f"Grau {score_mmrc}")
            exibir_interpretacao_mmrc(score_mmrc)
        except:
            st.info("Score mMRC não selecionado.")

    with st.expander("Nefrologia", expanded=True):
        st.subheader("eGFR (CKD-EPI 2021)")
        try:
            egfr_data = {"creatinine": st.session_state.creatinine, "age": st.session_state.age, "sex_str": st.session_state.sex}
            if not all(v is not None for v in egfr_data.values()): raise Exception()
            score_egfr = calcular_egfr_ckd_epi(**egfr_data)
            st.metric("eGFR (CKD-EPI 2021)", f"{formatar_score(score_egfr, 0)} mL/min/1.73 m²")
            exibir_interpretacao_egfr(score_egfr)
        except:
            st.info("Dados insuficientes para calcular o eGFR.")


# --- 3. INICIALIZAÇÃO E ROTEAMENTO ---

def initialize_session_state():
    """Define todos os valores possíveis no state para evitar erros na primeira execução."""
    params = {
        "sex": "Feminino", "age": None, "bmi": None, "tc": None, "hdl": None, 
        "sbp": None, "dm": False, "smoking": False, 
        "bptreat": False, "statin": False, "uacr_val": None, "hba1c_val": None, 
        "bilirubin": None, "inr": None, "sodium": None, 
        "albumin": None, "dialise": False, "ascites": "Ausente", 
        "encephalopathy": "Ausente", "ast": None, "alt": None, "platelets": None,
        "weight": None, "height_cm": None, "glucose_fasting": None, 
        "insulin_fasting": None, "creatinine": None,
        "cat_1": 0, "cat_2": 0, "cat_3": 0, "cat_4": 0, "cat_5": 0, "cat_6": 0, 
        "cat_7": 0, "cat_8": 0,
        "mmrc_score": "Grau 0: Dispneia apenas com exercício intenso"
    }
    for key, default_value in params.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def main():
    """Função principal que desenha o app."""
    st.set_page_config(layout="wide", page_title="Calculadoras Médicas")
    
    # Inicializa o st.session_state ANTES de qualquer widget
    initialize_session_state()
    
    # Menu da Barra Lateral
    st.sidebar.title("Plataforma de Scores 🩺")
    st.sidebar.markdown("---")
    
    paginas = {
        "Dados do Paciente": pagina_dados_paciente,
        "Resumo Geral": pagina_resumo,
        "Cardiologia": pagina_cardiologia,
        "Gastroenterologia": pagina_gastroenterologia,
        "Endocrinologia": pagina_endocrinologia,
        "Pneumologia": pagina_pneumologia,
        "Nefrologia": pagina_nefrologia,
    }
    
    selecao = st.sidebar.radio("Navegação:", list(paginas.keys()), key="pagina_selecionada")
    
    # Chama a função da página selecionada
    pagina_selecionada = paginas[selecao]
    pagina_selecionada()

if __name__ == "__main__":
    main()
