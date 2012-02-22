"""
	ngl.py will make a pyngl plot of the sounding, just for viewing/showing
	
	as with all of this package, this is prefabricated to just give the plot desired
"""
import Ngl
import numpy as np


def skewt(fname, p, tc, tdc, z, wspd, wdir, saveas='png', barbstride=20):
	wks = Ngl.open_wks(saveas,fname)

	dataOpts                               = Ngl.Resources()  # Options describing 
	"""                                                          # data and plotting.
	dataOpts.sktHeightWindBarbsOn          = True             # Plot wind barbs at
                                                          # height levels.
	dataOpts.sktPressureWindBarbComponents = "SpeedDirection" # Wind speed and 
                                                          # dir [else: u,v].

	dataOpts.sktHeightWindBarbPositions  = hght        # height of wind reports
	dataOpts.sktHeightWindBarbSpeeds     = hspd        # speed
                                                   # [or u components]
	dataOpts.sktHeightWindBarbDirections = hdir        # direction
                                                   # [or v components]
	"""

	skewtOpts                              = Ngl.Resources()
	skewtOpts.sktHeightScaleOn             = True      # default is False
	skewtOpts.sktHeightScaleUnits          = "km"    # default is "feet"
	skewtOpts.sktColoredBandsOn            = False      # default is False
	skewtOpts.sktGeopotentialWindBarbColor = "Red"
	dataOpts.sktPressureWindBarbStride     = barbstride
	skewtOpts.tiMainString                 = "Graw Launch WBB - Env. Instr Lab 5"

	# create a background
	skewt_bkgd = Ngl.skewt_bkg(wks, skewtOpts)
	# plot the darn profile...
	skewt_data = Ngl.skewt_plt(wks, skewt_bkgd, p, tc, tdc, z, \
                                wspd, wdir, dataOpts)
	Ngl.draw(skewt_bkgd)
	Ngl.draw(skewt_data)
	Ngl.frame(wks)

	Ngl.end()

def read_plot(savename):
	"""
		This will attempt to read the raw text file using numpy
		to do it quickly.
		
		Only basic text files, no headers can be handled by this code
	"""
	pass
	# this seems like a silly function to have, and I should use NGL simply.
