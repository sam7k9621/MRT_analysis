#!/bin/env python
import sys
import argparse
import pandas as pd
import numpy as np

def classifyLabel( df, col, big, small ):
    total = df[col].sum()
   
    big = df[col] >= total*big
    sml = df[col] >= total*small
    big = big.astype(int)
    sml = sml.astype(int)

    df["Label_{}".format( col )] = big+sml 
    return df

def SM_Plot( idx ):
    global df
    global df_sm 

    df_d = df[ (df.Time > 5)   & (df.Time < 11) ]
    df_n = df[ (df.Time > 16 ) & (df.Time < 22) ]

    df_sm.loc[idx, "di_count"] += df_d.in_count.sum() 
    df_sm.loc[idx, "do_count"] += df_d.out_count.sum() 
    df_sm.loc[idx, "ni_count"] += df_n.in_count.sum() 
    df_sm.loc[idx, "no_count"] += df_n.out_count.sum() 

def WT_Plot():
    global df 
    global df_wt

    df_wt = pd.concat([df_wt, df], ignore_index=True, sort=False)

def main(args):
    parser = argparse.ArgumentParser("")
    parser.add_argument( '-d', '--date', nargs="+" )
    parser.add_argument( '-m', '--make', help='make json', action='store_true' )
    parser.add_argument( '-o', '--output', default="/wk_cms2/sam7k9621/MRT_analysis/MRT_crawl" )
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
    
    global df
    global df_sm 
    global df_wt
    global df_pi

    df_wt = pd.DataFrame( columns=[ "Date", "Time", "Weekday", "in_count", "out_count", "Temp", "Drop", "R_label" ] )
    df_pi = pd.DataFrame( columns=[ "Date", "Time", "Weekday", "in_count", "out_count", "Temp", "Drop", "R_label" ] )
    df_sm = pd.DataFrame(0, index=np.arange(0, stat_df.shape[0]), columns=["Station", "di_count", "do_count", "ni_count", "no_count" ])

    # https://blog.csdn.net/haolexiao/article/details/81180571
    df_sm.Station.astype(str)
    df_sm.loc[:, 'Station'] = stat_df.Zh_tw
   
    for idx, (station_zh, station_en) in enumerate( zip( stat_df["Zh_tw"], stat_df["En"] ) ):       
        for date in opt.date:
            station_en = station_en.replace(" ", "_").replace("/", "_").replace(".", "") 
            df = pd.read_csv("results/{}_{}.csv".format( date, station_en) ) 

            # Cut on weekday
            df = df[ df.Weekday < 5]
            
            # Split into day and night
            df = df[ ( (df.Time > 5) & (df.Time < 11) ) | (df.Time > 16 ) & (df.Time < 22) ]
            SM_Plot( idx )
            WT_Plot()

        df_wt.to_csv( "results/Weather_{}_{}.csv".format( station_en, "-".join(opt.date)), index=False )
        df_wt = df_wt.iloc[0:0]

    df_sm = classifyLabel( df_sm, "do_count", 0.02, 0.005 )
    df_sm = classifyLabel( df_sm, "no_count", 0.02, 0.005 )
    df_sm.to_csv( "results/Label_{}.csv".format("-".join(opt.date)), index=False )

if __name__ == '__main__':
    main(sys.argv)
