import pytest
import numpy as np
from MineSweeperAI import game

def test_initGame():
	""" Make sure we are able to init a game"""
	mygame = game.minesweeper()
	assert mygame

def test_board_bombs_placed():
	mygame = game.minesweeper(height=16, width=21, bombs=68)
	"""The game should get initialized"""
	assert mygame.height == 16
	assert mygame.width == 21
	assert mygame.bombs == 68
	assert mygame.num_bombs() == 68
	
def test_too_many_bombs():
	with pytest.raises(game.ToManyBombs):
		mygame = game.minesweeper(height=2, width=2, bombs=5)

def test_surrondingSquares():
	mygame = game.minesweeper()
	#Edge Piece
	assert set(mygame.getSurroundingSquares((0,1))) == {(0,0), (0,2), (1,1), (1,2), (1, 0)}
	#Corner Piece
	assert set(mygame.getSurroundingSquares((7,0))) == {(6,0), (6,1), (7,1)}
	#Not corner or edge piece
	assert set(mygame.getSurroundingSquares((5,4))) == {(6,4), (4,4), (5,3), (5,5), (4,3), (4,5), (6, 3), (6, 5)}

def test_BoardSetup():
	mygame = game.minesweeper(100, 100, 2100)
	nonBombs = set(zip(np.where(mygame.board != 9)[0], np.where(mygame.board != 9)[1]))
	for cell in nonBombs:
		surrondingCells = mygame.getSurroundingSquares(cell)
		assert mygame.board[cell] == sum(map(lambda x: x==9, [mygame.board[c] for c in surrondingCells]))
			


