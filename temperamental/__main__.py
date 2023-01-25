import pyglet
from .gui import TemperamentalMainGUI

def main():
    main_window = TemperamentalMainGUI()
    pyglet.app.run()

if __name__ == '__main__':
    main()
