# -*- coding: utf-8 -*-

# J.R.Hoem / jorgen.hoem@gmail.com


import sys, operator
from math import sqrt

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import mpl_toolkits.mplot3d.art3d as art3d

from matplotlib.backends.backend_pdf import PdfPages


args = sys.argv[1:]
num_args = len(args)

if num_args == 0:
	exit("plot.py <filename [filename ...]>")


def get_distance(coords):

	distance = {}

	# finner de 5 narmeste punktene til et punkt
	for idx1, xyz1 in enumerate(coords):
		xyz1 = [float(i) for i in xyz1.split(",")]

		dist = {}

		for idx2, xyz2 in enumerate(coords):
			xyz2 = [float(i) for i in xyz2.split(",")]

			if xyz1[0] == xyz2[0] and xyz1[1] == xyz2[1] and xyz1[2] == xyz2[2]:
				continue 

			d = sqrt( (xyz2[0]-xyz1[0])**2 + (xyz2[1]-xyz1[1])**2 + (xyz2[2]-xyz1[2])**2 )
			dist[idx2] = d

		sorted_dist = sorted(dist.items(), key=operator.itemgetter(1))
		sorted_dist = sorted_dist[:5]
		#print sorted_dist
		distance[idx1] = sorted_dist

	#print distance

	# finner hvilke punkt som har min/max distanse
	min_distance = { "distance":1e5 }
	max_distance = { "distance":-1 }
	for pnt, val in distance.iteritems():
		
		point1 = pnt
		min_d = dict([val[0]])
		min_point2 = min_d.keys()[0]
		min_p2p_dist = min_d.values()[0]
		max_d = dict([val[-1]])
		max_point2 = max_d.keys()[0]
		max_p2p_dist = max_d.values()[0]
		
		if min_p2p_dist < min_distance["distance"]:
			min_distance = { "point1":point1, "point2":min_point2, "distance":min_p2p_dist }

		if max_p2p_dist > max_distance["distance"]:
			max_distance = { "point1":point1, "point2":max_point2, "distance":max_p2p_dist }

	print "Min distance from", min_distance["point1"]+1, "to", min_distance["point2"]+1, ":", min_distance["distance"]
	print "Max distance from", max_distance["point1"]+1, "to", max_distance["point2"]+1, ":", max_distance["distance"]
	
	avvik = max_distance["distance"] - min_distance["distance"]
	print "Avvik :", avvik

	return [min_distance, max_distance], avvik


rows = 1
cols = num_args

if num_args > 3:
	rows = 2
	cols = num_args/2


for n in range(1, num_args+1):

 	fname = sys.argv[n]

	with open(fname) as f:
		coords = f.readlines()

	ax = plt.subplot(rows, cols, n, projection='3d')
	ax.set_aspect('equal')

	x = []
	y = []
	z = []
	xyz1 = 0
	xyz2 = 0

	distance = []

	for idx, c in enumerate(coords):
		c = [float(i) for i in c.split(",")]
		x.append(c[0])
		y.append(c[1])
		z.append(c[2])

		ax.text3D(c[0], c[1], c[2], str(idx+1), color="black", fontsize=10)
	
	ax.scatter3D(x, y, z, marker='o', color='r', s=100)

	print str(fname)
	dist, avvik = get_distance(coords)
	for d in dist:
		p1 = coords[d["point1"]]
		p1 = [float(i) for i in p1.split(",")]
		p2 = coords[d["point2"]]
		p2 = [float(i) for i in p2.split(",")]
		ax.add_line(art3d.Line3D((p1[0],p2[0]), (p1[1],p2[1]), (p1[2],p2[2])))

		mid_p = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2] 
		ax.text3D(mid_p[0], mid_p[1], mid_p[2], str(round(d["distance"],3)), color="b", fontsize=10)

	print ""


	u = np.linspace(0, 2 * np.pi, 100)
	v = np.linspace(0, np.pi, 100)

	x = 0.96 * np.outer(np.cos(u), np.sin(v))
	y = 0.96 * np.outer(np.sin(u), np.sin(v))
	z = 0.96 * np.outer(np.ones(np.size(u)), np.cos(v))
	ax.plot_surface(x, y, z, color="lightgrey", linewidth=0, rstride=4, cstride=4)

	ax.set_title('%s (%d)\navvik: %s' % (str(fname), len(coords), round(avvik,3)))

	ax.set_xlim3d(-1, 1)
	ax.set_ylim3d(-1, 1)
	ax.set_zlim3d(-1, 1)

#pp = PdfPages('multipage.pdf')
#pp.savefig()
#pp.close()
ax.set_aspect('equal')
plt.tight_layout()
plt.show()

