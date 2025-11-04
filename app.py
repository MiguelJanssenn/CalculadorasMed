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
        logor_10yr_CVD = -3.307728 + 0.7939329*(age - 55)/10 + 0.0305239*(mmol_conversion_py(tc - hdl) - 3.5) - 0.1606857*(mmol_conversion_py(hdl) - 1.3)/(0.3) - 0.2394003*(min(sbp, 110) - 110)/20 + 0.4462414*(max(sbp, 110) - 130)/20 + 0.9927144*(dm) + 0.6534485*(smoking) - 0.1117663*(min(bmi, 30) - 25)/5 + 0.0985221*(max(bmi, 30) - 30)/5 - 0.1916204*(egfr - 60)/(-15) + 0.3389267*(bptreat) + 0.0000031*(statin)
        logor_10yr_ASCVD = -3.819975 + 0.719883*(age - 55)/10 + 0.1176967*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.151185*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0835358*(min(sbp, 110) - 110)/20 + 0.4216637*(max(sbp, 110) - 130)/20 + 0.9309832*(dm) + 0.8155258*(smoking) - 0.2042813*(min(bmi, 30) - 25)/5 + 0.1307943*(max(bmi, 30) - 30)/5 - 0.1579024*(egfr - 60)/(-15) + 0.2974247*(bptreat) + 0.0307194*(statin)
        logor_10yr_HF = -4.310409 + 0.8998235*(age - 55)/10 - 0.4559771*(min(sbp, 110) - 110)/20 + 0.3576505*(max(sbp, 110) - 130)/20 + 1.038346*(dm) + 0.583916*(smoking) - 0.0072294*(min(bmi, 30) - 25)/5 + 0.0467858*(max(bmi, 30) - 30)/5 - 0.2449829*(egfr - 60)/(-15) + 0.4078071*(bptreat) - 0.0584764*(statin)
    else: # Masculino
        logor_10yr_CVD = -3.031168 + 0.7688528*(age - 55)/10 + 0.0736174*(mmol_conversion_py(tc - hdl) - 3.5) - 0.0954431*(mmol_conversion_py(hdl) - 1.3)/(0.3) - 0.4347345*(min(sbp, 110) - 110)/20 + 0.5467796*(max(sbp, 110) - 130)/20 + 0.9281269*(dm) + 0.5821953*(smoking) - 0.1283408*(min(bmi, 30) - 25)/5 + 0.0776444*(max(bmi, 30) - 30)/5 - 0.0996958*(egfr - 60)/(-15) + 0.1885913*(bptreat) + 0.0001067*(statin)
        logor_10yr_ASCVD = -3.500655 + 0.7099847*(age - 55)/10 + 0.1658663*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1144285*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2837212*(min(sbp, 110) - 110)/20 + 0.5150765*(max(sbp, 110) - 130)/20 + 0.8451116*(dm) + 0.7017055*(smoking) - 0.2003384*(min(bmi, 30) - 25)/5 + 0.1061667*(max(bmi, 30) - 30)/5 - 0.0801698*(egfr - 60)/(-15) + 0.1479555*(bptreat) + 0.0302738*(statin)
        logor_10yr_HF = -3.946391 + 0.8972642*(age - 55)/10 - 0.6811466*(min(sbp, 110) - 110)/20 + 0.3634461*(max(sbp, 110) - 130)/20 + 0.923776*(dm) + 0.5023736*(smoking) - 0.0485841*(min(bmi, 30) - 25)/5 + 0.0234438*(max(bmi, 30) - 30)/5 - 0.1383798*(egfr - 60)/(-15) + 0.2559063*(bptreat) - 0.0711082*(statin)
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
        logor_10yr_CVD = -3.738341 + 0.7969249*((age - 55)/10) + 0.0256635*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1588107*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2255701*(min(sbp, 110) - 110)/20 + 0.4194773*(max(sbp, 110) - 130)/20 + 0.8889289*(dm) + 0.6492178*(smoking) - 0.1070318*(min(bmi, 30) - 25)/5 + 0.0879889*(max(bmi, 30) - 30)/5 - 0.1405965*(egfr - 60)/(-15) + 0.3262346*(bptreat) - 0.0067095*(statin) + uacr_term_cvd
        logor_10yr_ASCVD = -4.174614 + 0.7201999*((age - 55)/10) + 0.1135771*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1493506*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0726677*(min(sbp, 110) - 110)/20 + 0.3950769*(max(sbp, 110) - 130)/20 + 0.8254127*(dm) + 0.8090158*(smoking) - 0.1963397*(min(bmi, 30) - 25)/5 + 0.1149604*(max(bmi, 30) - 30)/5 - 0.1040068*(egfr - 60)/(-15) + 0.2839119*(bptreat) + 0.0246663*(statin) + uacr_term_ascvd
        logor_10yr_HF = -4.841506 + 0.9145975*((age - 55)/10) - 0.4441346*(min(sbp, 110) - 110)/20 + 0.3260323*(max(sbp, 110) - 130)/20 + 0.9611365*(dm) + 0.5755787*(smoking) + 0.0008831*(min(bmi, 30) - 25)/5 + 0.0298895*(max(bmi, 30) - 30)/5 - 0.1618092*(egfr - 60)/(-15) + 0.3884682*(bptreat) - 0.0727406*(statin) + uacr_term_hf
    else: # Masculino
        uacr_term_cvd = 0.0916979 if math.isnan(log_uacr) else 0.1887974*log_uacr
        uacr_term_ascvd = 0.0556 if math.isnan(log_uacr) else 0.1510073*log_uacr
        uacr_term_hf = 0.1472194 if math.isnan(log_uacr) else 0.2306299*log_uacr
        logor_10yr_CVD = -3.510705 + 0.7768655*((age - 55)/10) + 0.0659949*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0951111*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.420667*(min(sbp, 110) - 110)/20 + 0.5197926*(max(sbp, 110) - 130)/20 + 0.8278987*(dm) + 0.5785324*(smoking) - 0.120892*(min(bmi, 30) - 25)/5 + 0.0668743*(max(bmi, 30) - 30)/5 - 0.0440869*(egfr - 60)/(-15) + 0.1760267*(bptreat) - 0.0110346*(statin) + uacr_term_cvd
        logor_10yr_ASCVD = -3.85146 + 0.7141718*((age - 55)/10) + 0.1602194*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1139086*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2719456*(min(sbp, 110) - 110)/20 + 0.4880853*(max(sbp, 110) - 130)/20 + 0.7378961*(dm) + 0.6965027*(smoking) - 0.1903598*(min(bmi, 30) - 25)/5 + 0.0953199*(max(bmi, 30) - 30)/5 - 0.0245764*(egfr - 60)/(-15) + 0.1353084*(bptreat) + 0.0241738*(statin) + uacr_term_ascvd
        logor_10yr_HF = -4.556907 + 0.9111795*((age - 55)/10) - 0.6693649*(min(sbp, 110) - 110)/20 + 0.3290082*(max(sbp, 110) - 130)/20 + 0.8377655*(dm) + 0.4978917*(smoking) - 0.042749*(min(bmi, 30) - 25)/5 + 0.0115044*(max(bmi, 30) - 30)/5 - 0.0639677*(egfr - 60)/(-15) + 0.2385024*(bptreat) - 0.0849965*(statin) + uacr_term_hf
    return logor_10yr_CVD, logor_10yr_ASCVD, logor_10yr_HF

def calcular_prevent_hba1c_py(sex, age, tc, hdl, sbp, dm, smoking, bmi, egfr, bptreat, statin, hba1c):
    """ Porta da função 'pred_risk_hba1c' do R """
    logor_10yr_CVD = logor_10yr_ASCVD = logor_10yr_HF = np.nan
    hba1c_val = hba1c if (hba1c is not None and not math.isnan(hba1c)) else np.nan
    if sex == 1: # Feminino
        hba1c_term_cvd = -0.0142496 if math.isnan(hba1c_val) else (0.1338348*(hba1c_val-5.3)*(dm) + 0.1622409*(hba1c_val-5.3)*(1-dm))
        hba1c_term_ascvd = 0.0015678 if math.isnan(hba1c_val) else (0.1339055*(hba1c_val-5.3)*(dm) + 0.1596461*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0143112 if math.isnan(hba1c_val) else (0.1856442*(hba1c_val-5.3)*(dm) + 0.1833083*(hba1c_val-5.3)*(1-dm))
        logor_10yr_CVD = -3.306162 + 0.7858178*((age - 55)/10) + 0.0194438*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1521964*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2296681*(min(sbp, 110) - 110)/20 + 0.4300133*(max(sbp, 110) - 130)/20 + 0.6547968*(dm) + 0.6514476*(smoking) - 0.1161518*(min(bmi, 30) - 25)/5 + 0.0915479*(max(bmi, 30) - 30)/5 - 0.186733*(egfr - 60)/(-15) + 0.3322857*(bptreat) - 0.0045089*(statin) + hba1c_term_cvd
        logor_10yr_ASCVD = -3.838746 + 0.7111831*((age - 55)/10) + 0.106797*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1425745*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0736824*(min(sbp, 110) - 110)/20 + 0.4062502*(max(sbp, 110) - 130)/20 + 0.6098068*(dm) + 0.8107206*(smoking) - 0.2060919*(min(bmi, 30) - 25)/5 + 0.1224629*(max(bmi, 30) - 30)/5 - 0.1523041*(egfr - 60)/(-15) + 0.2911779*(bptreat) + 0.0273305*(statin) + hba1c_term_ascvd
        logor_10yr_HF = -4.288225 + 0.8997391*((age - 55)/10) - 0.4422749*(min(sbp, 110) - 110)/20 + 0.3378691*(max(sbp, 110) - 130)/20 + 0.681284*(dm) + 0.5886005*(smoking) - 0.0148657*(min(bmi, 30) - 25)/5 + 0.0397989*(max(bmi, 30) - 30)/5 - 0.2346086*(egfr - 60)/(-15) + 0.4009168*(bptreat) - 0.0642148*(statin) + hba1c_term_hf
    else: # Masculino
        hba1c_term_cvd = -0.0128373 if math.isnan(hba1c_val) else (0.13159*(hba1c_val-5.3)*(dm) + 0.1295185*(hba1c_val-5.3)*(1-dm))
        hba1c_term_ascvd = -0.0010001 if math.isnan(hba1c_val) else (0.1157161*(hba1c_val-5.3)*(dm) + 0.1288303*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0113444 if math.isnan(hba1c_val) else (0.1652857*(hba1c_val-5.3)*(dm) + 0.1505859*(hba1c_val-5.3)*(1-dm))
        logor_10yr_CVD = -3.040901 + 0.7699177*((age - 55)/10) + 0.0605093*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.0888525*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.417713*(min(sbp, 110) - 110)/20 + 0.529143*(max(sbp, 110) - 130)/20 + 0.6415534*(dm) + 0.5821829*(smoking) - 0.1301863*(min(bmi, 30) - 25)/5 + 0.072696*(max(bmi, 30) - 30)/5 - 0.0942224*(egfr - 60)/(-15) + 0.1841002*(bptreat) - 0.0035698*(statin) + hba1c_term_cvd
        logor_10yr_ASCVD = -3.51835 + 0.7064146*((age - 55)/10) + 0.1532267*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1082166*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.2675288*(min(sbp, 110) - 110)/20 + 0.4993817*(max(sbp, 110) - 130)/20 + 0.5724969*(dm) + 0.7019522*(smoking) - 0.2009896*(min(bmi, 30) - 25)/5 + 0.100655*(max(bmi, 30) - 30)/5 - 0.0745119*(egfr - 60)/(-15) + 0.1430815*(bptreat) + 0.0272071*(statin) + hba1c_term_ascvd
        logor_10yr_HF = -3.961954 + 0.911787*((age - 55)/10) - 0.6568071*(min(sbp, 110) - 110)/20 + 0.3524645*(max(sbp, 110) - 130)/20 + 0.5849752*(dm) + 0.5014014*(smoking) - 0.0512352*(min(bmi, 30) - 25)/5 + 0.0186882*(max(bmi, 30) - 30)/5 - 0.1294527*(egfr - 60)/(-15) + 0.2507323*(bptreat) - 0.0766348*(statin) + hba1c_term_hf
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
        logor_10yr_CVD = -3.860385 + 0.7716794*((age - 55)/10) + 0.0062109*(mmol_conversion_py(tc - hdl) - 3.5) - 0.1547756*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.1933123*(min(sbp, 110) - 110)/20 + 0.3905809*(max(sbp, 110) - 130)/20 + 0.6075584*(dm) + 0.6397651*(smoking) - 0.1046086*(min(bmi, 30) - 25)/5 + 0.0786147*(max(bmi, 30) - 30)/5 - 0.1213086*(egfr - 60)/(-15) + 0.3124788*(bptreat) - 0.0167406*(statin) + uacr_term_cvd + hba1c_term_cvd
        logor_10yr_ASCVD = -4.291503 + 0.7023067*((age - 55)/10) + 0.0898765*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1407316*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.0256648*(min(sbp, 110) - 110)/20 + 0.3665396*(max(sbp, 110) - 130)/20 + 0.5592289*(dm) + 0.7982451*(smoking) - 0.1912677*(min(bmi, 30) - 25)/5 + 0.1052043*(max(bmi, 30) - 30)/5 - 0.0900863*(egfr - 60)/(-15) + 0.2735398*(bptreat) + 0.0189296*(statin) + uacr_term_ascvd + hba1c_term_ascvd
        logor_10yr_HF = -4.896524 + 0.884209*((age - 55)/10) - 0.421474*(min(sbp, 110) - 110)/20 + 0.3002919*(max(sbp, 110) - 130)/20 + 0.6170359*(dm) + 0.5380269*(smoking) - 0.0191335*(min(bmi, 30) - 25)/5 + 0.0206508*(max(bmi, 30) - 30)/5 - 0.1437316*(egfr - 60)/(-15) + 0.3736044*(bptreat) - 0.0836224*(statin) + uacr_term_hf + hba1c_term_hf
    else: # Masculino
        uacr_term_cvd = 0.1095674 if math.isnan(log_uacr) else 0.1772853*log_uacr
        uacr_term_ascvd = 0.0652944 if math.isnan(log_uacr) else 0.1375837*log_uacr
        uacr_term_hf = 0.1702805 if math.isnan(log_uacr) else 0.2164607*log_uacr
        hba1c_term_cvd = -0.0230072 if math.isnan(hba1c_val) else (0.1165698*(hba1c_val-5.3)*(dm) + 0.1048297*(hba1c_val-5.3)*(1 - dm))
        hba1c_term_ascvd = -0.0112852 if math.isnan(hba1c_val) else (0.101282*(hba1c_val-5.3)*(dm) + 0.1092726*(hba1c_val-5.3)*(1-dm))
        hba1c_term_hf = -0.0234637 if math.isnan(hba1c_val) else (0.148297*(hba1c_val-5.3)*(dm) + 0.1234088*(hba1c_val-5.3)*(1-dm))
        logor_10yr_CVD = -3.631387 + 0.7847578*((age - 55)/10) + 0.0534485*(mmol_conversion_py(tc - hdl) - 3.5) - 0.0911282*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.4921973*(min(sbp, 110) - 110)/20 + 0.4973365*(max(sbp, 110) - 130)/20 + 0.5551685*(dm) + 0.5749388*(smoking) - 0.1174366*(min(bmi, 30) - 25)/5 + 0.0596829*(max(bmi, 30) - 30)/5 + 0.0089518*(egfr - 60)/(-15) + 0.1632606*(bptreat) - 0.0225355*(statin) + uacr_term_cvd + hba1c_term_cvd
        logor_10yr_ASCVD = -3.969788 + 0.7128741*((age - 55)/10) + 0.1465201*((mmol_conversion_py(tc) - mmol_conversion_py(hdl)) - 3.5) - 0.1125794*(mmol_conversion_py(hdl) - 1.3)/0.3 - 0.3387216*(min(sbp, 110) - 110)/20 + 0.4647987*(max(sbp, 110) - 130)/20 + 0.4800699*(dm) + 0.6924193*(smoking) - 0.1848598*(min(bmi, 30) - 25)/5 + 0.0860975*(max(bmi, 30) - 30)/5 + 0.0337427*(egfr - 60)/(-15) + 0.1241255*(bptreat) + 0.0191854*(statin) + uacr_term_ascvd + hba1c_term_ascvd
        logor_10yr_HF = -4.663513 + 0.9095703*((age - 55)/10) - 0.6765184*(min(sbp, 110) - 110)/20 + 0.3111651*(max(sbp, 110) - 130)/20 + 0.5535052*(dm) + 0.4326811*(smoking) - 0.0854286*(min(bmi, 30) - 25)/5 + 0.0005782*(max(bmi, 30) - 30)/5 - 0.0470054*(egfr - 60)/(-15) + 0.223257*(bptreat) - 0.0981031*(statin) + uacr_term_hf + hba1c_term_hf
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

    # --- CORREÇÃO DO BUG DE PERSISTÊNCIA ---
    # Removido value= e index= pois o key= gerencia automaticamente o estado
    
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
        st.number_input("Relação Albumina/Creatinina Urinária (RAC) (mg/g)", min_value=0.0, max_value=5000.0, step=0.1, format="%.1f", key="uacr_val", placeholder="Opcional: Ex: 10.0")
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
        st.warning
