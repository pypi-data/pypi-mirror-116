from setuptools import setup,find_packages

setup(
      name = 'StockPrediction',
      version = '1.0',
      description = 'Use LSTM to predict stock close price',
      author = "Sherlock Xu",
      author_email = 'sherlockjjobs@icloud.com',
      url = 'https://blog.csdn.net/weixin_43456810',
      license = 'LGPL',
      py_modules = ['StockPrediction','__init__'],
      packages= find_packages(),
      )

