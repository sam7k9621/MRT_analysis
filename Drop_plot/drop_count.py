#!/bin/env python3
import sys
import argparse
import pandas as pd
import ROOT
import constant as plt
import math

def Drop_Label( x ):
    if x < 1:
        return 0.5
    elif x < 3:
        return 1.5
    elif x < 5:
        return 2.5
    elif x < 15:
        return 3.5
    else:
        return 4.5

def Count_Label( x ):
    if abs(x) < 5:
        return math.copysign( 0.5, x ) 
    elif abs(x) < 10:
        return math.copysign( 1.5, x ) 
    elif abs(x) < 20:
        return math.copysign( 2.5, x ) 
    elif abs(x) < 50:
        return math.copysign( 3.5, x ) 
    else:
        return math.copysign( 4.5, x ) 


def main( args ):
    parser = argparse.ArgumentParser("")
    parser.add_argument( '-d', '--date', nargs="+" )
    parser.add_argument( '-s', '--station' )
    
    try:
        global opt 
        opt = parser.parse_args(args[1:])
    except:
        parser.print_help()
        raise

    df = pd.read_csv("output_{}.csv".format( opt.station ) )
    df.Variety *= 100
    df[ "label_var" ]  = df.Variety.apply( Count_Label ) 
    df[ "label_drop" ] = df.Drop.apply( Drop_Label ) 
    
    c = plt.NewCanvas()

    xbin = math.ceil( df.Drop.max() )
    h1= ROOT.TH2D( 'org', "",   xbin, 0, xbin, 40, -100, 100 )
    h2= ROOT.TH2D( 'label', '', 5, 0, 5, 10, -5, 5 )
    
    h1.SetStats( False )
    h2.SetStats( False )
    
    for index, row in df.iterrows():
        h1.Fill( row.Drop, row.Variety )
        h2.Fill( row.label_drop, row.label_var )

    h1.Draw("COLZ")
    h1.GetXaxis().SetTitle("Rain drop [mm] / 1.0")
    h1.GetYaxis().SetTitle("Ridership deviation [%] / 2.5")

    line1 = ROOT.TLine( 1,  -100, 1,  100 )
    line2 = ROOT.TLine( 3,  -100, 3,  100 )
    line3 = ROOT.TLine( 5,  -100, 5,  100 )
    line4 = ROOT.TLine( 15, -100, 15, 100 )

    line5 = ROOT.TLine( 0,  0, xbin,  0 )
   
    for l in [line1, line2, line3, line4, line5]:
        l.Draw("same")
        l.SetLineColor( ROOT.kRed )
        l.SetLineWidth( 1 )
        l.SetLineStyle( 7 )



    plt.SetSinglePadWithPalette( c )
    plt.Set2DAxis( h1 )
    plt.DrawEntryRight( "2019_{}".format( opt.station ) )
    c.SaveAs( "org_{}.pdf".format( opt.station ) )

    h2.Draw("COLZ") 
    h2.GetXaxis().SetTitle("Rain drop label")
    h2.GetYaxis().SetTitle("Ridership deviation label")
    plt.SetSinglePadWithPalette( c )
    plt.Set2DAxis( h2 )
    plt.DrawEntryRight( "2019_{}".format( opt.station ) )
    c.SaveAs( "label_{}.pdf".format( opt.station ) )

    df = df[ (df.label_drop < 1) ]
    print( "Before cut: {}".format( df.Variety.mean() ) )
    df = df[ ( abs(df.Variety) < 50 ) ]
    print( "after  cut: {}".format( df.Variety.mean() ) )


if __name__ == '__main__':
    main(sys.argv)

