#!/bin/env python
import sys
import json
import argparse
import pandas as pd
from functools import reduce 

def csv2df( date ):
    # encoding problem https://stackoverflow.com/questions/17912307/u-ufeff-in-python-string
    with open( "{}/results/{}.csv".format( opt.output, date ), encoding='utf-8-sig' ) as input:
        content = [ ",".join( x.split() ).split(",") for x in input.readlines() ]
        content = [ x for x in content if len(x) == 5 ] 
    
    df = pd.DataFrame( content[2:], columns=content[0] )
    df.rename( columns={ "日期": "Date", "時段": "Time", "進站": "GetIn", "出站": "GetOut", "人次": "Count" }, inplace=True )
    df['Count'] = df['Count'].astype(int)
    return df

def getSubdf( group, label ):
    df = group.sum()
    df.reset_index(inplace=True)
    df.columns = [ "Station", label ]
    return df 

def classifyLabel( row ):
    sun  = row[ "di_count" ] >= row["do_count" ]
    moon = row[ "ni_count" ] >= row["no_count" ]

    if sun and moon:
        return "D"
    elif not sun and moon:
        return "C"
    elif sun and not moon:
        return "B"
    else:
        return "A"

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

    if opt.make:
        df = csv2df( "201911" )
        data = {}
        data["stations"] = list( df.groupby("GetIn").groups )
        
        for s in data["stations"]:
            print( s )
        print( len(data["stations"]))
        return
        with open('{}/data/SampleInfo.json'.format( opt.output ), 'w' ) as outfile:
            json.dump(data, outfile, ensure_ascii=False)
        return

    with open('{}/data/SampleInfo.json'.format( opt.output ), 'r') as infile:
        data = json.load( infile )
        stations = data["stations"]

    for date in opt.date:
        df = csv2df( date )
        
        df_day   = df[ df.Time.str.match("06|07|08|09|10") ]
        df_night = df[ df.Time.str.match("17|18|19|20|21") ]
        
        di_group = df_day.groupby("GetIn")
        ni_group = df_night.groupby("GetIn")
        do_group = df_day.groupby("GetOut")
        no_group = df_night.groupby("GetOut")
  
        dflst = [ getSubdf( x, y ) for x, y in zip([di_group, ni_group, do_group, no_group], ["di_count", "ni_count", "do_count", "no_count" ]) ]

        df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Station'],how='outer'), dflst)

        df_merged["label"] = df_merged.apply(lambda row: classifyLabel(row), axis=1)
        df_merged.to_csv("{}/results/Label_{}.csv".format( opt.output, date ), index=False)
if __name__ == '__main__':
    main(sys.argv)
