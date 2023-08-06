#!/usr/bin/env python3
# coding:utf-8
from .error import ParsecError
from . import Parsec
from io import StringIO


def string(s, case_sensitive=True):
    @Parsec
    def call(st):
        buffer = StringIO()
        segment = s if case_sensitive else s.lower()
        for chr in segment:
            c = st.next()
            if (chr != c and case_sensitive) or (not case_sensitive and chr != c.lower()):
                raise ParsecError(st, "Expect '{0}' but got {1}".format(s, c))
            else:
                buffer.write(c)
        else:
            return buffer.getvalue()

    return call


@Parsec
def space(state):
    c = state.next()
    if c.isspace():
        return c
    raise ParsecError(state, "Expect a space but got {0}".format(c))


@Parsec
def digit(state):
    c = state.next()
    if c.isdigit():
        return c
    else:
        raise ParsecError(state, "Expect a space but got {0}".format(c))

