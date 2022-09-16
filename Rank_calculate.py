def compute_point(winner, loser):
	base_point = 10
	base = 10
	point = base_point + (loser - winner) / base
	new_winner = int(winner + point)
	new_loser = int(loser - point)
	return new_winner, new_loser


