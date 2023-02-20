import pandas as pd
import numpy as np
import streamlit as st
import math

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
    m_wt= st.number_input('Molecular weight')
    z= st.number_input('Compressibility factor')
    k= st.number_input('Cp/Cv')
    
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
        poly_coef = (1-(math.log10(td_ts)/math.log10(dd_ds)))**-1
        n_1_n = (poly_coef - 1)/ poly_coef
        poly_eff = (poly_coef*(k-1))/(k*(poly_coef-1)) * 100
        adiab_eff = (suc_t/(disch_t-suc_t))*((dd_ds**k_1_k)-1) * 100
        td_adiab = suc_t*((disch_p/suc_p)**k_1_k)-273
        power_kw = ((1/(adiab_eff*3672)))*r_mwt*suc_t*z*m_kg_hr*(p_port)*k_k_1
        return poly_eff, adiab_eff, td_adiab, power_kw,m_kg_hr,dd_ds,poly_coef,td_ts
    if st.button("Reveal Calculations", key = 'calculations_table'):
        try:
            poly_eff, adiab_eff, td_adiab, power_kw,m_kg_hr,dd_ds,poly_coef,td_ts =   calculations(Q_nm3, suc_p,suc_t, disch_p,disch_t,m_wt,z,k)
            url = 'https://raw.githubusercontent.com/Ahmedhassan676/compressor_evaluation/main/compressor_table.csv'
            df = pd.read_csv(url, index_col=0)
            df['Calculations'] = [Q_nm3,m_kg_hr,suc_p, disch_p,suc_t,disch_t,td_adiab, power_kw,m_wt,z,k,dd_ds,td_ts,poly_coef,poly_eff, adiab_eff]
            st.dataframe(df)
        except (ValueError, TypeError, KeyError, ZeroDivisionError): st.write('Please Check your data')

if __name__ == '__main__':
    main()