

class PlaceHolder:
    """

    ----------------
    . this is terminal screen.
    .
    .

                      <- before_blanks 
    Hello PlaceHolder <- placeholder
                      <- after_blanks
    ----------------

    """
    def __init__(
        self,
        placeholder=None,
        before_blanks=1,
        after_blanks=1,
    ):
        self.placeholder = placeholder
        self._placelines = len(
            self.placeholder.splitlines()
        )
        self.before_blanks = before_blanks
        self.after_blanks = after_blanks

    def above_placelines(self, lines):
        if not isinstance(lines, int):
            TypeError(
                "lines must be int type."
            )
        return lines - self._placelines - \
            self.before_blanks - self.after_blanks

    @property
    def placeholder(self):
        if self._placeholder is None:
            return ""
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        if value is not None and \
                not isinstance(value, str):
            raise TypeError(
                "placeholder must be str type."
            )
        self._placeholder = value

    @property
    def before_blanks(self):
        return self._before_blanks

    @before_blanks.setter
    def before_blanks(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "before_blanks must be int type."
            )
        self._before_blanks = value

    @property
    def before_blank(self):
        blank = str()
        for _ in range(self.before_blanks):
            blank += "\n"
        return blank

    @property
    def after_blanks(self):
        return self._after_blanks

    @after_blanks.setter
    def after_blanks(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "after_blanks must be int type."
            )
        self._after_blanks = value

    @property
    def after_blank(self):
        blank = str()
        for _ in range(self.before_blanks):
            blank += "\n"
        return blank
