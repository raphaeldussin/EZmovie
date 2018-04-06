#!usr/bin/env python
from EZmovie import lib_EZmovie as lez
import datetime as dt
import matplotlib.cm as cm

run1 = {'grid':'','name':'','directory':'/Users/raphael/WORK/RUNS_MITGCM/tutorial_global_oce_latlon/run'}

sst      = {'variable':'T','type':'map','level':0,'vmin':-2,'vmax':30,'filetype':'','pal':cm.gist_ncar}
sss      = {'variable':'S','type':'map','level':0,'vmin':30,'vmax':40,'filetype':'','pal':cm.gist_ncar}
T500     = {'variable':'T','type':'map','level':7,'vmin':-2,'vmax':10,'filetype':'','pal':cm.gist_ncar}
S500     = {'variable':'S','type':'map','level':7,'vmin':33,'vmax':37,'filetype':'','pal':cm.gist_ncar}

plotting = {'cbar_shrink':0.35}

diag1 = {'label':'SST ','run':run1,'row':1,'col':1}
diag2 = {'label':'SSS ','run':run1,'row':1,'col':2}
diag3 = {'label':'T 1300m ','run':run1,'row':2,'col':1}
diag4 = {'label':'S 1300m ','run':run1,'row':2,'col':2}

diag1.update(sst)
diag2.update(sss)
diag3.update(T500)
diag4.update(S500)

diag1.update(plotting)
diag2.update(plotting)
diag3.update(plotting)
diag4.update(plotting)

diags = [diag1,diag2,diag3,diag4]

movie = lez.EZmovie(diags,plotdir='./')
movie.MITgcm_movie('test_mitgcm.gif',10,360,delta_step=10)
