from blessed import Terminal


TERMINAL = Terminal()


def get_terminal():
    return TERMINAL


def check_for_terminal(error_msg):
    if not TERMINAL.is_a_tty:
        output = " ".join( line.strip() for line in error_msg.splitlines() )

        print(output)
        quit()