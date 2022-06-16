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

The ghost pawn is currently being captured by the black queen, which is not right.
Options & FEN: -uw "8/8/8/8/8/K6q/4P3/8 w - - 0 1"

When no choices are left for a player, an Exception is thrown. In this case we would like to show either a loss or a stalemate.

For demo time end of June 2022
  - En passant capture & promotion: "7k/3p3N/6K1/4P3/8/8/8/8 b"
  - King in check: -uwb "rnb1kbnr/pppp1ppp/8/4p3/6Pq1/5P3/PPPPP2P/RNBQKBNR w"
  - To capture or not to capture

To research (FEN):
  - Does a king capture a queen?