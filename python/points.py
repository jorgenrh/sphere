# -*- coding: utf-8 -*-


# http://web.archive.org/web/20120107030109/http://cgafaq.info/wiki/Evenly_distributed_points_on_sphere

import sys
import numpy as np 
import coord

args = sys.argv[1:]
num_args = len(args)


alg = ["rusin", "goldensection", "saffkuijlaars"]

if num_args < 2:
	exit("points.py <%s> <num points> [outputfile]" % "|".join(alg))

algorithm = sys.argv[1]

if algorithm not in alg: 
	exit("points.py <%s> <num points> [outputfile]" % "|".join(alg))

num_points = sys.argv[2]

fname = False
if num_args > 2:
	fname = sys.argv[3]


def golden_section(N):
	"""
	http://www.softimageblog.com/archives/115
	"""
	N = float(N)

	inc = np.pi * (3 - np.sqrt(5))
	off = 2 / N
    
	k = np.arange(N)
	phi = k * inc
	y = k * off - 1 + (off / 2)
	r = np.sqrt(1 - y**2)
	x = np.cos(phi) * r
	z = np.sin(phi) * r

	return x, y, z, len(x)


def saff_kuijlaars(N):
	k = np.arange(N)
	h = -1 + 2 * k / (N - 1)
	theta = np.arccos(h)
	phi = np.zeros_like(h)
	for i in range(1, N - 1):
		phi[i] = (phi[i - 1] + 3.6 / np.sqrt(N * (1 - h[i]**2))) % (2 * np.pi)

	x,y,z = coord.sph2car(theta, phi)

	return x, y, z, len(x)


def saff_kuijlaars2(N):

	N_count = 2
	N = float(N)

	s = 3.6 / np.sqrt(N)
	phi = 0
	x_l = [0]
	y_l = [-1]
	z_l = [0]
	for k in range(1, int(N)-1):
		y = -1 + 2 * k / (N-1)
		r = np.sqrt(1 - y**2)
		phi = phi + s / r
		x_l.append(np.cos(phi)*r)
		y_l.append(y)
		z_l.append(np.sin(phi)*r)

	x_l.append(0)
	y_l.append(1)
	z_l.append(0)

	return np.array(x_l), np.array(y_l), np.array(z_l), len(x_l)


def rusin_disco(vn):

	N_count = 2
	N = 0

	for N in range(1, int(vn)):
		expected_pts = 2.0 - ((2.0*N * np.sin(np.pi/N))/(np.cos(np.pi/N) - 1.0))
		print N, ' -> ', expected_pts
		if (expected_pts >= float(vn)): 
			break

	x_l = [0]
	y_l = [0]
	z_l = [1.0]

	vert_angle = np.pi / N

	for i in range(1, N):

		hori_radius = np.sin(i * vert_angle)
		circle_length = 2.0 * np.pi * hori_radius
		z = np.cos(i * vert_angle)
		point_num_per_circle = np.floor(circle_length / vert_angle)
		hori_angle = 2.0*np.pi/point_num_per_circle

		for j in range(0, int(point_num_per_circle)):

			x = np.cos(j * hori_angle) * hori_radius
			y = np.sin(j * hori_angle) * hori_radius

			x_l.append(x)
			y_l.append(y)
			z_l.append(z)

			N_count = N_count + 1

	x_l.append(0)
	y_l.append(0)
	z_l.append(-1.0)

	return np.array(x_l), np.array(y_l), np.array(z_l), N_count


if algorithm == "rusin":
	x, y, z, num = rusin_disco(num_points)
elif algorithm == "goldensection":
	x, y, z, num = golden_section(num_points)
#elif algorithm == "saffkuijlaars1":
#	x, y, z, num = saff_kuijlaars(num_points)
elif algorithm == "saffkuijlaars":
	x, y, z, num = saff_kuijlaars2(num_points)


if fname:
	f = open(fname,'w')
	for i in range(0, num):
		f.write("%f,%f,%f\n" % (x[i], y[i], z[i]))
	f.close()
else:
	for i in range(0, num):
		print "%f,%f,%f" % (x[i], y[i], z[i])

print num, "points created"




