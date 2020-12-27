#!/bin/env python
import sys
import argparse
import pandas as pd
import numpy as np


def main(args):
    parser = argparse.ArgumentParser("")
    parser.add_argument( '-d', '--date', required=True, nargs="+" )
    parser.add_argument( '-m', '--make', help='make json', action='store_true' )
    parser.add_argument( '-o', '--output', default="/wk_cms2/sam7k9621/MRT_analysis/MRT_crawl" )
    
    try:
        global opt 
        opt = parser.parse_args(args[1:])
    except:
        parser.print_help()
        raise

    big = 0.02
    sml = 0.005
    stat_df = pd.read_csv("data/MRT_Info2.csv" )
    
    df_merged = pd.DataFrame(index=np.arange(0, stat_df.shape[0]), columns=["Station", "di_count", "do_count", "ni_count", "no_count" ])
    for idx, (station_zh, station_en) in enumerate( zip( stat_df["Zh_tw"], stat_df["En"] ) ):       
        dicount, docount, nicount, nocount = 0, 0, 0, 0 
        
        for date in opt.date:
            station_en = station_en.replace(" ", "_").replace("/", "_").replace(".", "") 
            df = pd.read_csv("results/{}_{}.csv".format( date, station_en) ) 

            # Cut on weekday
            df = df[ df.Weekday < 5]
            
            # Split into day and night
            df_d = df[ (df.Time > 5)   & (df.Time < 11) ]
            df_n = df[ (df.Time > 16 ) & (df.Time < 22) ]

            dicount += df_d.in_count.sum()
            docount += df_d.out_count.sum()
            nicount += df_n.in_count.sum()
            nocount += df_n.out_count.sum()
        
        df_merged.loc[idx] = [station_zh, dicount, docount, nicount, nocount ]

    df_merged = classifyLabel( df_merged, "do_count", big, sml )
    df_merged = classifyLabel( df_merged, "no_count", big, sml )
    df_merged.to_csv("results/Label_{}.csv".format( "-".join( opt.date ) ), index=False)

        

if __name__ == '__main__':
    main(sys.argv)
