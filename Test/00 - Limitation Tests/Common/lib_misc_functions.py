def rob_centroid(robots):
	x_coords = 0
	y_coords = 0
	for r in robots:
		x_coords = x_coords + r.x
		y_coords = y_coords + r.y
	return (x_coords/len(robots), y_coords/len(robots))
