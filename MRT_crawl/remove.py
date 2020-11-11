#!/bin/env python
import sys
import argparse
import pandas as pd

def main(args):
    parser = argparse.ArgumentParser("")
    parser.add_argument( '-t', '--test', help='testing command', action='store_true' )
    parser.add_argument( '-d', '--date' )
    
    try:
        opt = parser.parse_args(args[1:])
    except:
        parser.print_help()
        raise

    save_dir = "/wk_cms2/sam7k9621/MRT_analysis/MRT_crawl/results" 
    
    if opt.test:
        opt.date = "test"
    
    # encoding problem https://stackoverflow.com/questions/17912307/u-ufeff-in-python-string
    with open( save_dir + "/{}.csv".format( opt.date ), encoding='utf-8-sig' ) as input:
        content = [ ",".join( x.split() ).split(",") for x in input.readlines() ]
        content = [ x for x in content if len(x) == 5 ] 

    df = pd.DataFrame( content[1:], columns=content[0] )
    df.rename( columns={ "日期": "Date", "時段": "Time", "進站": "GetIn", "出站": "GetOut", "人次": "Count" }, inplace=True )
    
    df = df[ ( df.GetIn.str.match("台北車站$|松山$|板橋$|南港$") | df.GetOut.str.match("台北車站$|松山$|板橋$|南港$") ) & df.Time.str.match("06|07|18|19") ]
    print( df ) 
    # print( df[ "中山國中" not in df.iloc[:,1:] ] )

    # df.to_csv( save_dir + "/test.csv" ) 
if __name__ == '__main__':
    main(sys.argv)
