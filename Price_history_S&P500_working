#import required packages
#pandas-used for general wrangling
#pandas_datareader-used to scrape data from yahoo
#datetime-used to convert time into unix time (yahoo finance url format uses unix time)
#relativedelta-used to subtract from datetime
#xlsxwriter-used to write dataframe to Excel

#code to import packages
import pandas as pd
import pandas_datareader as web
from datetime import datetime
from dateutil.relativedelta import relativedelta
import xlsxwriter

#get current time
now_time=datetime.now()

#empty dataframe (later appended with temp df through loop)
df_SP500_=pd.DataFrame()

#note that S&P500 price data can only be downloaded for 100 days at once
#loop for each 100 days to overcome this limitation
for i in range(0,18200,100):
    start_time=datetime(now_time.year,now_time.month,now_time.day)-relativedelta(days=i+100)
    end_time = datetime(now_time.year, now_time.month, now_time.day)-relativedelta(days=i)
    temp_df=web.DataReader("^GSPC","yahoo",start_time,end_time)
    if i==0:
        df_SP500_=temp_df
    else:
        df_SP500=pd.concat([temp_df,df_SP500])

#writer object to export dataframe to Excel
writer= pd.ExcelWriter('SP500 price history.xlsx',engine='xlsxwriter')

#write to Excel and save file
df_SP500.to_excel(writer)
writer.save()
