#!/bin/env python3
import sys
import argparse
import pandas as pd
import folium
import geopandas
import shapely
import json 
from selenium import webdriver                                                  
from webdriver_manager.chrome import ChromeDriverManager

def Line_Color( line ):
    if "GA" in line:
        return "#a7df72"
    elif "RA" in line:
        return "#fb9a99"
    elif "BR" in line:
        return "#cc8528"
    elif "B" in line:
        return "#2a54ff"
    elif "O" in line:
        return "#ff9e17"
    elif "G" in line:
        return "#33a02c"
    elif "R" in line:
        return "#e34043"
    else:
        print("aaa")
        return "#000000"

def main( args ):
    parser = argparse.ArgumentParser("")
    parser.add_argument( '-d', '--date' )
    parser.add_argument( '-s', '--station' )
    
    try:
        global opt 
        opt = parser.parse_args(args[1:])
    except:
        parser.print_help()
        raise


    option = webdriver.ChromeOptions()                                              
    option.add_argument("headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)          
    driver.set_window_size(1300, 1400) 



    gdf_line = geopandas.read_file("mrt_line.geojson")
    gdf_node = geopandas.read_file("mrt_station.geojson")
    icon_url = "https://i.imgur.com/GZy08h3.png"

    
    for i in range( 24 ):
        line_dict = json.load(open('{}_{}.json'.format( i, opt.date ), encoding='utf-8-sig'))
        m = folium.Map(location=[25.061, 121.515], zoom_start=13, tiles="CartoDB positron", zoom_control=False)
        for idx, row in gdf_line.iterrows():
            # MultiLineString to list
            # https://gis.stackexchange.com/questions/319295/how-to-reverse-the-multilinestring-command-to-a-list-of-arrays
            loc = [list(x.coords) for x in list(row.geometry)][0]
            loc = [ tuple(reversed(x)) for x in loc ]

            weight = line_dict[ row["name"] ] * 2000
            color  = Line_Color( row["Line_No"] )
            folium.PolyLine( loc, color=color, weight=weight, opacity=1).add_to( m )

        for idx, row in gdf_node.iterrows():
            if row["中文站名"] in ["中山", "台北車站", "大安", "板橋", "古亭", "西湖", "西門", "中正紀念堂", "士林", "忠孝新生", "忠孝復興", "淡水", "北投", "蘆洲", "新莊", "三重","江子翠","永安市場", "南港", "景美"]:
                loc = list( reversed( list( row["geometry"].coords )[0] ) )
                icon = folium.features.CustomIcon( icon_url, icon_size=(16, 16) )
                folium.Marker( loc, icon=icon ).add_to( m )

        p0 = [25.163,  121.5945]
        p1 = [25.15,  121.59]
        p2 = [25.165, 121.62]
        folium.Marker( p0, icon=folium.DivIcon( html='<div style="font-size: 40pt; color : black">{:02d}:00</div>'.format(i) )).add_to(m)
        folium.Rectangle([ p1, p2 ], color='#ff7800', fill=True, fill_color='#ffff00', fill_opacity=0.2).add_to(m)

        m.save("{}_{}.html".format( i, opt.date ))
       

        url = "file:///Users/sam/{}_{}.html".format( i, opt.date )
        driver.get( url ) 
        driver.get_screenshot_as_file( "{}_{}.png".format( i, opt.date ) )
        
if __name__ == '__main__':
    main(sys.argv)

