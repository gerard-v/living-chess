Notes
- At daybreak & nightfall: pass on vibrations, store in squares
- Vibrations are important not just on squares around you but also on the square where you are
- Friendly vibrations mean safety, or plus points, enemy vibrations are danger or minus points
- Strong pieces should be extra sensitive to enemy vibrations

- Question: should we see the vibrations as continuously present or as events?...
- refactor determination of neighbours for squares
- CRC cards

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

Idea for testing the changed way of propagating, passing ghost pawns (and kings):
Create a FEN with a rook on h3 and a single Pawn that can still move 2 squares forward,
somewhere in the middle, eg on e2 or g2.

When no choices are left for a player, an Exception is thrown. In this case we would like to show either a loss or a stalemate.

For demo time end of August 2022
  - En passant capture & promotion: "7k/3p3N/6K1/4P3/8/8/8/8 b"
  - Ghost pawn is not captured by a queen
  - King in check: -uwb "rnb1kbnr/pppp1ppp/8/4p3/6Pq1/5P3/PPPPP2P/RNBQKBNR w"
  - To capture or not to capture

To research (FEN):
  - Does a king capture a queen? Answer: sometimes.
Examples of capturing a king:
  - -uw "8/8/8/3k4/8/4Q3/8/7K w"
  - -uwb "rnb1kbnr/pppp1ppp/8/4p3/6Pq1/5P3/PPPPP2P/RNBQKBNR w"

Features to add:
  1. All pieces sense if they are attacked (not just the king), and by whom
  2. Improve evaluations for biddings by pieces by including how they are attacked and defended
Example: a queen attacked by a queen is acceptable if she is defended, but a queen attacked by a pawn is probably not acceptable.

