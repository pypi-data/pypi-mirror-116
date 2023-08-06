#!/usr/bin/env python3

###
# This module simplifies the use of path::``PEUF`` files for datas used
# to achieve unit tests.
###


from typing import *

from pathlib import Path

from orpyste.data import Read, ReadBlock


###
# prototype::
#     file = ; // See Python typing...
#            just use the magic constant ``__file__`` when calling
#            this function from a testing file.
#
#     :return: = ; // See Python typing...
#                an instance of ``ReadBlock`` obtained by analyzing
#                a path::``PEUF`` file.
#
#     :see: = _build_datas
###

def build_datas_block(
    file: str,
) -> ReadBlock:
    return _build_datas(
        file = file,
        clss = ReadBlock
    )


###
# prototype::
#     file = ; // See Python typing...
#            just use the magic constant ``__file__`` when calling
#            this function from a testing file.
#
#     :return: = ; // See Python typing...
#                an instance of ``Read`` obtained by analyzing
#                a path::``PEUF`` file.
#
#     :see: = _build_datas
###

def build_datas(
    file: str,
) -> Read:
    return _build_datas(
        file = file,
        clss = Read
    )


###
# prototype::
#     file = ; // See Python typing...
#            just use the magic constant ``__file__`` when calling
#            this function from a testing file.
#     clss = _ in [Read, ReadBlock] ; // See Python typing...
#            the class to use to analyze the path::``PEUF`` file.
#
#     :return: = ; // See Python typing...
#                an instance obtained by analyzing a path::``PEUF`` file.
#
# This function returns an instance of either ``Read``, or ``ReadBlock`` 
# obtained after analyzing a path::``peuf`` file. 
# 
# info::
#     The name of the path::``peuf`` file must be obtained by removing
#     path::``test_`` at the beginning of the name of the testing file.
###

def _build_datas(
    file: str,
    clss: Union[Read, ReadBlock],
) -> Union[Read, ReadBlock]:
    file    = Path(file)
    thisdir = file.parent

    whatistested = file.stem
    whatistested = whatistested.replace('test_', '')

    return clss(
        content = thisdir / f'{whatistested}.peuf',
        mode    = {"keyval:: =": ":default:"}
    )
