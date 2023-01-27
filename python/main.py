import sys
from maze import Maze
import time

def main():
    if len(sys.argv) != 6:
        sys.exit("usage: python main.py filename search_type big_factor play delay")
    filename = sys.argv[1]
    search_type = sys.argv[2]
    try:
        big = int(sys.argv[3])
        play = int(sys.argv[4].lower())
        delay = float(sys.argv[5])
    except ValueError:
        sys.exit("big_factor must be an integer\nplay must be a 0 or 1\ndelay must be a float")

    maze = Maze(filename)

    print("Maze:\n")
    print(maze.print(big))
    print(f"dims : {maze.dims}")
    print(f"start: {maze.start}")
    print(f"goal : {maze.goal}")
    print("Searching...")
    if search_type == "breadth":
        maze.breadth_search()
    elif search_type == "depth":
        maze.depth_search()
    elif search_type == "greedy":
        maze.greedy_search()
    elif search_type == "astar":
        maze.astar_search()
    elif search_type == "random":
        maze.random_search()
    else:
        sys.exit("search_type must be breadth, depth, greedy, astar, or random")
        
    print("Solution is:")
    actions, cells = maze.solution
    print(f"Actions: {actions}")
    print(f"Cells:   {cells}")


    if play:
        print("Replaying solution:")
        for state in cells:
            time.sleep(delay)
            print("-" * 20)
            print(maze.print_state(state, big))
        print("Finished.")

    
  
if __name__ == "__main__":
        main()
