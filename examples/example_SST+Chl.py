#!usr/bin/env python
from EZmovie import lib_EZmovie as lez
import datetime as dt
import matplotlib.cm as cm

run1 = {'grid':'CCS1','name':'CCS1-RD.NVOcobalt29R','directory':'/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt29R/'}
run2 = {'grid':'CCS1','name':'CCS1-RD.NVOcobalt31S','directory':'/Volumes/P7/ROMS/CCS1/CCS1-RD.NVOcobalt31S/'}

sst      = {'variable':'temp','operation':None,   'type':'map','level':49,'depth':None,'vmin':10,'vmax':30,'filetype':'avg','pal':cm.gist_ncar}
surf_chl = {'variable':'chl', 'operation':'log10','type':'map','level':49,'depth':None,'vmin':-2,'vmax':2, 'filetype':'dia','pal':cm.bwr}

diag1 = {'label':'SST 2PS',           'run':run1,'row':1,'col':1}
diag2 = {'label':'Surface logChl 2PS','run':run1,'row':1,'col':2}
diag3 = {'label':'SST 3PS',           'run':run2,'row':2,'col':1}
diag4 = {'label':'Surface logChl 3PS','run':run2,'row':2,'col':2}

diag1.update(sst)
diag2.update(surf_chl)
diag3.update(sst)
diag4.update(surf_chl)

diags = [diag1,diag2,diag3,diag4]

start = dt.datetime(1996,1,2)
end = dt.datetime(1996,12,27)
#end = dt.datetime(2006,12,30)

movie = lez.EZmovie(diags,plotdir='/Volumes/P4/workdir/raphael/Movies_EZ/')
movie('compare_2PS-3PS.gif',start,end)
