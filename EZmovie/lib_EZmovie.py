import numpy as np
import datetime as dt
import matplotlib.pylab as plt
import netCDF4 as nc
import ezmovie_plots as ezp
import os

# ROMS specific packages
try:
	import pyroms
except:
	print 'pyroms is not installed, will not work with ROMS'

# MITgcm specific packages
try:
	import xarray as xr
	import MITgcmutils
except:
	print 'xarray or MITgcmutils are not installed, will not work with MITgcm '

#------------------------------------------------------------------------------------

class EZmovie():

	def __init__(self,diags,plotdir='./anim/'):
		self.diags = diags
		self.plotdir = plotdir
		self.ncol=0
		self.nrow=0
		self.grd=None
		return

	def ROMS_movie(self,fileout,start_date,end_date,means='no',step=5):

		if (means == 'no'):
			total_days = (end_date -start_date).days
			add_days = np.arange(0,total_days+step,step)
			list_dates = [start_date + dt.timedelta(n) for n in add_days]
		elif (means == 'monthly'):
			# do something else
			pass
		elif (means == 'annual'):
			# do something else
			pass
		else:
			pass

		for current_date in list_dates:
			print 'working on ', current_date.isoformat()
			self.write_one_frame(model='ROMS',current_date=current_date)

		self.make_animated_gif(fileout)
		return

	def MITgcm_movie(self,fileout,start_step,end_step,means='no',delta_step=5):

		if (means == 'no'):
			list_steps = list(np.arange(start_step,end_step+delta_step,delta_step))
		elif (means == 'monthly'):
			# do something else
			pass
		elif (means == 'annual'):
			# do something else
			pass
		else:
			pass

		for current_step in list_steps:
			print 'working on step', current_step
			self.write_one_frame(model='MITgcm',current_step=current_step)

		self.make_animated_gif(fileout)
		return

	def write_one_frame(self,model='ROMS',current_date=None,current_step=None):
		''' write one frame of plots '''
		# arguments check
		if model == 'ROMS' and current_data is None:
			exit('for ROMS model, you must provide a date')
		if model == 'MITgcm' and current_step is None:
			exit('for MITgcm model, you must provide a timestep')

		ccurrent_step = str(current_step).zfill(10)
		# find number of subplots
		for diag in self.diags:
			self.ncol = max(self.ncol,diag['col'])
			self.nrow = max(self.nrow,diag['row'])

		# create figure	
		plt.figure(figsize=[8*self.ncol,8*self.nrow])

		for diag in self.diags:
			this_subplot = diag['col'] + (diag['row'] - 1) * self.ncol
			ax = plt.subplot(self.nrow,self.ncol,this_subplot)
			if model == 'ROMS':
				coord1, coord2, data = self.read_data_roms_esm(diag,current_date)
			elif model == 'MITgcm':
				coord1, coord2, data = self.read_data_mitgcm(diag,current_step)

			if diag.has_key('operation'):
				if diag['operation'] == 'log10':
					data = np.log10(data)
			if diag['type'] == 'map':
				ezp.plot_map(ax,diag,coord1,coord2,data,current_date,ccurrent_step)
			elif diag['type'] == 'section':
				ezp.plot_section(ax,diag,coord1,coord2,data,current_date,ccurrent_step)

		if current_date is not None:
			gifname = self.plotdir + 'frame_' + current_date.isoformat() + '.gif'
			pngname = self.plotdir + 'frame_' + current_date.isoformat() + '.png'
		if current_step is not None:
			gifname = self.plotdir + 'frame_' + str(ccurrent_step) + '.gif'
			pngname = self.plotdir + 'frame_' + str(ccurrent_step) + '.png'

		plt.savefig(pngname,bbox_inches='tight')
		plt.close()
		os.system(' convert ' + pngname + ' ' + gifname)
		os.system(' rm ' + pngname )
		return None

	def make_animated_gif(self,fileout):
		os.system(' rm  ' + self.plotdir + fileout)
		os.system(' gifsicle -d 20 -l ' + self.plotdir + 'frame*.gif -o ' + self.plotdir + fileout)
		os.system(' rm ' + self.plotdir + 'frame*gif')
		return None

	#------------------------- ROMS ----------------------------------
	def read_data_roms_esm(self,diag,current_date):
		''' read the data for each diag '''

		ncfile = diag['run']['directory'] + str(current_date.year) + '/' + diag['run']['name'] + \
		'_' + diag['filetype'] + '_' + current_date.isoformat() + '.nc'
		tmp = self.readnc(ncfile,diag['variable'])

		# load grid first time only
		if self.grd is None:
			self.grd = pyroms.grid.get_ROMS_grid(diag['run']['grid'])
		# reload if different grid (allows multiple grid in one movie)
		if self.grd.name != diag['run']['grid']:
			self.grd = pyroms.grid.get_ROMS_grid(diag['run']['grid'])

		if diag['type'] == 'map':
			if diag.has_key('level') and diag.has_key('depth'):
				exit('you can choose a level or a depth')
			if diag.has_key('level'):
				if len(tmp.shape) == 2:
					# variable is 2d (ssh,...)
					data = tmp
				elif len(tmp.shape) == 3:
					data = tmp[diag['level'],:]

				coord1 = self.grd.hgrid.lon_rho
				coord2 = self.grd.hgrid.lat_rho
			if diag.has_key('depth'):
				data, coord1, coord2 = pyroms.tools.zslice(tmp, diag['depth'], self.grd, \
				                                           Cpos='rho', vert=False, mode='linear')
		elif diag['type'] == 'section':
			if diag.has_key('jindex') and diag.has_key('iindex'):
                                exit('you can choose a section along i or j')
			if diag.has_key('jindex'):
				data, coord2, coord1, coord3 = pyroms.tools.jslice(tmp, diag['jindex'], self.grd)
			if diag.has_key('iindex'):
				data, coord2, coord3, coord1 = pyroms.tools.islice(tmp, diag['iindex'], self.grd)
			pass
		return coord1, coord2, data

	def readnc(self,myfile,myvar,myframe=None):
                ''' read data from netcdf '''
                fid = nc.Dataset(myfile,'r')
                if myframe is None:
                        out = fid.variables[myvar][:].squeeze()
                else:
                        out = fid.variables[myvar][myframe,:].squeeze()
                fid.close()
                return out

	#------------------------- MITgcm ----------------------------------
	def read_data_mitgcm(self,diag,current_step):
		''' '''
		tmp = MITgcmutils.mds.rdmds(diag['run']['directory'] + os.sep + diag['variable'],itrs=current_step)

		if diag['type'] == 'map':
			coord1 = MITgcmutils.mds.rdmds(diag['run']['directory'] + os.sep + 'XC')
			coord2 = MITgcmutils.mds.rdmds(diag['run']['directory'] + os.sep + 'YC')
			if diag.has_key('level'):
				if len(tmp.shape) == 2:
					# variable is 2d (Eta,...)
					data = tmp
				elif len(tmp.shape) == 3:
					data = tmp[diag['level'],:]
			else:
				data = tmp

		elif diag['type'] == 'section':
			print 'not implemented yet'
			pass
		return coord1, coord2, data
