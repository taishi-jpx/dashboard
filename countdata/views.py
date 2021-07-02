# from django.shortcuts import render

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

import os
import glob
import pandas as pd

DEFAULT_DIR = os.getcwd()
FILE_OUT_DIR = './static/media/'

def index(request):

	#Topページのボタンが押下されると以下の処理を実行する。	
	if request.method == 'POST' and request.FILES['iris_data']:

		#djangoでファイルを扱うオブジェクトを作成する。
		fs = FileSystemStorage()

		#カレントディレクトリをmediaがあるパスに変更する。
		#・・・/dashboard/がデフォルトのカレントディレクトリだが、それを・・・/dashboard/static/media/をカレントディレクトリにする。
		os.chdir(FILE_OUT_DIR)

		#FILE_OUT_DIRにあるファイルを削除する。
		#media配下にあるファイル一覧を取得する。
		file_lst = glob.glob("*")

		#もしファイルが1つ以上あれば、1ファイルずつ削除する。
		if len(file_lst) >= 1:
			for file in file_lst:
				fs.delete(file)

		os.chdir(DEFAULT_DIR)

		#各ファイルのファイル名を変数化する。
		myfile = request.FILES['iris_data']

		#選択されたファイルを./static/media/配下にコピーする。
		myfile_tmp = fs.save(myfile.name, myfile)
		myfile_fix = myfile_tmp

		#./static/media/配下にコピーしたファイルをpandasで読み込んで加工し、同ディレクトリにcsv形式で出力する。
		iris = pd.read_csv(FILE_OUT_DIR + myfile_fix, header=None)
		iris.rename(columns={0:'sepal_length',1:'sepal_width',2:'petal_length',3:'petal_width',4:'class'}, inplace=True)
		#・・・/dashboard/static/media/配下に「iris.csv」を出力する。
		iris.to_csv(FILE_OUT_DIR + 'iris.csv', index=False)

		#irisのclass構成比のcsvを出力する。
		iris_class_compose = iris.groupby('class').count()[['sepal_length']].reset_index()
		iris_class_compose.rename(columns={'sepal_length':'count'}, inplace=True)
		iris_class_compose['sum'] = iris_class_compose['count'].sum()
		iris_class_compose['compose'] = iris_class_compose['count'] / iris_class_compose['sum'] * 100
		#・・・/dashboard/static/media/配下に「iris_class_compose.csv」を出力する。
		iris_class_compose.to_csv(FILE_OUT_DIR + 'iris_class_compose.csv', index=False)
		
		#http://127.0.0.1:8000/result/にアクセスする。
		return redirect('./result')

	#index.htmlを表示する。
	return render(request, 'index.html')

def result(request):

	#result.htmlを表示する。
	return render(request, 'result.html')