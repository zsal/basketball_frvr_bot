import subprocess
import time
import sys
import numpy as np
from scipy import misc
import glob

	

## calibrate ##
image_path = "/Users/zanesalem/Desktop/basketball.png"

#rgb of hoop color
hoop = np.array([255,108,0], dtype=np.uint8)

#top left color of game
initx, inity = 700,125

w, h = 450, 900

def get_screen_cap(ret_time=True):
	imgcap_cmd = "screencapture -R%i,%i,%i,%i %s" % (initx, inity, w, h, image_path)
	subprocess.check_output(imgcap_cmd, shell=True)
	start_time = time.time()
	image = misc.imread(image_path)
	return image[:,:,0:3], start_time


def get_hoop_center():
	while True:
		image, captime = get_screen_cap()
		upx,upy,_ = image.shape
		thex, they = [],[]
		for y in range(upy):
			goty=False
			for x in range(upx):
				if (hoop == image[x,y,:]).all():
					thex.append(x)
					they.append(y)
					goty=True
			if goty==False and len(thex):
				print 'early exit'
				break

					#import pdb; pdb.set_trace

		if len(thex) and len(they):
			thex = np.array(thex).mean()
			they = np.array(they).mean()
			return thex, they, captime
		else:
			print "cannot find anything..."
			subprocess.check_output("cliclick c:920,930", shell=True)	


def get_hoop_velocity():
	thex_hist, they_hist = [-1,-1], [-1,-1]
	print('collecting screen image for velocity...')
	thex, they, captime = get_hoop_center()
	thex2, they2, captime2 = get_hoop_center()

	time_passed = captime2 - captime
	x_vel = (thex2-thex)/time_passed
	y_vel = (they2-they)/time_passed
	return x_vel, y_vel


def get_throw_point(use_vel):
	center = 205


	if use_vel:
		velx, vely = get_hoop_velocity()
	else:
		velx, vely = 0, 0


	thex, they, _ = get_hoop_center()

	#if abs(they - center) > 22:
	
	#	they = np.array([they, they, center]).mean()
	xhoop = initx+they+10+vely
	yhoop = inity+thex+velx

	print 'hoop:', xhoop, yhoop
	m =  (yhoop - 930) / ((xhoop - 920)*1.0)
	print m


	return 920 + int((xhoop-920)/m), 800 #hoop assymetric color bias


def throw_ball(use_vel):
	throwx, throwy = get_throw_point(use_vel)
	print throwx, throwy
	subprocess.check_output("cliclick c:920,930 w:50 c:920,930 w:50 dd:920,900 du:%i,%i" \
								%  (throwx, throwy), shell=True)	


def main():
	theround = 0

	while True:
		if theround<5:
			throw_ball(False)
		else:
			throw_ball(True)
		time.sleep(.5)
		theround+=1



if __name__ == '__main__':

	print 'number of args:', len(sys.argv)
	if len(sys.argv) > 1: #calibrate mode
		while True:
			cur_mouse = subprocess.check_output("cliclick p:'.'", shell=True).split(':')[-1][1:]
			cur_color = subprocess.check_output("cliclick cp:%s" % cur_mouse, shell=True)
			print cur_mouse, cur_color
			time.sleep(1.1)
	else:
		main()