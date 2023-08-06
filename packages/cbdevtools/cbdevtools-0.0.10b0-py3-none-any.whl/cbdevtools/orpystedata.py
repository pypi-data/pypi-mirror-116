#!/usr/bin/env python3

###
# This module simplifies the use of path::``PEUF`` files for datas used
# to achieve unit tests.
###


from typing import *

from pathlib import Path
from pytest import fixture

from orpyste.data import ReadBlock


###
# prototype::
#     file = ; // See Python typing...
#            just use the magic constant ``__file__`` when calling
#            this function from a testing file.
#
#     :return: = ; // See Python typing...
#                an object containing the datas defined in a 
#                path::``PEUF`` file (see the ¨info below).
#
# This function returns an instance of ``ReadBlock`` obtained after 
# analyzing a path::``peuf`` file automatically named. 
# 
# info::
#     The name of the path::``peuf`` file is obtained by removing the prefix
#     path::``test_`` of the name of the testing file (see ``file``).
###

def build_datas_block(
    file: str,
) -> ReadBlock:
    file    = Path(file)
    thisdir = file.parent

    whatistested = file.stem
    whatistested = whatistested.replace('test_', '')

    return ReadBlock(
        content = thisdir / f'{whatistested}.peuf',
        mode    = {"keyval:: =": ":default:"}
    )


###
# prototype::
#     :see: = build_datas_block
#
# This fixture yields a ready-to-use data dictionary used to acheive the tests.
# It also finalizes the cleaning of ¨orpyste extra files in case of problem. 
#
# info::
#     The "intuitive" dictionary is build via ``mydict("std nosep nonb")``.
#     See ¨orpyste.
# 
# 
# Here is a real example of use.
#
# python::
#     from cbdevtools import *
#
#     addsrc(
#         file    = __file__,
#         project = 'TeXitEasy',
#     )
#
#     from src.escape import fstringit
#
#     def test_latex_use_fstringit(peuf_fixture):
#         tests = peuf_fixture(__file__)
#
#         for infos in tests.values():
#             found  = fstringit(infos['source'])
#             wanted = infos['fstring']
#
#             assert wanted == found
###

# Refs
#    * https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
#    * https://docs.pytest.org/en/6.2.x/fixture.html#factories-as-fixtures

@fixture(scope = "session")
def peuf_fixture():
    datas_build = []

###
# prototype::
#     file = ; // See Python typing...
#            just use the magic constant ``__file__`` when calling
#            this function from a testing file.
###
    def _make_peuf_datas(file):
        datas_build.append(datas := build_datas_block(file))
        
        datas.build()

        return datas.mydict("std nosep nonb")

    yield _make_peuf_datas

    for datas in datas_build:
        datas.remove_extras()
