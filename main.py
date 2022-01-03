import curses
import string
import json
import requests


with open('hangman.json', 'r') as f:
        hangmans = json.loads(f.read())


def init_colors():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)



def main_window(screen):
    screen.clear()
    screen.addstr(1, 1, 'Welcome to Hangman, please press <ENTER> to start or <q> to quit')
    return screen.getkey()
    

def game_window(screen):
    init_colors()

    solution = requests.get('https://random-word-api.herokuapp.com/word').json()[0]
    for c in string.punctuation:
        solution = solution.replace(c, '')
    output = solution
    for c in string.ascii_lowercase:
        output = output.replace(c, '_')
    mistakes = 0

    hangman = curses.newwin(9, 11, 0, 0)
    sol = curses.newwin(3, 15, 1, 13)
    user = curses.newwin(3, 3, 5, 13)
    for i, line in enumerate(hangmans[mistakes], 1):
        hangman.addstr(i, 1, hangmans[mistakes][i - 1])
    hangman.box()
    sol.box()
    user.box()
    hangman.refresh()
    sol.refresh()
    user.refresh()

    sol.addstr(1, 2, output)
    user.move(1, 1)
    sol.refresh()
    user.refresh()

    while (guess:=user.getkey()) != '\n':
        if guess not in solution:
            mistakes += 1
            for i, line in enumerate(hangmans[mistakes], 1):
                hangman.addstr(i, 1, hangmans[mistakes][i - 1])
            hangman.refresh()
        if mistakes == len(hangmans) - 1:
            screen.clear()
            screen.addstr(f'You lose!!! The word was "{solution}".', curses.color_pair(1))
            screen.refresh()
            break
        tmp_output = list(output)
        for i, c in enumerate(solution):
            if c == guess:
               tmp_output[i] = c
        if '_' not in output:
            screen.clear()
            screen.addstr(f'You win!!! The word was "{solution}".', curses.color_pair(2))
            screen.refresh()
            break
        output = ''.join(tmp_output)
        sol.addstr(1, 2, output)
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
