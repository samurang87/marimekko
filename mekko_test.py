# -*- coding: utf-8 -*-

import mekko 
import pandas as pd

# -----------------------------------------------------------------------------------------------
# GET THE DATA
# Data needs to have this structure: First row label| Second row label |some columns of kpis to plot, choose one at a time|a column for the colour kpi
# -----------------------------------------------------------------------------------------------

data = pd.io.parsers.read_csv("data.csv", dtype = object) # insert file path

# -----------------------------------------------------------------------------------------------
# SET THE VARIABLES
# Make sure that the variables correspond to the right column names
# -----------------------------------------------------------------------------------------------

level1 = "Ice cream type"
level2 = "Flavour"

kpi = "Revenues" #Insert the kpi (column title) corresponding to the height of the boxes

kpiColor = "Quantity sold" # Insert the kpi (column title) corresponding to the colour shading


# -----------------------------------------------------------------------------------------------
# EXECUTE
# -----------------------------------------------------------------------------------------------

mekko.mekko(data = data, level1 = level1, level2 = level2, kpi = kpi, kpiColor = kpiColor)

