import chess
import chess.svg
from flask import Flask, Response, request
import traceback
import time
import webbrowser
from IPython.display import SVG
import math
from tables import pawnscore, knightscore, bishopscore, queenscore, rookscore, kingscore_middle, kingscore_end
board = chess.Board()

app = Flask(__name__)

#minmax algorithm
def minimax(currMove, depth, alpha, beta, maximizingPlayer):
    if (depth == 0 or board.is_checkmate() or board.is_insufficient_material()):
        return (material_eval(), currMove)
    if maximizingPlayer:
        maxEvaluation = -math.inf
        bestMove = None
        for move in board.legal_moves:
            board.push(move)
            evaluation,_ = minimax(move, depth - 1, alpha, beta, not maximizingPlayer)
            if (evaluation > maxEvaluation):
                maxEvaluation = evaluation
                bestMove = move
            alpha = evaluation if evaluation > alpha else alpha
            if (beta <= alpha):
                board.pop()
                break
            board.pop()
        return (maxEvaluation, bestMove)
    else:
        minEvaluation = math.inf
        bestMove = None
        for move in board.legal_moves:
            board.push(move)
            evaluation,_ = minimax(move, depth - 1, alpha, beta, not maximizingPlayer)
            if (evaluation < minEvaluation):
                minEvaluation = evaluation
                bestMove = move
            beta = evaluation if evaluation < beta else beta
            if (beta <= alpha):
                board.pop()
                break
            board.pop()
        return (minEvaluation, bestMove)


#simplified evaluation function from https://www.chessprogramming.org/Simplified_Evaluation_Function
def material_eval():
    whitescore = 0
    blackscore = 0
    #check for checkmate
    if (board.is_checkmate()):
        if(board.turn == chess.BLACK):
            whitescore = 9999
        else:
            blackscore = -9999
        return whitescore if not board.turn else -blackscore
    
    if (board.is_stalemate() or board.is_insufficient_material()):
        return 0

    #I really want to find a method that returns all the piece types
    #in an array and iterate through it, but I can't find in the python-chess docs
    numberOfWhiteQueens = len(board.pieces(chess.QUEEN, chess.WHITE))
    numberOfBlackQueens = len(board.pieces(chess.QUEEN, chess.BLACK))

    pawn_squares = board.pieces(chess.PAWN, chess.WHITE)
    knight_squares = board.pieces(chess.KNIGHT, chess.WHITE)
    bishop_squares = board.pieces(chess.BISHOP, chess.WHITE)
    rook_squares = board.pieces(chess.ROOK, chess.WHITE)
    queen_squares = board.pieces(chess.QUEEN, chess.WHITE)
    king_squares = board.pieces(chess.KING, chess.WHITE)

    
    for square in pawn_squares:
        whitescore += pawnscore[square]

    for square in knight_squares:
        whitescore += knightscore[square]

    for square in bishop_squares:
        whitescore += bishopscore[square]

    for square in  queen_squares:
        whitescore += queenscore[square]

    for square in rook_squares:
        whitescore += rookscore[square]

    for square in king_squares:
        if (numberOfWhiteQueens == 0 and numberOfBlackQueens == 0):
            whitescore += kingscore_end[square]
        else:
            whitescore += kingscore_middle[square]

    pawn_squares = board.pieces(chess.PAWN, chess.BLACK)
    knight_squares = board.pieces(chess.KNIGHT, chess.BLACK)
    bishop_squares = board.pieces(chess.BISHOP, chess.BLACK)
    rook_squares = board.pieces(chess.ROOK, chess.BLACK)
    queen_squares = board.pieces(chess.QUEEN, chess.BLACK)
    king_squares = board.pieces(chess.KING, chess.BLACK)

    for square in pawn_squares:
        blackscore += pawnscore[chess.square_mirror(square)]

    for square in knight_squares:
        blackscore += knightscore[chess.square_mirror(square)]

    for square in bishop_squares:
        blackscore += bishopscore[chess.square_mirror(square)]
        
    for square in  queen_squares:
        blackscore += queenscore[chess.square_mirror(square)]
        
    for square in rook_squares:
        blackscore += rookscore[chess.square_mirror(square)]

    for square in king_squares:
        if (numberOfWhiteQueens == 0 and numberOfBlackQueens == 0):
            blackscore += kingscore_end[chess.square_mirror(square)]
        else:
            blackscore += kingscore_middle[chess.square_mirror(square)]

    return whitescore if not board.turn else -blackscore

@app.route("/")
def main():
    global board
    ret = '<html><head>'
    ret += '<style>input {font-size: 20px; } button { font-size: 20px; }</style>'
    ret += '</head><body>'
    ret += '<img width=510 height=510 src="/board.svg?%f"></img></br></br>' % time.time()
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit">New Game</button></form>'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit">Undo Last Move</button></form>'
    ret += '<form action="/move/"><input type="submit" value="Make Human Move:"><input name="move" type="text"></input></form>'
    ret += '<form action="/dev/" method="post"><button name="Comp Move" type="submit">Make Ai Move</button></form>'
    return ret
# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')
# Human Move
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        board.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()
# Make Ai’s Move
@app.route("/dev/", methods=['POST'])
def dev():
    try:
        #aimove()
        evaluated, aiMove = minimax(None, 5, -math.inf, math.inf, board.turn)
        board.push(aiMove)
    except Exception:
        traceback.print_exc()
    return main()

# New Game
@app.route("/game/", methods=['POST'])
def game():
    board.reset()
    return main()
# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        board.pop()
    except Exception:
        traceback.print_exc()
    return main()

board = chess.Board()
webbrowser.open("http://127.0.0.1:5000/")
app.run()

#game playing loop for terminal
# while (not board.is_checkmate()):
#     print(board)
#     print(board.legal_moves)
#     move = input('Please enter your move: ')
#     board.push_san(move)
#     evaluated,aiMove = minimax("e7e5", 5, -math.inf, math.inf, False)
#     print(f'AI chose {aiMove}')
#     board.push(aiMove)
#     print(material_eval())