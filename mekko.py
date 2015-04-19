# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------
# LIBRARIES
# -----------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import colorsys
from math import floor
from matplotlib import rcParams
from pylab import *
import fractions

# -----------------------------------------------------------------------------------------------
# FUNCTIONS
# colormaps here -> http://matplotlib.org/examples/color/colormaps_reference.html )
# -----------------------------------------------------------------------------------------------



def floored_percentage(val, digits):
    val *= 10 ** (digits + 2)
    return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)


def ColourList(num_colors):
    cm = get_cmap('Blues') # change the value in quotes to the desired color map
    clist = [cm(1.*i/num_colors) for i in range(num_colors)]

    # # Test
    # for i in range(num_colors):
    #     print 1.*i/num_colors 

    return clist


def mekko (data, level1, level2, kpi, kpiColor):


    # 1. Get the color shading
    dfColor = data[[level1, level2, kpiColor]] # Eliminate unnecessary columns if any

    dfColor = dfColor.fillna(0) # Fill blanks with zeroes
    
    dfColor = dfColor.convert_objects(convert_numeric=True) # Convert to numeric, because the data is stored as something else

    dfColor[[kpiColor]] = dfColor[[kpiColor]].astype(int) # Convert floats to integers, necessary to get the color map
    
    # # TEST
    # print dfColor.dtypes

    ncolors = int(dfColor[kpiColor].max() - dfColor[kpiColor].min()) #get the number of colours
    
    maxColor = dfColor[kpiColor].max() # Maximum value of the colour kpi, will be used later

    # # TEST
    # print dfColor[kpiColor].max(), dfColor[kpiColor].min(), ncolors

    valList = dfColor[kpiColor].values.tolist() # Store as list
    
    if 0 in valList:
        colorlist = ColourList(ncolors+1) 

    else:
        colorlist = ColourList(ncolors+2)
        valList.append(0) # zero needs to be there

    valList.sort() # Sort the list, so the zero is in the right place
    
    # # TEST
    # print len(valList) == len(colorlist), len(valList), len(colorlist)

    #colReference = range(dfColor[kpiColor].min(), (dfColor[kpiColor].max()+1)) # Get the range of all possible values associated to colours
    colReference = list(range(dfColor[kpiColor].min(), (dfColor[kpiColor].max()+1))) # Get the range of all possible values associated to colours

    if 0 not in colReference:
        colReference.append(0)
    colReference.sort()
    
    # # TEST
    #print len(colReference) == len(colorlist)
    
    referenceDict = dict(zip(colReference, colorlist))

    dfColor = dfColor.pivot(index=level1, columns=level2, values=kpiColor) #.reset_index()

    dfColor =dfColor.fillna(0)

    dfColor = dfColor.applymap(lambda x: referenceDict[x])

    df = data[[level1, level2, kpi]]
    
    df.loc[:, kpi] = df.loc[:,kpi].convert_objects(convert_numeric=True)
    
    # # TEST
    # print df.dtypes

    total = sum(df[kpi])

    dfCat = df[[level1, kpi]]

    dfCat = dfCat.groupby([level1]).sum()

    dfCatTotals = dfCat

    dfCat = dfCat.applymap(lambda x: (x/total))

    dfCat = dfCat.rename(columns = {kpi: "Width"})

    dfCat = dfCat.reset_index()

    widths = dfCat['Width'].tolist()

    df = df.pivot(index=level1, columns=level2, values=kpi) #.reset_index()

    df = df.fillna(0)

    df = df.apply(lambda x : x / x.sum(), axis=1)   
    
    pos = [0]
    cumulative = 0

    for i in widths[:-1]:
        cumulative += i
        pos.append(cumulative)
   
    counter = 0
    
    xticks = []

    bottoms = [0 for i in range(len(dfCat[level1]))]
   
    fig, axes = plt.subplots()
    
    # Change title as desired; use the version above if you don't have python3
    # plt.title(kpi+" (tot. "+"{0:,.2f}".format(float(dfCatTotals.sum()))+("€").decode('utf-8')+"), darkest shading = max "+kpiColor+" ("+"{0:,.2f}".format(float(maxColor))+")", y = 1.02, size = "medium")
    plt.title(kpi+" (tot. "+"{0:,.2f}".format(float(dfCatTotals.sum()))+("€")+"), darkest shading = max "+kpiColor+" ("+"{0:,.2f}".format(float(maxColor))+")", y = 1.02, size = "medium")

    axes.get_yaxis().set_visible(False)
    axes.set_ylim([0,1])
    
    axes.set_xlim([0,sum(widths)])

    fig.set_size_inches(20,10)
    plt.subplots_adjust(bottom=0.15, top = 0.95)

    for pl in range(len(df.columns)):

        for cat in range(len(dfCat[level1])):

            position = pos[cat]
            width = widths[cat]
            height = df.iat[cat, pl]
            bottom = bottoms[cat]
            color = dfColor.iat[cat,pl]

            # if cat == 1:
            #     print width, height

            xticks.append(position + width/2)

            plt.bar(left = position, height = height, width = width, bottom = bottom, color = color)
            
            if height > 0.05 and width > 0.05:
                textsize =  'medium'
            else:
                textsize = "x-small"

            if height > 0.01 and width > 0.01:
                plt.text(position + width/2, bottom + height/2, df.columns[pl]+"\n"+ floored_percentage(height, 0), ha='center', size = textsize, va = "center")

            bottoms[cat] += height
    
    # Change if necessary; use version above if you don't have python3
    # plt.xticks(xticks, [str.split(u)[0].decode('utf-8')+" - "+"{0:,.2f}".format(float(dfCatTotals.loc[u]))+("€").decode('utf-8') for u in dfCat[level1].tolist()], rotation='vertical', size = "x-small")
    plt.xticks(xticks, [str.split(u)[0]+" - "+"{0:,.2f}".format(float(dfCatTotals.loc[u]))+("€") for u in dfCat[level1].tolist()], rotation='vertical', size = "x-small")

    fig.savefig(kpi+".png", dpi = 100)

    # plt.show()

    plt.clf()




