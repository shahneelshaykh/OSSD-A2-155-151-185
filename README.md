# Battling Knights

This Python program simulates battles between knights in an arena. Knights can move, pick up items, and engage in fights with each other. The program reads a set of movements from an instruction file, updates the state of the arena, and outputs the final state in a JSON file.

## Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/OSSD-A2-155-151-185.git
   cd OSSD-A2-155-151-185

2. **Run the Program**
     python battling_knights.py

     The program reads the movements from the moves.txt file, updates the arena, and generates the final state in a JSON file named final_state.json.

3. **View the Output**
    --> The final state is saved in final_state.json.
    --> Open the JSON file to view the positions, status, equipped items,      attack power, and defense power of each knight.

4. **Instruction File Format** 
    The instruction file (moves.txt) should contain a sequence of movements for each knight. Each movement should be in the format <Knight>:<Direction>, where <Knight> is the knight's name (red, blue, green, yellow), and <Direction> is the movement direction (N, E, S, W).

    GAME-START
    R:S
    R:S
    B:E
    G:N
    Y:N
    GAME-END
   Invalid moves will be ignored, and a message will be printed to the console.

5.  **Final State JSON Format**   
    The output JSON file (final_state.json) follows the format:

    {
  "red": [<R position>, <R status>, <R item (null if no item)>, R Attack, <R Defence>],
  "blue": [<B position>, <B status>, <B item (null if no item)>, B Attack, <B Defence>],
  "green": [<G position>, <G status>, <G item (null if no item)>, G Attack, <G Defence>],
  "yellow": [null, <Y status>, null, 0, 0],
  "magic_staff": [<M position>, false],
  "helmet": [<H position>, false],
  "dagger": [<D position>, false],
  "axe": [<A position>, false]
}

<Knight>: Knight's name (red, blue, green, yellow).
<Knight> position: [Row, Column] position on the board.
<Knight> status: LIVE, DEAD, or DROWNED.
<Knight> item: Equipped item (null if no item).
<Knight> Attack: Knight's attack power.
<Knight> Defence: Knight's defense power.


6. **Notes**
  --> Knights cannot hold more than one item.
  --> Knights that die in battle drop their item.
  --> Knights that drown throw their item to the bank before sinking.

Feel free to reach out if you have any questions or encounter issues. 

**Copy and paste this template into a new file named `README.md` in your project folder. Customize it as needed, providing additional details or clarifications as required by your specific implementation.**
