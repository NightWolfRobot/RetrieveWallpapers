#!/usr/bin/env python
# -*- coding: utf-8 -*-

# C:\Users\USERNAME\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets

import os
import argparse
import shutil
import logging
import struct
import imghdr

def launch (args):
	logger = logging.getLogger(__name__)
	
	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.CRITICAL)
	#print(destination_dir, usr)
	if not os.path.exists(args.dst):
		os.makedirs(args.dst)
	
	if os.path.exists('C:/Users/'+args.user_name+'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'):
		logger.info('Directory path ok, now reading content ...')
		for filename in os.listdir('C:/Users/'+args.user_name+'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'):
			if os.path.isfile('C:/Users/'+args.user_name+'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/'+filename):
				logger.debug('File: '+filename)
				shutil.copy2('C:/Users/'+args.user_name+'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/'+filename, "/"+args.dst+"/"+filename+".png")
		logger.info("Done to copy files")
		if args.rename:	
			renameFiles(args.dst)
		if args.clean:
			cleanRepo(args.dst)
	else:
		logger.critical("No usr like this, please retry")
	
	


# rename all files in the current directory by "wallpaper_NUMBER.ext"
#ADD ARG BOOL FOR THIS
def renameFiles(destination_dir):
	cmpt = 1
	logger = logging.getLogger(__name__)
	logger.info('Start renaming files ...')
	for filename in os.listdir(destination_dir):
		ext = os.path.splitext(filename)[1]
		os.replace(destination_dir+"/"+filename, destination_dir+"/wallpaper_"+str(cmpt)+ext)
		logger.debug('Renamed file -> '+destination_dir+"/wallpaper_"+str(cmpt)+ext)
		cmpt +=1
	logger.info('Done renaming files')

def cleanRepo(destination_dir):
	logger = logging.getLogger(__name__)
	logger.info('Start cleaning repository ...')
	for filename in os.listdir(destination_dir):
		if os.stat(destination_dir+'/'+filename).st_size < 100000:
			os.remove(destination_dir+'/'+filename)
			logger.debug('File removed -> '+destination_dir+'/'+filename)

		elif (not get_image_size(destination_dir+'/'+filename) is None):
			width, height = get_image_size(destination_dir+'/'+filename)
			logger.debug('File: '+filename+'\t| width -> '+str(width)+' \t| '+'height -> '+ str(height))
			if width <= height:
				logger.debug('\t'+filename+' [TO BE REMOVED]')
				os.remove(destination_dir+'/'+filename)
				logger.debug('File removed -> '+destination_dir+'/'+filename)
		else:
			logger.error('Size img = None')

				
	logger.info(' Done cleaning')



def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height


def handleArgs ():
	parser = argparse.ArgumentParser(description="Get hidden wallpapers stored on your Windows")
	parser.add_argument('user_name', type=str, help="Enter the name of your user on Windows")
	parser.add_argument('-d',"--dst", type=str, help="Enter the directory of destination", default="Wallpapers")
	parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true", default=False)
	parser.add_argument("-r", "--rename", help="Rename copied files by wallpaper_XX.png", action="store_true", default=False)
	parser.add_argument("-c", "--clean",action='store_true', default=False, help="Clean repository. Be carefull, it will also wipe out every file under 100ko")
	args = parser.parse_args()
	return args

if __name__=='__main__':
	args = handleArgs()
	#print(args)
	launch(args)
	