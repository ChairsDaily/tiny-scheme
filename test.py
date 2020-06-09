def step (result, x, y, limit):
	if limit <= 0: return result
	if (x + y) % 2 == 0:
		return step(result+(x+y), y, x+y, limit-1)
	else:
		return step(result, y, x+y, limit)
print(step(0, 1, 1, 4))
