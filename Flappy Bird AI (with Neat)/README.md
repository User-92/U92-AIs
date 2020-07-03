# Description
This is an AI that learns using NEAT (NeuroEvolution of Augmenting Topologies). As the AI learns, it's topology (genome) grows and becomes smarter.

NEAT Documentation: https://neat-python.readthedocs.io/en/latest/

Paper on NEAT: http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf

# Instructions
To create an ai, run the main.py script. The ai will learn how to play Flappy Bird and master it.
When an ai reaches 50, it will create a flapai.txt file.
The txt file will be loaded when you run the test-trained-ai.py script. The ai is no longer learning and will just play the game.
You do not need to delete the old flapai.txt file if you want to create a new ai, the new ai will override the old one.
You can change ai config settings (ex: population size) in the config.txt file in data
If you want to play the game yourself, that will be in data also under the name "gameforhumans.py".

## Requirements
1. pygame
2. neat-python
3. Python 3.7
