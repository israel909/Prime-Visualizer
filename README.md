# Prime-Visualizer
Python visualization tool for the Sieve of Eratosthenes. Draws the found primes in red and the "sieved" composites in blue.

## Author
Made by Israel Kwilinski using the Pyglet library. 

## What is the Sieve of Eratosthenes?
The Sieve of Erathosthenes is an algorithm for primes (and composites) from 2 to a given limit. It was developed in Ancient Greece by Eratosthenes, a greek mathematician. 

## How does it work?
First a list of numbers 2, 3, ..., LIMIT is created and no numbers are initially crossed out. Let's set LIMIT = 15 for a simple example.
The first number not crossed out is 2, so 2 is prime. Thus, we can mark 2 as prime, 
Then we can proceed to cross out the numbers that are multiples of 2 starting from 4 (this is the "sieving" step).
Our list now looks list: 2 3 ~~4~~ 5 ~~6~~ 7 ~~8~~ 9 ~~10~~ 11 ~~12~~ 13 ~~14~~ 15
The next number that is not crossed out is 3. Thus we mark 3 as prime and remove all the multiples of 3.
Our list now looks list: 2 3 ~~4~~ 5 ~~6~~ 7 ~~8~~ ~~9~~ ~~10~~ 11 ~~12~~ 13 ~~14~~ ~~15~~
The next number is not crossed out is 5. Since 5^2 > 15 (ie. our LIMIT) we can conlude that all of the remaining numbers that are not crossed out are primes.
Conversely we can conclude that all of the crossed numbers are composite. 

## How do you use the program?
The program can be from the command: `python3 sieve.py [-h] [--frame-rate FRAME_RATE] [--dimensions DIMENSIONS]`.
FRAME_RATE gives the user the ability to control of speed the animation. DIMENSIONS controls the canvas dimensions that animation is drawn on.
Default frame rate is 12 squares per second. Default window size is 800x800.
If a `ModuleNotFoundError` is encountered please try `pip install numpy pyglet`.

## Additonal Controls
This program enables keyboard-based control. By pressing a number key between `1` to `9` the grid will be redrawn to be larger or smaller and the animation will start over. The starting grid size is 10x10 (from 1 to 100). The maximum grid size is 18x18 (from 1 to 324). 
The program ends when the `Q` key is pressed.
