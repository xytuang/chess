import chess
from tables import pawnscore, knightscore, bishopscore, queenscore, rookscore, kingscore_middle, kingscore_end
board = chess.Board()


#simplified evaluation function from https://www.chessprogramming.org/Simplified_Evaluation_Function
def material_eval():
    currColor = board.turn
    #I really want to find a method that returns all the piece types
    #in an array and iterate through it, but I can't find in the python-chess docs
    pawn_score = 0
    knight_score = 0
    bishop_score = 0
    rook_score = 0
    queen_score = 0
    king_score = 0

    pawn_squares = board.pieces(chess.PAWN, currColor)
    knight_squares = board.pieces(chess.KNIGHT, currColor)
    bishop_squares = board.pieces(chess.BISHOP, currColor)
    queen_squares = board.pieces(chess.QUEEN, currColor)
    rook_squares = board.pieces(chess.ROOK, currColor)
    king_squares = board.pieces(chess.KING, currColor)

    if (currColor):
        
        for square in pawn_squares:
            pawn_score += pawnscore[square]

        
        for square in knight_squares:
            knight_score += knightscore[square]
        
        
        for square in bishop_squares:
            bishop_score += bishopscore[square]
        
       
        for square in  queen_squares:
            queen_score += queenscore[square]

        
        for square in rook_squares:
            rook_score += rookscore[square]

        
        for square in king_squares:
            king_score += kingscore_middle[square]
    else:
        for square in pawn_squares:
            pawn_score += pawnscore[chess.square_mirror(square)]

        for square in knight_squares:
            knight_score += knightscore[chess.square_mirror(square)]
        
        for square in bishop_squares:
            bishop_score += bishopscore[chess.square_mirror(square)]
        
        for square in  queen_squares:
            queen_score += queenscore[chess.square_mirror(square)]
        
        for square in rook_squares:
            rook_score += rookscore[chess.square_mirror(square)]

        for square in king_squares:
            king_score += kingscore_middle[chess.square_mirror(square)]

    return pawn_score + knight_score + bishop_score + rook_score + queen_score + king_score    
    

#game playing loop
while (not board.is_checkmate()):
    print(board)
    print(board.legal_moves)
    move = input('Please enter your move: ')
    board.push_san(move)
    print(f'{"Black" if board.turn else "White"}={material_eval()}')






