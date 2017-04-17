#import common_plot as common
import matplotlib.pylab as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap
import numpy as np

def plot_map(ax,diag,coord1,coord2,data,current_date):
	''' single plot '''
	#contours, norm, ticks = common.setup_contour(dict_plot,40)
	#cbarfmt = common.setup_colorbar_fmt(data)

	pal = cm.jet
	# background
        if diag['run']['grid'] == 'CCS1':
                bmap = Basemap(projection='cyl',llcrnrlat=18,urcrnrlat=51,\
                                                llcrnrlon=219,urcrnrlon=251,resolution='l')
                parallels = np.arange(20.,60.,10.)
                bmap.drawparallels(parallels,labels=[True,False,False,True])
                meridians = np.arange(220.,260.,10.)
                bmap.drawmeridians(meridians,labels=[True,False,False,True])
        elif diag['run']['grid'] == 'NWA':
                bmap = Basemap(projection='cyl',llcrnrlat=5,urcrnrlat=55, llcrnrlon=250, \
                                                urcrnrlon=320,resolution='l')
                parallels = np.arange(0.,70.,10.)
                bmap.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
                meridians = np.arange(240.,340.,10.)
                bmap.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
        else:
                pass
        bmap.drawcoastlines()
        bmap.fillcontinents(color='grey',lake_color='white')


	#m = common.setup_map(grd)
        C = ax.contourf(coord1,coord2,data,40,cmap=pal)
        #cbarfmt = common.setup_colorbar_fmt(data)
        #cbar = plt.colorbar(C,format=cbarfmt,shrink=0.8,ticks=ticks)
	fmt = "%Y %m %d"
        plt.title(diag['label'] + ' ' + current_date.strftime(fmt))

	return ax
