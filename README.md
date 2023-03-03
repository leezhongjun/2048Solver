# 2048Solver
[2048](https://play2048.co/) webapp and AI solver in Python

## Features
 - [Expectimax](https://en.wikipedia.org/wiki/Expectiminimax), an adversarial search for non-deterministic games
 - Heuristics
    - Penalty for non-monotonic columns and rows with [CMA-ES](https://en.wikipedia.org/wiki/CMA-ES)
    - No. of empty spaces
    - No. of potential merges
    - Large values on the edge
 - [Bitboard](https://en.wikipedia.org/wiki/Bitboard) representation for grid
 - [Transposition table](http://en.wikipedia.org/wiki/Transposition_table) to speed up search

 ## Potential improvements
 - [N-tuple network](https://en.wikipedia.org/wiki/RAMnets) trained with reinforcement learning for evaluation function
 - Port to a [compiled language](https://en.wikipedia.org/wiki/Compiled_language) for faster performance
 - 

### Acknowlegements
 - This [StackOverflow answer](https://stackoverflow.com/a/22498940/1204143) for *What is the optimal algorithm for the game 2048?*
 - [nneonneo/2048-ai](https://github.com/nneonneo/2048-ai) 
 - [Temporal difference learning for 2048](https://github.com/ziap/2048-tdl)
 - W. Jaśkowski, "Mastering 2048 With Delayed Temporal Coherence Learning, Multistage Weight Promotion, Redundant Encoding, and Carousel Shaping," in IEEE Transactions on Games, vol. 10, no. 1, pp. 3-14, March 2018, doi: 10.1109/TCIAIG.2017.2651887.

### Dependencies
 - flask
 - numpy

### How to use:
1. Run `main.py`

