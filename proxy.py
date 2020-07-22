import argparse
import subprocess
import sys

# Keeps track of whether or not the robot has crashed and needs to reset
crashed = False
state = {
    "crashed" : False,
    "hasLimit" : False
}

movement_commands = ["moveForward", "turnLeft", "turnRight", "wallFront",
                     "wallLeft", "wallRight"]

def invalid_to_send(line):
    if state["crashed"]:
        # Commands to move, turn, or detect walls will be ignored.
        if line.split()[0] in movement_commands:
            sys.stderr.write("Cannot move or detect walls while crashed. Must send ackReset.\n")
            sys.stderr.flush()
            return True
    return False

commands_that_need_response = [
    "mazeWidth",
    "mazeHeight",
    "wallFront",
    "wallRight",
    "wallLeft",
    "moveForward",
    "turnRight",
    "turnLeft",
    "wasReset",
    "ackReset",
]

def needs_response(line):
    """Takes the input line and returns True if the line needs a response from
    the simulator, otherwise returns false."""
    line_start = line.split()[0]
    return line_start in commands_that_need_response

def is_movement_command(line):
    """Takes the input line and returns True if the command was a move or turn,
    otherwise returns false."""
    line_start = line.split()[0]
    return line_start in ["moveForward", "turnRight", "turnLeft"]

def get_distance_plus_turns():
    """Gets the total effective distance plus total turns from the simulator"""
    sys.stdout.write("getStat total-effective-distance\n")
    sys.stdout.flush()
    total_distance = int(sys.stdin.readline())
    sys.stdout.write("getStat total-turns\n")
    sys.stdout.flush()
    total_turns = int(sys.stdin.readline())
    return total_distance + total_turns
    
def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--out", help="file to output the score")
    parser.add_argument("--limit", type=int, help="maximum number of turns plus movements before ending program")
    # TODO Add feature to log score to output file once supported by the simulator API
    # Uncomment those parser arguments once implemented.

    parser.add_argument("command", type=str, nargs="+", help="command that executes the maze-solving program")
    args = vars(parser.parse_args())
    sys.stderr.write(str(args['command'])+'\n')

    # Determine if a limit is invoked
    if args["limit"] is not None:
        state["hasLimit"] = True
        state["limit"] = args["limit"]

    # Launch the subprocess
    proc = subprocess.Popen(args['command'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
    try:
        # Loop until subprocess terminates
        # TODO If possible, add a time limit to terminate the program if it doesn't send a command after more than one second of waiting.
        for line in iter(proc.stdout.readline, b''):
            decode_line = line.decode('utf-8')
            if invalid_to_send(decode_line):
                # Send "crash" if mouse had previously crashed and has not reset.
                proc.stdin.write(b"crash\n")
                proc.stdin.flush()
                continue
            sys.stdout.write(decode_line)
            sys.stdout.flush()
            
            if (needs_response(decode_line)):
                inp = sys.stdin.readline() # Read from simulator
                if (inp == "crash\n"):
                    state["crashed"] = True
                elif (decode_line == "ackReset\n" and inp == "ack\n"):
                    # No longer crashed
                    state["crashed"] = False
                proc.stdin.write(inp.encode('utf-8'))
                proc.stdin.flush()

                # Check if mouse exceeded limit of moves + turns
                if (is_movement_command(decode_line) and state["hasLimit"]
                    and get_distance_plus_turns() > state["limit"]):
                    sys.stderr.write("Maximum movements exceeded\n")
                    sys.stderr.flush()
                    proc.kill()
                    exit(1)
    except:
        sys.stderr.write("exception\n")
        sys.stderr.flush()
        proc.kill()
        raise
    
    # TODO(zdasaro) detect program crash and exit with error so the simulator know the program terminated unexpectedly.

if __name__ == "__main__":
    main()