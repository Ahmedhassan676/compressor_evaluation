import pandas as pd
import numpy as np
import streamlit as st

def calculations(Q_nm3, suc_p,suc_t, disch_p,disch_t,m_wt,z,k):
        m_kg_hr = Q_nm3*m_wt*0.0446098580359918482953956685434
        suc_p = suc_p + 1.03323
        disch_p = disch_p + 1.03323
        suc_t = suc_t + 273.15
        disch_t = disch_t + 273.15
        k_1_k = (k-1)/k
        k_k_1 = k/(k-1)
        r = 8.3143
        td_ts = disch_t/suc_t
        dd_ds = disch_p/suc_p
        p_port = (dd_ds**k_1_k) - 1
        r_mwt = r / m_wt
        poly_coef = (1-(np.log(td_ts)/np.log(dd_ds)))**-1
        n_1_n = (poly_coef - 1)/ poly_coef
        poly_eff = (k_1_k*np.log(dd_ds)/np.log(td_ts)) * 100
        adiab_eff = (suc_t/(disch_t-suc_t))*((dd_ds**k_1_k)-1) * 100
        td_adiab = suc_t*((disch_p/suc_p)**k_1_k)-273
        power_kw = ((1/(poly_eff*36)))*r_mwt*suc_t*z*m_kg_hr*(p_port)*k_k_1
        return poly_eff, adiab_eff, td_adiab, power_kw,m_kg_hr,dd_ds,poly_coef,td_ts
def k_calculations(df,Q_nm3,suc_p,suc_t, disch_p,disch_t):
        k = sum(df['mol%']*df['cp/cv']*0.01)
        m_wt = sum(df['mol%']*df['m.wt']*0.01)
        df1= pd.DataFrame({'mol%':100,'m.wt':m_wt,'cp/cv':k}, index=['Total'])
        df = df[df['mol%'] != 0].sort_values(by='mol%', ascending=False).append(df1)
        SGr = m_wt/29
        p = [suc_p,disch_p]
        t = [suc_t,disch_t]
        q_m3hr = [Q_nm3*((t[i]+273)/(273))*((1.03323)/(p[i]+ 1.03323)) for i in range(2)]
        density_lb_ft3 = [((Q_nm3*m_wt*0.044)/q_m3hr[i])*0.062428 for i in range(2)]
        p = (np.array(p)+1) * 14.2233
        t = np.array(t)*1.8 + 491.67
        Z = [0,0]
        
        
        for i in range(2):
            #if p[i] <= 100:
             #   Z[i] = 1
            #else: Z[i] = 1/(1+((p[i]*34400*(10**(1.85*SGr)))/(t[i]**3.825)))
            Z[i] = (m_wt*p[i])/(10.73*t[i]*density_lb_ft3[i])
        z =  sum(Z)/2
        return st.dataframe(df), z, m_wt, k

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
    Q_nm3= st.number_input('Capacity (nm3/hr)', key = 'cap_1')
    suc_p= st.number_input('Suction pressure (kg/cm2.g)', key = 'sucp')
    suc_t= st.number_input('Suction temperature (C)', key = 'suct')
    disch_p= st.number_input('Discharge pressure (kg/cm2.g)', key = 'disp')
    disch_t= st.number_input('Discharge temperature (C)', key = 'dist')
    s1 = st.selectbox('Estimate M.wt, Cp/Cv and Z?',('I already have these values','Yes'), key = 'k_calculations')
    if s1 == 'I already have these values':
        m_wt= st.number_input('Molecular weight' , key = 'mwt')
        z= st.number_input('Compressibility factor', key = 'z')
        k= st.number_input('Cp/Cv', key = 'k')
    else:
        url = 'https://raw.githubusercontent.com/Ahmedhassan676/compressor_evaluation/main/composition.csv'
        df = pd.read_csv(url, index_col=0)
        
        try:
            sum_of_comp = 0 
            c1,c2,c3,c15,c4,c5,c6,c7,c8,c9,c16,c10,c11,c12,c13,c14 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
            while sum_of_comp != 100:
                options = st.multiselect(
                'Select your components',
                df.index.values)
                if df.index.values[0] in options:
                    c1 = st.number_input('hydrogen%', key = 'c1')
                if df.index.values[1] in options:
                    c2 = st.number_input('methane%', key = 'c2')
                if df.index.values[2] in options:
                    c3 = st.number_input('ethane%', key = 'c3')
                if df.index.values[3] in options:
                    c15 = st.number_input('ethylene%', key = 'c15')
                if df.index.values[4] in options:
                    c4 = st.number_input('propane%', key = 'c4')
                if df.index.values[5] in options:
                    c5 = st.number_input('nbutane%', key = 'c5')
                if df.index.values[6] in options:
                    c6 = st.number_input('isobutane%', key = 'c6')
                if df.index.values[7] in options:
                    c7 = st.number_input('pentane%', key = 'c7')
                if df.index.values[8] in options:
                    c8 = st.number_input('hexane%', key = 'c8')
                if df.index.values[9] in options:
                    c9 = st.number_input('Oxygen%', key = 'c9')
                if df.index.values[10] in options:
                    c16 = st.number_input('nitrogen%', key = 'c16')
                if df.index.values[11] in options:
                    c10 = st.number_input('carbon monoxide%', key = 'c10')
                if df.index.values[12] in options:
                    c11 = st.number_input('carbon dioxide%', key = 'c11')
                if df.index.values[13] in options:
                    c12 = st.number_input('sulphur dioxide%', key = 'c12')
                if df.index.values[14] in options:
                    c13 = st.number_input('hydrogen sulphide%', key = 'c13')
                if df.index.values[15] in options:
                    c14 = st.number_input('air%', key = 'c14')
                if c1 or c2 or c3 or c15 or c4 or c5 or c6 or c7 or c8 or c9 or c16 or c10 or c11 or c12 or c13 or c14:
                    c = []
                    for i in (c1,c2,c3,c15,c4,c5,c6,c7,c8,c9,c16,c10,c11,c12,c13,c14):
                        c.append(i)
                    
                    for (i,j) in zip(range(len(df['mol%'])),c):
                        if j != None:
                                df['mol%'][i] = j
                    
                    sum_of_comp = np.sum(df['mol%'])
            st.success('This is a success message!', icon="✅")
            df, z, m_wt, k = k_calculations(df,Q_nm3,suc_p,suc_t, disch_p,disch_t)

        except (st.errors.DuplicateWidgetID): st.write('your total mol. percent should add up to 100')
        except (TypeError, KeyError, ZeroDivisionError):st.write('Please Check your data')

    
    
    
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
