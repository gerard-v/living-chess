# Living Chess

Living Chess is a chess engine in which every piece has a will of its own. There is no central point of intelligence.

Interesting aspects of this kind of mechanism are:
  - different motivations to move (for example protecting the king) and the resulting behavior
  - the entire "decision" process that leads to a single move during each turn

The process leading to a single move can have the form of:
  - a lottery
  - a queue
  - a bidding process
  - ...?

The bidding process seems the best candidate of the above, since the others will probably lead to more or less random, unintelligent play.
Note that we should prevent a central point of intelligence somehow sneaking in through the back door.
