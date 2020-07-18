import argparse
import subprocess
import sys

# Keeps track of whether or not the robot has crashed and needs to reset
crashed = False

movement_commands = ["moveForward", "turnLeft", "turnRight", "wallFront",
                     "wallLeft", "wallRight"]

def invalid_to_send(line):
    if crashed:
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
    
def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--out", help="file to output the score")
    # parser.add_argument("--limit", type=int, help="maximum number of turns plus movements before ending program (default 2000)")
    # TODO Add feature to log score to output file once supported by the simulator API
    # TODO Implement limit on number of moves + turns once simulator API
    # supports getting score. Assume for now that the simulator will give this
    # information with the command `getStat totalDistance` and
    # `getStat totalTurns`. After reaching limit, terminate the process.
    # Uncomment those parser arguments once implemented.

    parser.add_argument("command", type=str, nargs="+", help="command that executes the maze-solving program")
    args = vars(parser.parse_args())
    sys.stderr.write(str(args['command'])+'\n')

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
                global crashed
                if (inp == "crash\n"):
                    crashed = True
                elif (decode_line == "ackReset\n" and inp == "ack\n"):
                    # No longer crashed
                    crashed = False
                proc.stdin.write(inp.encode('utf-8'))
                proc.stdin.flush()
    except:
        sys.stderr.write("exception\n")
        proc.kill()
        raise
    
    # TODO(zdasaro) detect program crash and exit with error so the simulator know the program terminated unexpectedly.

if __name__ == "__main__":
    main()