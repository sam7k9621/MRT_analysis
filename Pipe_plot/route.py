#!/bin/env python3
# coding=utf-8

import re
import sys
import json
import pandas as pd
import argparse
from dijkstra import DijkstraSPF
from dijkstra import Graph
from string import ascii_letters 

def Find_Path( start, end ):
    global station_dict
    global graph

    score = float("inf")
    path  = []
    for s in station_dict[ start ]:
        dijkstra = DijkstraSPF( graph, s )

        for e in station_dict[ end ]:
            value = dijkstra.get_distance( e )
            if value <= score:
                score = value 
                path  = dijkstra.get_path( e ) 
    
    path = list( dict.fromkeys( [ x.lstrip(ascii_letters) for x in path ] ) )
    return score, path

def Add_Edge( x1, x2, graph, value ):
    graph.add_edge( x1, x2, value )
    graph.add_edge( x2, x1, value )

def main(args):
    parser = argparse.ArgumentParser("")
    parser.add_argument( '-d', '--date' )
    parser.add_argument( '-s', '--station' )
    
    try:
        global opt 
        opt = parser.parse_args(args[1:])
    except:
        parser.print_help()
        raise

    df = pd.read_csv("northern-taiwan.csv" )

    # Declare global variable
    global station_dict
    global graph

    # Setup station map
    station_dict = {}
    score_dict   = {}
    stat_df = df.groupby("station_name_tw")["line_code"].apply(list).reset_index()
    for name, line in zip( stat_df.station_name_tw, stat_df.line_code ):
        station_dict[ name ] = [ x+name for x in line]

    # Setup station graph
    graph = Graph()
    MRT_line = ["R", "BR", "G", "O", "BL"]
    for line in MRT_line:
        temp = df[ df.station_code.str.match( "{}[0-9]+$".format( line ) ) ]
        namelst  = temp.station_name_tw.tolist()
        codelst  = temp.station_code.tolist()
        lst = [x+y for x, y in zip( codelst, namelst)]
       
        # Avoid the last element
        for t, n in zip( lst[:-1], lst[1:]):
            tid = re.search(r'\d+', t).group() 
            nid = re.search(r'\d+', n).group()
            if int(tid) + 1 != int(nid):
                continue
            t, n = t.replace( tid, "", 1 ), n.replace( nid, "", 1 )
            score_dict[ "{}-{}".format(t.lstrip(ascii_letters), n.lstrip(ascii_letters)) ]   = 0
            score_dict[ "{}-{}".format(n.lstrip(ascii_letters), t.lstrip(ascii_letters)) ]   = 0

            graph.add_edge( t, n, 1 )
            graph.add_edge( n, t, 1 )
   
    Add_Edge( "R中山", "G中山",                 graph, 0.5 )
    Add_Edge( "R中正紀念堂", "G中正紀念堂",     graph, 0.1 )
    Add_Edge( "BR南京復興", "G南京復興",        graph, 1.5 )
    Add_Edge( "BR南港展覽館", "BL南港展覽館",   graph, 0.5 )
    Add_Edge( "G古亭", "O古亭",                 graph, 0.1 )
    Add_Edge( "R台北車站", "BL台北車站",        graph, 1.5 )
    Add_Edge( "BR大安", "R大安",                graph, 1.5 )
    Add_Edge( "BR忠孝復興", "BL忠孝復興",       graph, 1.5 )
    Add_Edge( "O忠孝新生", "BL忠孝新生",        graph, 0.5 )
    Add_Edge( "R東門", "O東門",                 graph, 0.5 )
    Add_Edge( "G松江南京", "O松江南京",         graph, 1.5 )
    Add_Edge( "R民權西路", "O民權西路",         graph, 0.5 )
    Add_Edge( "G西門", "BL西門",                graph, 0.5 )

    Add_Edge( "R北投", "R新北投",               graph, 1 )
    Add_Edge( "G七張", "G小碧潭",               graph, 1 )
    Add_Edge( "O大橋頭站", "O三重國小",         graph, 1 )
            
    score_dict[ "{}-{}".format( "北投","新北投" ) ]  = 0
    score_dict[ "{}-{}".format( "新北投","北投" ) ]  = 0
    score_dict[ "{}-{}".format( "七張", "小碧潭" ) ] = 0
    score_dict[ "{}-{}".format( "小碧潭","七張" ) ]  = 0
    score_dict[ "{}-{}".format( "大橋頭站", "三重國小" ) ] = 0
    score_dict[ "{}-{}".format( "三重國小", "大橋頭站" ) ]  = 0


    print( Find_Path( "東門",   "南京復興" ) )
    print( Find_Path( "善導寺", "南京復興" ) )
    return

    for i in range( 24 ):
        df = pd.read_csv("Pipe_{}_{}.csv".format( i, opt.date ))
  
        for start, end, weight, in zip( df.GetIn, df.GetOut, df.Count ):
            score, path = Find_Path( start, end )
            for t, n in zip( path[:-1], path[1:] ):
                score_dict[ "{}-{}".format( t, n ) ] += weight 
                score_dict[ "{}-{}".format( n, t ) ] += weight 
            
        total = sum(score_dict.values(), 0.0) / 2
        score_dict = {k: 0 if v == 0 else v / total for k, v in score_dict.items() }
    
        with open('{}_{}.json'.format( i, opt.date ), 'w', encoding='utf-8-sig') as f:
            json.dump(score_dict, f, indent=4, ensure_ascii=False)

        score_dict = dict.fromkeys( score_dict, 0 )

if __name__ == '__main__':
    main(sys.argv)
