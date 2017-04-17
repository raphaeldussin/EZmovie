#!usr/bin/env python
from EZmovie import lib_EZmovie as lez
import datetime as dt

run1 = {'grid':'CCS1','name':'CCS1-RD.NVOcobalt29R','directory':'/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt29R/'}
run2 = {'grid':'CCS1','name':'CCS1-RD.NVOcobalt31S','directory':'/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt31S/'}

diag1 = {'label':'SST 2PS',        'run':run1,'variable':'temp','type':'map','level':49,'depth':None,'filetype':'avg','row':1,'col':1}
diag2 = {'label':'Surface Chl 2PS','run':run1,'variable':'chl', 'type':'map','level':49,'depth':None,'filetype':'dia','row':1,'col':2}
diag3 = {'label':'SST 3PS',        'run':run2,'variable':'temp','type':'map','level':49,'depth':None,'filetype':'avg','row':2,'col':1}
diag4 = {'label':'Surface Chl 3PS','run':run2,'variable':'chl', 'type':'map','level':49,'depth':None,'filetype':'dia','row':2,'col':2}

diags = [diag1,diag2,diag3,diag4]

start = dt.datetime(1996,1,2)
end = dt.datetime(1996,1,12)
#end = dt.datetime(1996,12,27)

movie = lez.EZmovie(diags,plotdir='/Volumes/P4/workdir/raphael/Movies_EZ/')
movie('compare_2PS-3PS.gif',start,end)
