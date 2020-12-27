#!/bin/env python
# coding=utf-8
import sys
import argparse
import calendar
import pandas as pd
import multiprocessing
import datetime
from dateutil.relativedelta import relativedelta

def run( date, station_zh, station_en ):
    global df
    global wdf
    global opt 

    df_in  = df[ df.GetIn. str.match( station_zh + "$" ) ]
    df_out = df[ df.GetOut.str.match( station_zh + "$" ) ]
    
    df_isum = df_in.groupby (['Date', "Time", 'Weekday']).agg({'Count': 'sum'}).reset_index()
    df_osum = df_out.groupby(['Date', "Time", 'Weekday']).agg({'Count': 'sum'}).reset_index()
    df_isum = df_isum.rename( columns={"Count": "in_count" } )
    df_osum = df_osum.rename( columns={"Count": "out_count" } )
    df_merged = pd.merge(df_isum, df_osum, on = ['Date', 'Time', 'Weekday' ], how = 'right' )
   
    if opt.weather:
        if df_merged.shape != wdf.shape:
            print( "{}_{} is not done, weather and station is not matched".format( date, station_zh ) )
            return
    
        df_merged = pd.concat( [ df_merged.reset_index(drop=True), wdf[ ["Temp", "Drop", "R_label"] ].reset_index(drop=True)], axis=1)

    df_merged.to_csv( "results/{}_{}.csv".format( date, station_en.replace(" ", "_").replace("/","_").replace(".","") ),index=False )
    print( "{}_{} is done".format( date, station_en ) )

def main(args):
    parser = argparse.ArgumentParser("")
    parser.add_argument( '-d', '--date', nargs="+" )
    parser.add_argument( '-w', '--weather', action='store_true' )
    parser.add_argument( '-i', '--inputfile' )
    
    try:
        global opt 
        opt = parser.parse_args(args[1:])
    except:
        parser.print_help()
        raise

    if opt.inputfile:
        with open( "data/{}".format( opt.inputfile ) ) as input:
            content = input.readlines()
            opt.date = [ x.strip() for x in content if x.strip() ]  

    stat_df = pd.read_csv("data/MRT_Info2.csv" )
    weekday  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" ]
   
    weekday_dict = { x: 0 for x in range( 7 ) } 
  
    global df
    global wdf

    for date in opt.date:
        print( "Process {}".format( date ) )
        
        joblst = []
        date_cursor = datetime.datetime.strptime(date, '%Y%m').date() + relativedelta(months=+1)
        date_cursor = pd.Timestamp( date_cursor.strftime("%Y-%m-%d") )

        df = pd.read_csv( "precut/{}.csv".format( date ) )
        
        df = df.drop( df.head(1).index ) 
        dflst = df.iloc[:,0].str.split().tolist()
        dflst = [ x for x in dflst if len(x) == 5 ]
        df = pd.DataFrame( dflst, columns=["Date", "Time", "GetIn", "GetOut", "Count" ] )

        df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
        df['Weekday'] = df['Date'].dt.dayofweek
        df['Count'] = df['Count'].astype(int)
        df['Time'] = df['Time'].astype(int)

        df = df[ (df.Time < 2) | (df.Time > 5) ]
        df = df[ df.Date < date_cursor ]
       
        df_cut = df[ df.Weekday < 5]
        for i in range( 24 ):
            temp = df_cut[ df_cut.Time == i ]        
            temp = temp.groupby(["GetIn", "GetOut"]).agg({"Count": 'sum'}).reset_index()
            temp.to_csv( "results/Pipe_{}_{}.csv".format( i, date ), index=False )
        # df_d = temp[ (temp.Time > 5)   & (temp.Time < 11) ]         
        # df_n = temp[ (temp.Time > 16 ) & (temp.Time < 22) ]
        # df_d = df_d.groupby(["GetIn", "GetOut"]).agg({"Count": 'sum'}).reset_index()
        # df_n = df_n.groupby(["GetIn", "GetOut"]).agg({"Count": 'sum'}).reset_index()
        # df_d.to_csv( "results/Pipe_Day_{}.csv".format( date ), index=False )
        # df_n.to_csv( "results/Pipe_Night_{}.csv".format( date ), index=False )

        if opt.weather:
            wdf = pd.read_csv("weather/{}_{}.csv".format( date[:4], date[4:] ) )

            wdf['Date'] = pd.to_datetime(wdf['Date'], format="%Y/%m/%d")
            wdf.rename( columns={ "Hour":"Time", "Temperature(C)": "Temp", "Rain(mm)": "Drop" }, inplace=True )

            wdf = wdf[ (wdf.Time < 2) | (wdf.Time > 5) ]
            wdf = wdf[ wdf.Date < date_cursor ]

        for station_zh, station_en in zip( stat_df["Zh_tw"], stat_df["En"] ): 
            joblst.append( (date, station_zh, station_en) )   

        print( "Start sending {} jobs".format( date ) )
        with multiprocessing.Pool(processes=18) as pool:
            pool.starmap(run, joblst)
        print( "Finish sending {} jobs".format( date ) )

if __name__ == '__main__':
    main(sys.argv)
