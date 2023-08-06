import sys
import termios
import tty
import io
import os
from .placeholder import PlaceHolder


class MoreIOError(IOError):
    pass


class MoreAttributeError(AttributeError):
    pass


class More:
    def __init__(
        self,
        output,
        placeholder=None,
    ):
        self.placeholder = placeholder
        if not sys.stdin.isatty():
            raise MoreIOError(
                "stdin must be tty."
            )
        if not sys.stdout.isatty():
            raise MoreIOError(
                "stdout must be tty."
            )

        self._buffer = io.StringIO(
            initial_value=output,
            newline="\n"
        )
        self._buffer_lines = self._buffer.getvalue().splitlines()
        self._oldattr = termios.tcgetattr(sys.stdin.fileno())
    
    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        if type(value) is not PlaceHolder and \
                value is not None:
            raise TypeError(
                "placeholder must be PlaceHolder class."
            )
        self._placeholder = value
        

    def _flush_screen(self):
        sys.stdout.write("\033[2J\033[H")

    def _terminal_size(self):
        columns, lines = os.get_terminal_size()
        return columns, lines

    def _terminal_full_size(self):
        columns, lines = self._terminal_size()
        return columns * lines

    def _termline(self, lines, placeholder="hello", brank_lines=1):
        _placelines = len(placeholder.splitlines())
        return lines - _placelines - brank_lines

    def print(self):
        self._setcbreak()
        now_line = 0
        buffer_lines = self._buffer_lines
        try:
            while True:
                self._flush_screen()
                columns, lines = self._terminal_size()
                _scrlines = list()
                for line in buffer_lines[now_line:]:
                    if len(line) > columns:
                        _scrlines.append(line[:columns])
                        _scrlines.append(line[columns:])
                    else:
                        _scrlines.append(line)

                if self.placeholder is not None:
                    _aboveplace = \
                        self.placeholder.above_placelines(
                            lines=lines
                        )
                else:
                    _aboveplace = lines
                total_line = 0
                for line in _scrlines:
                    print(line)
                    total_line += 1
                    if total_line == _aboveplace:
                        break
                if self.placeholder is not None and \
                    total_line == _aboveplace:
                    print(
                        self.placeholder.before_blank,
                        self.placeholder.placeholder,
                        self.placeholder.after_blank,
                    )

                if (len(_scrlines)-len(_scrlines[now_line+total_line:])) < _aboveplace:
                    return
                _input = sys.stdin.read(1)
                if ord(_input) == 0x71:
                    # quit
                    return
                elif ord(_input) == 0x20:
                    # space
                    now_line += total_line
                elif ord(_input) == 0x0a:
                    # enter
                    now_line += 1
                else:
                    continue
        finally:
            self._resetattr()

    # raw mode
    def _setrawmode(self):
        tty.setraw(sys.stdin.fileno())

    # cbreak mode
    def _setcbreak(self):
        tty.setcbreak(sys.stdin.fileno())

    def _resetattr(self):
        if not hasattr(self, "_oldattr"):
            raise MoreAttributeError(
                ""
            )
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._oldattr)
