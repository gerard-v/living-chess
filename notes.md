Notes
- Experiment with increasing the bounty for a piece that attacks multiple other pieces at once (eg fork)
- High valued pieces (eg king) are sometimes moving too easyily without reason. Perhaps give them some hesitation.

   i

   7  a8 b8  ..... g8 h8
   .  a7              h7
   .
   .
   .
   .
   .  a2              h2
   0  a1 b1  ..... g1 h1
      0               7  = j


When no choices are left for a player, an Exception is thrown. In this case we would like to show either a loss or a stalemate.

For demo time end of August 2022
  1. Play as human against computer
  2. King gets attacked: -uw "8/8/8/3k4/8/4Q3/8/7K w"
  3. Fool's mate: -uwb "rnb1kbnr/pppp1ppp/8/4p3/6Pq1/5P3/PPPPP2P/RNBQKBNR w"
  4. Fool's mate, white played by computer
  5. En passant capture & promotion: "7k/3p3N/6K1/4P3/8/8/8/8 b"
  6. Ghost pawn does not block vibrations: -uw "8/8/8/8/8/K6q/4P3/8 w - - 0 1"
  
To research (FEN):
  - Does a king capture a queen? Answer: sometimes.
Examples of capturing by a king:
  - -uw "8/8/8/3k4/8/4Q3/8/7K w"
Fool's mate (#1)
  - -uwb "rnb1kbnr/pppp1ppp/8/4p3/6Pq1/5P3/PPPPP2P/RNBQKBNR w"

Features to add:
  1. All pieces sense if they are attacked (not just the king), and by whom
  2. Improve evaluations for biddings by pieces by including how they are attacked and defended
Example: a queen attacked by a queen is acceptable if she is defended, but a queen attacked by a pawn is probably not acceptable.
  3. Castling: 
        a) king not moved + rook not moved
        b) king is not in check
        c) passing square for king is not attacked
        d) destination square for king is not attacked
        e) intermediate squares are empty
  When castling, we could call a method "castle", taking as parameters the direction and the rook to castle with.
  Castling moves now have a bid of 1, we should give this some thought.

Castling possibilities test FEN: "r1b1k2r/p6p/8/8/1B6/8/P6P/4K2R w"