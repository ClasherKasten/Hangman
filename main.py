import curses
import string
import json


SOLUTION = 'Hello World'.lower()
for c in string.punctuation:
   SOLUTION = SOLUTION.replace(c, '')
OUTPUT = SOLUTION
for c in string.ascii_lowercase:
    OUTPUT = OUTPUT.replace(c, '_')
    


def main_window(screen):
    screen.clear()
    screen.addstr('Welcome to Hangman, please press <ENTER> to start or <q> to quit')
    return screen.getkey()
    

def game_window(screen):
    global OUTPUT
    
    with open('hangman.json', 'r') as f:
        hangmans = json.loads(f.read())
    mistakes = 0

    hangman = curses.newwin(9, 11, 0, 0)
    sol = curses.newwin(3, 15, 1, 13)
    user = curses.newwin(3, 3, 5, 13)
    hangman.addstr(1, 1, hangmans[mistakes])
    hangman.box()
    sol.box()
    user.box()
    hangman.refresh()
    sol.refresh()
    user.refresh()

    sol.addstr(1, 2, OUTPUT)
    user.move(1, 1)
    sol.refresh()
    user.refresh()

    while (guess:=user.getkey()) != '\n':
        if guess not in SOLUTION:
            mistakes += 1
            hangman.addstr(1, 1, hangmans[mistakes])
        OUTPUT = list(OUTPUT)
        for i, c in enumerate(SOLUTION):
            if c == guess:
               OUTPUT[i] = c
        if '_' not in OUTPUT:
            screen.clear()
            screen.addstr(f'You win!!! The word was \"{"".join(OUTPUT)}\".')
            screen.refresh()
            break
        OUTPUT = ''.join(OUTPUT)
        sol.addstr(1, 2, OUTPUT)
        sol.refresh()
        user.move(1, 1)
        user.refresh()


def main(stdscr):
    while True:
        key = main_window(stdscr)
        if key == '\n':
            stdscr.clear()
            stdscr.refresh()
            game_window(stdscr)
            stdscr.getch()
        elif key in ['q', 'Q']:
            return 0
        else:
            return 1


if __name__ == '__main__':
    raise SystemExit(curses.wrapper(main))
