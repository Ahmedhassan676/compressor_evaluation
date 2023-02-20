import pandas as pd
import numpy as np
import streamlit as st

def main():
    html_temp="""
        <div style="background-color:lightblue;padding:16px">
        <h2 style="color:black"; text-align:center> Compressor Performance Evaluation </h2>
        </div>
        <style>
        table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }

        td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        }
        </style>
            """
    st.markdown(html_temp, unsafe_allow_html=True)
    Q_nm3= st.number_input('Capacity (nm3/hr)')
    suc_p= st.number_input('Suction pressure (kg/cm2.g)')
    suc_t= st.number_input('Suction temperature (C)')
    disch_p= st.number_input('Discharge pressure (kg/cm2.g)')
    disch_t= st.number_input('Discharge temperature (C)')
    s1 = st.selectbox('Estimate M.wt, Cp/Cv and Z?',('I already have these values','Yes'), key = 'k_calculations')
    if s1 == 'I already have these values':
        m_wt= st.number_input('Molecular weight')
        z= st.number_input('Compressibility factor')
        k= st.number_input('Cp/Cv')
    else:
        url = 'https://raw.githubusercontent.com/Ahmedhassan676/compressor_evaluation/main/composition.csv'
        df = pd.read_csv(url, index_col=0)
        
        try:
            if np.sum(df['mol%']) != 100:
                c1 = st.number_input('hydrogen%', key = 'c1')
                c2 = st.number_input('methane%', key = 'c2')
                c3 = st.number_input('ethane%', key = 'c3')
                c15 = st.number_input('ethylene%', key = 'c15')
                c4 = st.number_input('propane%', key = 'c4')
                c5 = st.number_input('nbutane%', key = 'c5')
                c6 = st.number_input('isobutane%', key = 'c6')
                c7 = st.number_input('pentane%', key = 'c7')
                c8 = st.number_input('hexane%', key = 'c8')
                c9 = st.number_input('Oxygen%', key = 'c9')
                c16 = st.number_input('nitrogen%', key = 'c16')
                c10 = st.number_input('carbon monoxide%', key = 'c10')
                c11 = st.number_input('carbon dioxide%', key = 'c11')
                c12 = st.number_input('sulphur dioxide%', key = 'c12')
                c13 = st.number_input('hydrogen sulphide%', key = 'c13')
                c14 = st.number_input('air%', key = 'c14')
                if c1 or c2 or c3 or c15 or c4 or c5 or c6 or c7 or c8 or c9 or c16 or c10 or c11 or c12 or c13 or c14:
                    c = []
                    for i in (c1,c2,c3,c15,c4,c5,c6,c7,c8,c9,c16,c10,c11,c12,c13,c14):
                        c.append(i)
                    
                    for (i,j) in zip(range(len(df['mol%'])),c):
                        if j != None:
                                df['mol%'][i] = j
                    st.dataframe(df)
            else: st.dataframe(df)
        except TypeError: st.write('your total mol. percent should add up to 100')

    
    def calculations(Q_nm3, suc_p,suc_t, disch_p,disch_t,m_wt,z,k):
        m_kg_hr = Q_nm3*m_wt*0.044
        suc_p = suc_p + 1.03323
        disch_p = disch_p + 1.03323
        suc_t = suc_t + 273
        disch_t = disch_t + 273
        k_1_k = (k-1)/k
        k_k_1 = k/(k-1)
        r = 847.83
        td_ts = disch_t/suc_t
        dd_ds = disch_p/suc_p
        p_port = (dd_ds**k_1_k) - 1
        r_mwt = r / m_wt
        poly_coef = (1-(np.log(td_ts)/np.log(dd_ds)))**-1
        n_1_n = (poly_coef - 1)/ poly_coef
        poly_eff = (poly_coef*(k-1))/(k*(poly_coef-1)) * 100
        adiab_eff = (suc_t/(disch_t-suc_t))*((dd_ds**k_1_k)-1) * 100
        td_adiab = suc_t*((disch_p/suc_p)**k_1_k)-273
        power_kw = ((1/(adiab_eff*3672)))*r_mwt*suc_t*z*m_kg_hr*(p_port)*k_k_1
        return poly_eff, adiab_eff, td_adiab, power_kw,m_kg_hr,dd_ds,poly_coef,td_ts
    def k_calculations(df, c):
        
        
        return df
    if st.button("Reveal Calculations", key = 'calculations_table'):
        try:
            poly_eff, adiab_eff, td_adiab, power_kw,m_kg_hr,dd_ds,poly_coef,td_ts =   calculations(Q_nm3, suc_p,suc_t, disch_p,disch_t,m_wt,z,k)
            url = 'https://raw.githubusercontent.com/Ahmedhassan676/compressor_evaluation/main/compressor_table.csv'
            df = pd.read_csv(url, index_col=0)
            df['Calculations'] = [Q_nm3,m_kg_hr,suc_p, suc_t, disch_p,disch_t,td_adiab, power_kw,m_wt,z,k,dd_ds,td_ts,poly_coef,poly_eff, adiab_eff]
            st.dataframe(df)
        except (ValueError, TypeError, KeyError, ZeroDivisionError): st.write('Please Check your data')

if __name__ == '__main__':
    main()