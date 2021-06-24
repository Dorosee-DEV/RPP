# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 11:36:24 2021

@author: BC-Woo
"""



import flaskapp
import pandas as pd
import numpy as np
import time
import datetime  
import os
#import dataframe_image as dfi


def rmi_analysis(year0, km0):
    filePath = f"static/resources/analysis_result.csv"
    if os.path.isfile(filePath):
        os.remove(filePath)

    PROJECT_DIRECTORY_PREFIX = os.getcwd()

    HPMS_DIRECTORY = os.path.join(PROJECT_DIRECTORY_PREFIX, 'input_Data/HPMS.csv')
    ESAL_DIRECTORY = os.path.join(PROJECT_DIRECTORY_PREFIX, 'input_Data/ESAL.csv')
    W_DIRECTORY = os.path.join(PROJECT_DIRECTORY_PREFIX, 'input_Data/W.csv')
    JSJ_DIRECTORY = os.path.join(PROJECT_DIRECTORY_PREFIX, 'input_Data/JSJ.csv')
    JISA_DIRECTORY = os.path.join(PROJECT_DIRECTORY_PREFIX, 'input_Data/jisa.csv')


    df1 = pd.read_csv(HPMS_DIRECTORY, encoding='cp949')
    df2 = pd.read_csv(ESAL_DIRECTORY, encoding='cp949')
    df3 = pd.read_csv(W_DIRECTORY, encoding='cp949')
    df4 = pd.read_csv(JSJ_DIRECTORY, encoding='cp949')
    df5 = pd.read_csv(JISA_DIRECTORY, encoding='cp949')


    

    #%% 재령
    age1 = df2.loc[:, '조사연도']
    age2 = df2.loc[:, '개통연도']
    age = pd.DataFrame(age1 - age2)
    age.columns = ['age']

    #%% 교통량
    ESAL_x = df2.iloc[:, 6:]

    l_row = len(ESAL_x)
    l_col = len(ESAL_x.columns)

    cp_e = {'cp' : [0.0001, 0.839, 0.004, 0.616, 3.417, 3.417, 3.417, 2.32, 4.472, 3.072, 4.472, 1.533]}
    cp = pd.DataFrame(cp_e)

    charo = pd.DataFrame(df2.loc[:, '차로'])
    charo_1 = charo.transpose()

    ES_nx = np.array(ESAL_x)
    cp_n = np.array(cp)
    cp_n1 = cp_n.transpose()

    ES = ES_nx * cp_n1
    ESA = ES.sum(axis = 1)/charo_1
    ESAL = pd.DataFrame(ESA.transpose())
    ESAL = ESAL.rename({'차로':'ESAL'},axis='columns')

    #%% 교통량 +ESAL+재령
    df2_r = pd.DataFrame()
    df2_r = pd.concat([df2, ESAL, age], axis=1)


    #%%   연도 추출

    df3_d = pd.DataFrame({'date': pd.to_datetime(df3['일시'])})
    df3['Year'] = df3_d['date'].dt.year                # df3에 연도를 추출해서 붙임

    #%% 기상
    df3_res = pd.DataFrame()                  # 결과 데이터프레임
    df3_re = pd.DataFrame()
    df3_r = pd.DataFrame()


    a = df3.drop_duplicates('지점명', keep='first')
    b = df3.drop_duplicates('Year', keep='first')


    

    for i in range(0, len(a)):

        x = a.iloc[i, 1]

        for j in range(0, len(b)):

            y = b.iloc[j, 6]

            # 조건에 맞는 데이터 df3로부터 추출(ex 속초2010)
            df3_c = pd.DataFrame()
            is_jj = df3['지점명'] == x
            is_da = df3['Year'] == y
            df3_c = df3[is_jj & is_da]

            if len(df3_c) >= 365:

                fzz = 0
                df3_res['지점명'] = [x]
                df3_res['Year'] = [y]
                df3_res['min'] = [min(df3_c['최저기온(°C)'])]
                df3_res['max'] = [max(df3_c['최고기온(°C)'])]
                df3_res['연교차'] = [max(df3_c['최고기온(°C)']) - min(df3_c['최저기온(°C)'])]
                # 강수일수 카운트
                counterFunc = df3_c.apply(lambda x: True if x[5] > 0 else False , axis=1)
                df3_res['강수일수'] = [len(counterFunc[counterFunc == True].index)]

                for k in range(0, len(df3_c)):

                    if df3_c.iloc[k, 3] < -2.2 and df3_c.iloc[k, 4] > 0 and df3_c.iloc[k, 5] > 0:
                        fzz = fzz + 1
                df3_res['freezingDay'] = [fzz]


                df3_re = df3_re.append(df3_res, ignore_index=True)



    #%%  지점별 연교차, 동결융해일수, 강수일수


    df3_fn = pd.DataFrame()
    a = df3_re.drop_duplicates('지점명', keep='first')


    for i in range(0, len(a)):
        x = a.iloc[i, 0]


        is_ji = df3_re['지점명'] == x
        df3r_1 = df3_re[is_ji]


        df3_r['지점명'] = [x]
        df3_r['연교차'] = [df3r_1['연교차'].mean()]
        df3_r['동결융해일수'] = [df3r_1['freezingDay'].mean()]
        df3_r['강수일수'] = [df3r_1['강수일수'].mean()]


        df3_fn = df3_fn.append(df3_r, ignore_index=True)


    #%% 지사별 지점 데이터

    df5_r = pd.DataFrame()
    df5_re = pd.DataFrame()
    df55 = pd.DataFrame()

    for i in range(0, len(df5)):

        x = df5.iloc[i, 1]
        is_j = df3_fn['지점명'] == x
        df5_re = df3_fn[is_j]
        df5_r = df5_r.append(df5_re, ignore_index=True)

    df55 = pd.concat([df5, df5_r], axis=1)
    df55 = df55.drop(['지점'], axis=1)

    #%% 제설제사용량

    df5_fn = pd.DataFrame()

    ton = df4.loc[:, '제설제사용량(ton)']
    km = df4.loc[:, '지사별관리연장(km)']
    jsj = pd.DataFrame(ton/km)
    jsj.columns=['제설제사용량']
    df5_fn = pd.concat([df4['지사'], jsj['제설제사용량']], axis=1)

    #%%   ESAL 재령 통합

    df_r = pd.DataFrame()
    df_re = pd.DataFrame()
    df_res = pd.DataFrame()

    for i in range(len(df1)):

        a = df1.iloc[i,3]
        sj = df1.iloc[i,7]
        jj = df1.iloc[i,8]

        is_ns = df2_r['노선명'] == a
        is_sj = df2_r['시점이정'] <= sj
        is_jj = df2_r['종점이정'] >= jj

        df_r = df2_r[is_ns & is_sj & is_jj]
        df_re = pd.concat([df_r['ESAL'], df_r['age']], axis=1)
        df_res = df_res.append(df_re, ignore_index=True)

    #%%  연교차 강우일수 동결융해일수 통합

    df_r3 = pd.DataFrame()
    df_re3 = pd.DataFrame()
    df_res3 = pd.DataFrame()

    for i in range(len(df1)):



        a = df1.iloc[i,2]   #지사

        is_js = df55['지사'] == a

        df_r3 = df55[is_js]
        df_re3 = pd.concat([df_r3['연교차'], df_r3['동결융해일수'], df_r3['강수일수']], axis=1)
        df_res3 = df_res3.append(df_re3, ignore_index=True)

    #%% 제설제

    df_r4 = pd.DataFrame()
    df_re4 = pd.DataFrame()
    df_res4 = pd.DataFrame()

    for i in range(len(df1)):



        a = df1.iloc[i,2]   #지사

        is_js = df5_fn['지사'] == a

        df_r4 = df5_fn[is_js]

        df_res4 = df_res4.append(df_r4, ignore_index=True)

    df_res4.drop(['지사'], axis = 1, inplace=True)

    #%% 통합DB

    df_fn = pd.DataFrame()

    df_fn = pd.concat([df1, df_res, df_res3, df_res4], axis=1)

    df_fn.drop(['노선번호'], axis = 1, inplace=True)

    #%%  RMI 계산
    import math

    df_rmi_x = pd.DataFrame()
    df_rmi = pd.DataFrame()
    diri = 0
    dsd = 0
    rmi = 0

    y_1 = df_fn.iloc[0,0]   #조사연도
    y_2 = int(year0)            #예측연도
    n = int(y_2 - y_1)
    if int(y_1 - y_2) >= 0:
        return os.exit()

    for i in range(len(df1)):


        df_fn.iloc[i,:]
        if df_fn.iloc[i,8] == 'JCP':
            a = 1.668
            b = 1.74
            AGE2_1 = 0.000078
            IRI_1 = 0.04658
            RT_1 = 0.0017
            DP_1 = 0.001287
            ASR_1 = 0.3048
            ESAL_1 = 0.008374
            const_1 = -0.2743
            SD_2 = 0.597787
            RT_2 = 0.010229
            ADFT_2 = 0.011852
            const_2 = -0.3021

        else:
            a = 2.29
            b = 1.464
            AGE2_1 = 0
            IRI_1 = 0.03753
            RT_1 = 0.030894
            DP_1 = 0.007087
            ASR_1 = 0
            ESAL_1 = 0.005695
            const_1 = -1.916763
            SD_2 = 1.034144
            RT_2 = 0.023678
            ADFT_2 = 0.011436
            const_2 = -0.851327

        iri = df_fn.iloc[i,9]
        sd = df_fn.iloc[i,10]
        hpci = df_fn.iloc[i,11]
        asr = df_fn.iloc[i,12]
        esal = df_fn.iloc[i,13]
        age = df_fn.iloc[i,14]
        rt = df_fn.iloc[i,15]      # 연교차
        ft = df_fn.iloc[i,16]      # 동결융해일수
        dp = df_fn.iloc[i,17]      # 강수일수
        ad = df_fn.iloc[i,18]      # 제설제사용량


        for j in range(1, n+1):


            diri = (AGE2_1*(age+j-1)**2+IRI_1*iri+RT_1*rt+DP_1*dp+ASR_1*asr+ESAL_1*esal/10**3+const_1)

            if ad == 0:
                dsd = (sd*SD_2+rt*RT_2+const_2)
            else:
                dsd = (sd*SD_2+rt*RT_2+ADFT_2*ft*math.log10(ad)+const_2)


            # if (diri > 0).bool() == True:
            if (diri > 0) :

                iri = diri + iri

            if (dsd > 0) :

                sd = dsd + sd

        rmi = b*iri + a*math.log10(1+5*sd)

        if rmi>10:
            rmi = 10

        df_rmi_x = pd.concat([pd.DataFrame([iri]), pd.DataFrame([sd]), pd.DataFrame([rmi])], axis=1)
        df_rmi = df_rmi.append(pd.DataFrame(df_rmi_x), ignore_index=True)


    df_rmi.columns=['IRI', 'SD', 'RMI']

    #%%  우선순위선정 데이터
    df_ws = pd.DataFrame()
    df_ws = pd.concat([df_fn['본부'], df_fn['지사'], df_fn['행선'], df_fn['노선'], df_fn['차로'], df_fn['시점이정'],
                       df_fn['종점이정'], df_rmi['RMI'], df_rmi['IRI'], df_rmi['SD']], axis=1)

    #%%  우선순위선정_3km 이하 구간 통합

    df_w_1 = pd.DataFrame()
    df_w_2 = pd.DataFrame()
    df_w_3 = pd.DataFrame()
    df_w_4 = pd.DataFrame()
    x = int(km0)
    
    for i in range(len(df_ws)):
        
    
        bonbu = df_ws.iloc[i, 0]
        jisa = df_ws.iloc[i, 1]
        hang = df_ws.iloc[i, 2]
        no = df_ws.iloc[i, 3]
        s0 = df_ws.iloc[i, 5]
        jong = df_ws.iloc[i, 6]

        s1 = s0 + x - 0.01
        

        is_hang = df_ws['행선'] == hang
        is_no = df_ws['노선'] == no
        is_s2_1 = df_ws['시점이정'] <= s1
        is_s2_2 = df_ws['시점이정'] >= s0 
        
        df_w_1 = df_ws[is_hang & is_no & is_s2_1 & is_s2_2]
        
        bb = df_w_1.iloc[0, 0]                     #본부
        js = df_w_1.iloc[0, 1]                     #지사
        hs = df_w_1.iloc[0, 2]                     #행선
        ns = df_w_1.iloc[0, 3]                     #노선
        s2jum = df_w_1.iloc[0, 5]                  #시점
        jongjum = df_w_1.iloc[-1, 6]               #종점
        df_w_2['연장'] = [jongjum - s2jum]         #연장
        
        
        mean_RMI = df_w_1['RMI'].mean()            #RMI평균값
        if mean_RMI > 10:
            mean_RMI = 10
        
    
        df_w_3 = pd.concat([pd.DataFrame([bb]), pd.DataFrame([js]), pd.DataFrame([hs]), 
                            pd.DataFrame([ns]), pd.DataFrame([s2jum]), pd.DataFrame([jongjum]),
                            pd.DataFrame(df_w_2['연장']), pd.DataFrame([mean_RMI])], axis=1)
        df_w_4 = df_w_4.append(df_w_3, ignore_index=True)
        
    

    df_w_4.columns = ['본부', '지사', '행선', '노선', '시점이정', '종점이정', '연장', 'RMI']

    #%%  우선순위선정_rmi7이상추출
    df_w_5 = pd.DataFrame()

    for i in range(len(df_w_4)):
        
        df_w_5 = df_w_4[df_w_4['RMI']>=7]
        
    #%%  우선순위선정_구간통합2_겹치는 구간 통합

    df_w_5_a = pd.DataFrame()
    df_w_6 = pd.DataFrame()
    df_w_7 = pd.DataFrame()
    df_w_7_a = pd.DataFrame()
    df_w_8 = pd.DataFrame()

    df_w_5_a = df_w_5[['행선', '노선']]
    df_w_5_a = df_w_5_a.drop_duplicates()

    for i in range(len(df_w_5_a)):
        
    
        
        hang = df_w_5_a.iloc[i, 0]
        no = df_w_5_a.iloc[i, 1]
        

        is_hang = df_w_5['행선'] == hang
        is_no = df_w_5['노선'] == no
        
        df_w_6 = df_w_5[is_hang & is_no]
            
        
        if len(df_w_6) >= 3:
            
            s1 = df_w_6.iloc[0, 4]
            s2 = df_w_6.iloc[1, 4]
            j1 = df_w_6.iloc[0, 5]
            j2 = df_w_6.iloc[1, 5]
            
            for j in range(len(df_w_6)-2):
                
                
                bonbu = df_w_6.iloc[j, 0]
                jisa = df_w_6.iloc[j, 1]
                
                
                if s1 <= s2 and j1 >= s2 and j2 >= j1:
                    
                    j1 = j2
                    s2 = df_w_6.iloc[j+2, 4]
                    j2 = df_w_6.iloc[j+2, 5]
                    
                    df_w_7 = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no],
                                        "시점이정":[s1], "종점이정":[j1], "연장":[j1-s1]})
                    if j == len(df_w_6)-3:
                        
                    
                        if s1 <= s2 and j1 >= s2 and j2 >= j1:
                        
                            df_w_7 = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no],
                                        "시점이정":[s1], "종점이정":[j2], "연장":[j2-s1]})
                        else:
                            
                            bonbu = df_w_6.iloc[-1, 0]
                            jisa = df_w_6.iloc[-1, 1]
                            df_w_7_a = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no],
                                        "시점이정":[s2], "종점이정":[j2], "연장":[j2-s2]})
                        
                else:
                    
                    
                    df_w_7 = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no],
                                        "시점이정":[s1], "종점이정":[j1], "연장":[j1-s1]})
                    df_w_8 = df_w_8.append(df_w_7, ignore_index=True)
                    
                    s1 = df_w_6.iloc[j+1, 4]
                    s2 = df_w_6.iloc[j+2, 4]
                    j1 = df_w_6.iloc[j+1, 5]
                    j2 = df_w_6.iloc[j+2, 5]

            df_w_8 = df_w_8.append(df_w_7, ignore_index=True)
            df_w_8 = df_w_8.append(df_w_7_a, ignore_index=True)
            df_w_8 = df_w_8.drop_duplicates()

        elif len(df_w_6) == 2:
            
            bonbu = df_w_6.iloc[0, 0]
            jisa = df_w_6.iloc[0, 1]
            
            s1 = df_w_6.iloc[0, 4]
            s2 = df_w_6.iloc[1, 4]
            j1 = df_w_6.iloc[0, 5]
            j2 = df_w_6.iloc[1, 5]
            
            if s1 <= s2 and j1 >= s2 and j2 >= j1:
                
            
                df_w_7 = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no],
                                    "시점이정":[s1], "종점이정":[j2], "연장":[j2-s1]})
                df_w_8 = df_w_8.append(df_w_7, ignore_index=True)
            
            else:
                
                df_w_7 = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no],
                                    "시점이정":[s1], "종점이정":[j1], "연장":[j1-s1]})
                df_w_8 = df_w_8.append(df_w_7, ignore_index=True)
            

        else:
            
            bonbu = df_w_6.iloc[0, 0]
            jisa = df_w_6.iloc[0, 1]
            
            df_w_7 = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no], 
                                "시점이정":[df_w_6.iloc[0,4]], "종점이정":[df_w_6.iloc[0,5]]
                                , "연장":[df_w_6.iloc[0,5] - df_w_6.iloc[0,4]]})
            
            df_w_8 = df_w_8.append(df_w_7, ignore_index=True)



    #%%  우선순위선정_구간통합3_평균 RMI계산

    df_w_9 = pd.DataFrame()
    df_w_8_a = pd.DataFrame()
    df_w_10 = pd.DataFrame()

    for i in range(len(df_w_8)):
    
    
        bonbu = df_w_8.iloc[i,0]
        jisa = df_w_8.iloc[i,1]
        hang = df_w_8.iloc[i,2]
        no = df_w_8.iloc[i,3]
        s2 = df_w_8.iloc[i,4]
        jong = df_w_8.iloc[i,5]
        

        is_hang = df_ws['행선'] == hang
        is_no = df_ws['노선'] == no
        is_s2 = df_ws['시점이정'] >= s2
        is_jong = df_ws['종점이정'] <= jong
        
        df_w_9 = df_ws[is_hang & is_no & is_s2 & is_jong]
        mean_RMI = round(df_w_9['RMI'].mean(),2)
            
        if mean_RMI > 10:
            mean_RMI = 10
        
        df_w_8_a = df_w_8_a.append(pd.DataFrame([mean_RMI]), ignore_index=True)


    df_w_10 = pd.concat([df_w_8, df_w_8_a], axis=1)
    df_w_10.columns = ['본부', '지사', '행선', '노선', '시점이정', '종점이정', '연장', 'RMI']

    #%% 1km 미만 구간 통합

    df_w_11 = pd.DataFrame()
    df_w_11_a = pd.DataFrame()
    df_w_11_b = pd.DataFrame()
    df_w_11_c = pd.DataFrame()
    df_w_11_d = pd.DataFrame()
    df_w_11_e = pd.DataFrame()
    df_w_12 = pd.DataFrame()


    df_w_12 = df_w_10[['행선', '노선']]
    df_w_12 = df_w_12.drop_duplicates()


    for i in range(len(df_w_12)):

        
        hang = df_w_12.iloc[i,0]
        no = df_w_12.iloc[i,1]
        
        is_hang = df_w_10['행선'] == hang
        is_no = df_w_10['노선'] == no
        
        df_w_11_a = df_w_10[is_hang & is_no]
    

        if len(df_w_11_a) >= 3:

            s1 = df_w_11_a.iloc[0,4]                ## 시점이정1
            s2 = df_w_11_a.iloc[1,4]                ## 시점이정2
            j1 = df_w_11_a.iloc[0,5]                ## 종점이정1
            j2 = df_w_11_a.iloc[1,5]                ## 종점이정2
            
            
            for j in range(len(df_w_11_a)-1):
            
                bonbu = df_w_11_a.iloc[j,0]
                jisa = df_w_11_a.iloc[j,1]
                
                if j!=0:
                    
                    s2 = df_w_11_a.iloc[j+1,4]                ## 시점이정2
                    j1 = df_w_11_a.iloc[j,5]                  ## 종점이정1
                    j2 = df_w_11_a.iloc[j+1,5]                ## 종점이정2 
                    
                if s2-j1<=1:
                    
                
                    is_hang = df_ws['행선'] == hang
                    is_no = df_ws['노선'] == no
                    
                    is_si = df_ws['시점이정'] >= s1
                    is_jong = df_ws['종점이정'] <= j2
                    
                    df_w_11_b = df_ws[is_hang & is_no & is_si & is_jong]
                    
                    mean_RMI = round(df_w_11_b['RMI'].mean(),2)

                    if mean_RMI > 10:
                        mean_RMI = 10
                    
                    if mean_RMI >= 7:
                        
                        df_w_11_c = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no], 
                                                "시점이정":[s1], "종점이정":[j2], "연장":[j2-s1], "RMI":[mean_RMI]})
                        
                        ## s1이 변하면 안됨
                        if j == len(df_w_11_a)-2:
                            df_w_11_d = df_w_11_d.append(df_w_11_c, ignore_index=True)
                            
                    else:
                        df_w_11_d = df_w_11_d.append(df_w_11_a.iloc[[j]], ignore_index=True)
                
                        
                        if j == len(df_w_11_a)-2:
                            df_w_11_d = df_w_11_d.append(df_w_11_a.iloc[[j+1]], ignore_index=True)
                        
                        else:
                            
                            s1 = df_w_11_a.iloc[j+1,4]                ## 시점이정1
                
                
                else:
                    
                    #c가 깡통일 때 아무이상 없나?_c가 깡통이 아닐때만 어팬드로 바꾸기
                    
                    df_w_11_d = df_w_11_d.append(df_w_11_c, ignore_index=True)
                    df_w_11_c = pd.DataFrame()
                    
                    if j == 0:
                        df_w_11_d = df_w_11_d.append(df_w_11_a.iloc[[j]], ignore_index=True)
                        
                    elif s2-j1 > 1:
                        
                        j_0 = df_w_11_a.iloc[j-1,4]
                        
                        if s1-j_0 >1:
                            df_w_11_d = df_w_11_d.append(df_w_11_a.iloc[[j]], ignore_index=True)
                            
                    
                    
                    ## 안겹치면 j증가싴켜서 다음행으로넘김
                    
                    if j == len(df_w_11_a)-2:
                        df_w_11_d = df_w_11_d.append(df_w_11_a.iloc[[j+1]], ignore_index=True)
                    
                    else:
                        s1 = df_w_11_a.iloc[j+1,4]                ## 시점이정1

            
                    
        elif len(df_w_11_a) == 2:
            
            bonbu = df_w_11_a.iloc[0,0]
            jisa = df_w_11_a.iloc[0,1]
            
            s1 = df_w_11_a.iloc[0,4]                ## 시점이정1
            s2 = df_w_11_a.iloc[1,4]                ## 시점이정2
            j1 = df_w_11_a.iloc[0,5]                ## 종점이정1
            j2 = df_w_11_a.iloc[1,5]                ## 종점이정2
            
            if s2-j1<=1:
                                    
                
                    is_hang = df_ws['행선'] == hang
                    is_no = df_ws['노선'] == no
                    
                    is_si = df_ws['시점이정'] >= s1
                    is_jong = df_ws['종점이정'] <= j2
                    
                    df_w_11_b = df_ws[is_hang & is_no & is_si & is_jong]
                    
                    mean_RMI = round(df_w_11_b['RMI'].mean(), 2)

                    if mean_RMI > 10:
                        mean_RMI = 10
                    
                    if mean_RMI >= 7:
                        
                        df_w_11_c = pd.DataFrame({"본부":[bonbu], "지사":[jisa], "행선":[hang], "노선":[no], 
                                                "시점이정":[s1], "종점이정":[j2], "연장":[j2-s1], "RMI":[mean_RMI]})
                        df_w_11_d = df_w_11_d.append(df_w_11_c, ignore_index=True)
            
            else:
                df_w_11_d = df_w_11_d.append(df_w_11_a.iloc[[0]], ignore_index=True)
                df_w_11_d = df_w_11_d.append(df_w_11_a.iloc[[1]], ignore_index=True)
                    
                
        else:
            
            df_w_11_d = df_w_11_d.append(df_w_11_a.iloc[[0]], ignore_index=True)



    df_w_11_d = df_w_11_d.drop_duplicates()
            
    df_w_11_e = df_w_11_d[df_w_11_d['연장']>=x]
    df_w_11 = df_w_11_e[df_w_11_e['RMI']>=7]
    df_w_11 = df_w_11.reset_index(drop=True)

    #%% RMI9이상 비율 
    df_w_13 = pd.DataFrame()
    df_w_13_a = pd.DataFrame()
    df_w_13_b = pd.DataFrame()
    df_w_13_c = pd.DataFrame()
    df_w_13_d = pd.DataFrame()


    for i in range(len(df_w_11)):

        
        bonbu = df_w_11.iloc[i,0]
        jisa = df_w_11.iloc[i,1]
        hang = df_w_11.iloc[i,2]
        no = df_w_11.iloc[i,3]
        s1 = df_w_11.iloc[i,4]
        j1 = df_w_11.iloc[i,5]

        is_hang = df_ws['행선'] == hang
        is_no = df_ws['노선'] == no
        
        is_si = df_ws['시점이정'] >= s1
        is_jong = df_ws['종점이정'] <= j1
        
        df_w_13_a = df_ws[is_hang & is_no & is_si & is_jong]
        
        is_rmi = df_w_13_a['RMI']>=9
        is_rmi_8 = df_w_13_a['RMI']>=8
        is_rmi_7 = df_w_13_a['RMI']>=7
        
        x = sum(is_rmi)/10                       # RMI 9이상 연장
        x1 = sum(is_rmi_8)/10
        x2 = sum(is_rmi_7)/10  
        
        y = len(df_w_13_a)/10                      # 자료상 연장
        z = round(x/y*100, 2)                   # 9이상비율(B/A)
        z1 = round(x1/y*100, 2)
        z2 = round(x2/y*100, 2) 
        
        df_w_13_b = pd.DataFrame({"자료상 연장(A)":[y], "RMI 9이상 연장(B)":[x], "RMI 9이상 비율(B/A)":[z]
                                , "RMI 8이상 비율":[z1], "RMI 7이상 비율":[z2]})
        df_w_13_c = df_w_13_c.append(df_w_13_b, ignore_index=True)

    df_w_13_d = pd.concat([df_w_11, df_w_13_c], axis=1)
    df_w_13 = df_w_13_d.sort_values(by=['RMI 9이상 비율(B/A)'], axis=0, ascending=False)
    df_w_13 = df_w_13.reset_index(drop=True)
    df_w_13 = df_w_13.reindex(columns=['본부', '지사', '행선', '노선', '시점이정', '종점이정', '연장',
                                    '자료상 연장(A)', 'RMI 9이상 연장(B)', 'RMI 9이상 비율(B/A)'
                                    ,"RMI 8이상 비율", "RMI 7이상 비율", 'RMI'])
    df_w_13.index += 1

    df_w_13.columns = ['본부', '지사', '행선', '노선', '시점이정', '종점이정', '실제 연장',
                    '자료상 연장(A)', 'RMI 9이상 연장(B)', 'RMI 9이상 비율(B/A)',
                    "RMI 8이상 비율", "RMI 7이상 비율",'평균 RMI']

    df_w_13.to_csv(os.path.join(PROJECT_DIRECTORY_PREFIX, 'static/resources/analysis_result.csv'), encoding= 'euc=kr')


    return df_w_13


if __name__ == '__main__':
    rmi_analysis()