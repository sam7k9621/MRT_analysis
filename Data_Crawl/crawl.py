#!/bin/env python3
import os
import sys
import argparse
import requests
import progressbar as pg
from bs4 import BeautifulSoup
from pathlib import Path
from pyunpack import Archive

def main(args):
    parser = argparse.ArgumentParser("")
    parser.add_argument( '-t', '--test', help='testing command', action='store_true' )
    parser.add_argument( '-i', '--inputfile' )

    try:
        opt = parser.parse_args(args[1:])
    except:
        parser.print_help()
        raise

    with open( "data/{}".format( opt.inputfile ) ) as input:
        content = input.readlines()
        content = [ x.strip() for x in content if x.strip() ]

    cmd_get = "wget --quiet --output-document {}/{}.zip {}"
    cmd_rm  = "rm {}/{}.zip"
    save_dir = "/wk_cms2/sam7k9621/MRT_analysis/MRT_crawl/precut" 
    if not os.path.exists( save_dir ):
        os.makedirs( save_dir )
    
    url = "http://163.29.157.32:8080/dataset/98d67c29-464a-4003-9f78-b1cbb89bff59"
    re = requests.get( url )
    soup = BeautifulSoup(re.text, 'html.parser')

    widgets = [ pg.Timer(), " ", pg.AdaptiveETA(), " | ", pg.SimpleProgress(), " ", pg.Bar(), "[", pg.Percentage(), "]" ]
    pbar = pg.ProgressBar(widgets=widgets, maxval=len(content)).start()

    for idx, chose_date in enumerate(content):
        tag = soup.find( title="臺北捷運每日分時各站OD流量統計資料_{}".format( chose_date ) )
        date = tag.get("title").split("_")[-1]
        url2 = "http://163.29.157.32:8080" + tag.get("href")
        re2 = requests.get( url2 )
        soup2 = BeautifulSoup( re2.text, "html.parser" )
        filepath = soup2.find( "a", class_="btn btn-primary resource-url-analytics resource-type-None" ).get("href")
        os.system( cmd_get.format( save_dir, date, filepath ) )
        Archive( "{}/{}.zip".format( save_dir, date ) ).extractall( save_dir )
        os.system( cmd_rm.format( save_dir, date ) ) 
        pbar.update(idx+1)
    pbar.finish()
    
    csvlst = os.listdir( save_dir )
    for csv in csvlst:
        csvpath = Path( save_dir + "/" + csv )
        csvpath.rename( save_dir + "/" + csv.split("_")[-1] )

if __name__ == '__main__':
    main(sys.argv)
