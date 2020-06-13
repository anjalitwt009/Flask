from flask import render_template, url_for, flash, redirect, request, abort,jsonify
from Exp_code import app
from werkzeug.utils import secure_filename
import pandas as pd
import csv
import os
from datetime import datetime
import json, json2html
UPLOAD_FOLDER = r'C:\Users\user\PycharmProjects\New folder'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file1 = request.files['file1']

        if (file and allowed_file(file.filename)) and (file1 and allowed_file(file1.filename)):
            filename = secure_filename(file.filename)
            filename1 = secure_filename(file1.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

            return redirect(url_for('analyze'))

    return render_template('home.html')


@app.route("/analyze")
def analyze():
    upload_time = datetime.utcnow()
    for files in os.listdir(r"C:\Users\user\PycharmProjects\New folder"):
        if files.endswith(".csv"):
            df = pd.read_csv(r"C:\Users\user\PycharmProjects\New folder\data.csv")
            lookup_df = pd.read_csv(r"C:\Users\user\PycharmProjects\New folder\lookup.csv")

            rows_before= len(df.index)

            data_df2 = df.drop_duplicates(keep ='last' )

            rows_after = len(data_df2.index)

            data_df_new = data_df2.merge(lookup_df, how='left')
            data_df_new = data_df_new.rename({'Sale Type': 'SaleType_Clean'}, axis=1)
            data_df_new = pd.DataFrame(data_df_new)

            data_df_new.to_csv(r"C:\Users\user\PycharmProjects\New folder\SalesFile.csv")

            earliest_date = data_df_new['AccountingDate'].min()
            recent_date = data_df_new['AccountingDate'].max()

            number_of_rows_removed= rows_before - rows_after

            numerical = ['FIIncome', 'GrossProfit']
            data_df_stat=data_df_new[numerical]
            stats=data_df_stat.describe()
            stats=pd.DataFrame(stats)

            data_df_new.sort_values(by='AccountingDate', ascending=True, inplace=True)
            data_df3 = data_df_new
            data_df3.index = pd.to_datetime(data_df3['AccountingDate'])
            data_df3.index.names = ['Date']
            data_df3.drop(['AccountingDate'], axis=1, inplace=True)
            data_df3.sort_values(by='Date', ascending=True, inplace=True)

            data_pt=[]
            df1 = data_df_new.loc['2017-7-1':'2017-7-31', data_df_new.columns.get_loc('DealNo')]
            df2 = data_df_new.loc['2017-8-1':'2017-8-31', data_df_new.columns.get_loc('DealNo')]
            df3 = data_df_new.loc['2017-9-1':'2017-9-30', data_df_new.columns.get_loc('DealNo')]
            df4 = data_df_new.loc['2017-10-1':'2017-10-31', data_df_new.columns.get_loc('DealNo')]
            df5 = data_df_new.loc['2017-11-1':'2017-11-30', data_df_new.columns.get_loc('DealNo')]
            df6 = data_df_new.loc['2017-12-1':'2017-7-31', data_df_new.columns.get_loc('DealNo')]

            dp1= df1['DealNo'].max()-df1['DealNo'].min()
            data_pt.append(dp1)
            dp2 = df2['DealNo'].max() - df2['DealNo'].min()
            data_pt.append(dp2)
            dp3 = df3['DealNo'].max() - df3['DealNo'].min()
            data_pt.append(dp3)
            dp4 = df4['DealNo'].max() - df4['DealNo'].min()
            data_pt.append(dp4)
            dp5 = df5['DealNo'].max() - df5['DealNo'].min()
            data_pt.append(dp5)
            dp6 = df6['DealNo'].max() - df6['DealNo'].min()
            data_pt.append(dp6)

            return render_template('report.html', upload_time=upload_time,earliest_date=earliest_date,
                                   recent_date=recent_date,number_of_rows_removed=number_of_rows_removed,
                                   tables=[stats.to_html()],data=to_json(data_pt))


