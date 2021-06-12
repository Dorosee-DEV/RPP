from flask import *
from threading import Thread
from multiprocessing import Process, Queue
app = Flask(__name__)
import pandas as pd
import numpy as np
import os
from io import StringIO
import RMI_1
import matplotlib.pyplot as plt
import pandas as pd
import dataframe_image as dfi
import csv

# version
# 21/06/12
filename = 'test12'
year = ''
km = ''

def testexport():
    temp_df = pd.DataFrame({'col1': [7, 8, 9], 'col2': [4, 5, 6]})  ## dataframe을 아무거나 만들어주고,
    temp_df.to_csv('static/resources/' + filename + '.csv', header=False, index=False)
    temp_df.dfi.export('static/images/' + filename + '.png')
    #temp_df.to_html
    return temp_df


@app.route('/')  # 기본 페이지입니다.
def csv_file_download_with_stream():
    return render_template('index.html')


@app.route('/execute')  # 호출이 되면 데이터 프레임을 저장하고 파일 다운 준비상태를 만듭니다.
def execute():
    # output_stream = StringIO()  ## dataframe을 저장할 IO stream
    # temp_df = pd.DataFrame({'col1': [7, 8, 9], 'col2': [4, 5, 6]})  ## dataframe을 아무거나 만들어주고,
    # temp_df.to_csv(output_stream)  ## 그 결과를 앞서 만든 IO stream에 저장해줍니다.
    # temp_df.to_csv('static/resources/' + filename + '.csv', header=False, index=False)
    # temp_df.dfi.export('static/images/' + filename + '.png')
    # response = Response(
    #    output_stream.getvalue(),
    #    mimetype='text/csv',
    #    content_type='application/octet-stream',
    # )
    # response.headers["Content-Disposition"] = "attachment; filename=" + filename + ".csv"
    # global testcsv
    # testcsv = response

    year = request.args.get("year", type=int)
    km = request.args.get("km", type=float)
    df_w_13 = RMI_1.rmi_analysis(year, km)
    # return redirect('/',resultimg=filename)
    # return render_template('test.html', resultimg=testexport())
    return render_template('index.html', resultimg=[df_w_13.to_html(classes='data')], titles=df_w_13.columns.values, resulttest ='1', test1=year, test2=km)
    # return redirect(url_for('csv_file_download_with_stream', resultimg=testexport()))


@app.route('/execute2')  # test용입니다.
def execute2():

    year = request.args.get("year")
    km = request.args.get("km")
    te = testexport()
    return render_template('index.html', resultimg=[te.to_html(classes='data')], titles=te.columns.values, resulttest='1', test1=year, test2=km)


@app.route('/error') # 실행을 누르지않고 export를 누를때 호출됩니다.
def error():
    return render_template('index.html', errorlog='파일이 없습니다.')
    #return redirect(url_for('csv_file_download_with_stream', errorlog='파일이 없습니다.'))


@app.route('/export')  # 호출이 되면 다운로드를 시작합니다.
def export():
    if request.args["resulttest"] == '1':
        file_name = f"static/resources/"+filename+".csv"
        if os.path.isfile(file_name):
            return send_file(file_name, mimetype='application/x-csv',
                     attachment_filename=''+filename+'.csv',  # 다운받아지는 파일 이름.
                     as_attachment=True, cache_timeout=0)
    else:
        return render_template('index.html', errorlog='파일이 없습니다.')
        #return redirect(url_for('csv_file_download_with_stream', errorlog='파일이 없습니다.'))


@app.route('/analysis/result') # export누를시 파일이 다운로드됩니다.
def getResult():
    # RMI_1.rmi_analysis() #다운로드 기능만을 수행해야하기때문에 빠졌습니다.
    if request.args["resulttest"] == '1':
        filePath = f"static/resources/analysis_result.csv"
        if os.path.isfile(filePath):
            return send_file(filePath,
                         mimetype='text/csv',
                         attachment_filename='result.csv',  # 다운받아지는 파일 이름.
                         as_attachment=True, cache_timeout=0)
    else:
        return render_template('index.html', errorlog='getResult()안에서의 오류입니다')
        #return redirect(url_for('csv_file_download_with_stream', errorlog='파일이 없습니다.'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
