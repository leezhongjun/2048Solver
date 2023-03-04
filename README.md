# 2048Solver
[2048](https://play2048.co/) webapp and AI solver in Python

## Demo (not sped up)
![2048-demo](https://user-images.githubusercontent.com/80515759/222767967-dd664566-7852-4cd4-bebb-efd7890492e4.gif)

## Features
 - [Expectimax](https://en.wikipedia.org/wiki/Expectiminimax), an adversarial search for non-deterministic games
 - [Heuristics](https://en.wikipedia.org/wiki/Heuristic_(computer_science))
    - Penalty for non-monotonic columns and rows
    - No. of empty spaces
    - No. of potential merges
    - Large values on the edge
 - Heuristic weights calculated with [CMA-ES](https://en.wikipedia.org/wiki/CMA-ES)
 - [Bitboard](https://en.wikipedia.org/wiki/Bitboard) representation for grid
 - [Transposition table](http://en.wikipedia.org/wiki/Transposition_table) to speed up search
 - [Multithreading](https://en.wikipedia.org/wiki/Multithreading_(computer_architecture))

 ## Potential improvements
 - [N-tuple network](https://en.wikipedia.org/wiki/RAMnets) trained with [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning) for evaluation function
 - Port to a [compiled language](https://en.wikipedia.org/wiki/Compiled_language) for faster performance
 - [Deep neural network](https://doi.org/10.1007/978-3-030-65883-0_5) according to [recent research](https://doi.org/10.2197/ipsjjip.29.336)

### Acknowlegements
 - This [StackOverflow answer](https://stackoverflow.com/a/22498940/1204143) for *What is the optimal algorithm for the game 2048?*
 - [nneonneo/2048-ai](https://github.com/nneonneo/2048-ai) 
 - [ziap/2048-tdl](https://github.com/ziap/2048-tdl)
 - W. Jaśkowski, "Mastering 2048 With Delayed Temporal Coherence Learning, Multistage Weight Promotion, Redundant Encoding, and Carousel Shaping," in IEEE Transactions on Games, vol. 10, no. 1, pp. 3-14, March 2018, doi: 10.1109/TCIAIG.2017.2651887.

### Dependencies
 - flask

### How to use:
1. Run `main.py`

