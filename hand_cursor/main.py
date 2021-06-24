import argparse
import time

from cursor import Cursor

def main(args):
	cursor = Cursor()

	while True:
		time.sleep(1)
		cursor.move_rel((1,  0))
		print(cursor.get_position())

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	args = parser.parse_args()
	main(args)