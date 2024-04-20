"""
This type stub file was generated by pyright.
"""

import os

"""
Paging capabilities for IPython.core

Notes
-----

For now this uses IPython hooks, so it can't be in IPython.utils.  If we can get
rid of that dependency, we could move it there.
-----
"""
def display_page(strng, start=..., screen_lines=...): # -> None:
    """Just display, no paging. screen_lines is ignored."""
    ...

def as_hook(page_func): # -> (self: Unknown, *args: Unknown, **kwargs: Unknown) -> Unknown:
    """Wrap a pager func to strip the `self` arg

    so it can be called as a hook.
    """
    ...

esc_re = ...
def page_dumb(strng, start=..., screen_lines=...): # -> None:
    """Very dumb 'pager' in Python, for when nothing else works.

    Only moves forward, same interface as page(), except for pager_cmd and
    mode.
    """
    ...

def pager_page(strng, start=..., screen_lines=..., pager_cmd=...): # -> None:
    """Display a string, piping through a pager after a certain length.

    strng can be a mime-bundle dict, supplying multiple representations,
    keyed by mime-type.

    The screen_lines parameter specifies the number of *usable* lines of your
    terminal screen (total lines minus lines you need to reserve to show other
    information).

    If you set screen_lines to a number <=0, page() will try to auto-determine
    your screen size and will only use up to (screen_size+screen_lines) for
    printing, paging after that. That is, if you want auto-detection but need
    to reserve the bottom 3 lines of the screen, use screen_lines = -3, and for
    auto-detection without any lines reserved simply use screen_lines = 0.

    If a string won't fit in the allowed lines, it is sent through the
    specified pager command. If none given, look for PAGER in the environment,
    and ultimately default to less.

    If no system pager works, the string is sent through a 'dumb pager'
    written in python, very simplistic.
    """
    ...

def page(data, start=..., screen_lines=..., pager_cmd=...): # -> None:
    """Display content in a pager, piping through a pager after a certain length.

    data can be a mime-bundle dict, supplying multiple representations,
    keyed by mime-type, or text.

    Pager is dispatched via the `show_in_pager` IPython hook.
    If no hook is registered, `pager_page` will be used.
    """
    ...

def page_file(fname, start=..., pager_cmd=...): # -> None:
    """Page a file, using an optional pager command and starting line.
    """
    ...

def get_pager_cmd(pager_cmd=...):
    """Return a pager command.

    Makes some attempts at finding an OS-correct one.
    """
    ...

def get_pager_start(pager, start):
    """Return the string for paging files with an offset.

    This is the '+N' argument which less and more (under Unix) accept.
    """
    ...

if os.name == 'nt' and os.environ.get('TERM', 'dumb') != 'emacs':
    def page_more():
        """ Smart pausing between pages

        @return:    True if need print more lines, False if quit
        """
        ...
    
else:
    def page_more():
        ...
    