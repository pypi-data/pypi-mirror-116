from .placeholder import PlaceHolder
from .more import More

def printm(
    output,
    placeholder=None,
    before_blanks=1,
    after_blanks=0,
    no_placeholder=False,
):
    """
    -> this is terminal screen.
    ------------------------------
    output
    .
    .
    .


    ------------------------------
                        <- before_blanks
    placeholder
                        <- after_blanks
    ------------------------------

params:

@output         (required): string you want to output. must be string type.
@placeholder      (option): placeholder string.
@before_blanks        (=1): number of lines inserted before placeholder string.
@after_blanks         (=0): number of lines inserted after placeholder string.
@no_placeholder   (=False): if true, delete placeholder field.

return:
    no return value.
    
    """
    if not no_placeholder:
        _placeholder = PlaceHolder(
            placeholder=placeholder,
            before_blanks=before_blanks,
            after_blanks=after_blanks,
        )
    else:
        _placeholder = None

    _more = More(
        output=output,
        placeholder=_placeholder
    )
    _more.print()
