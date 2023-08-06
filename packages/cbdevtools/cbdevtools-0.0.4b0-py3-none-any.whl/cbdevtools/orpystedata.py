#!/usr/bin/env python3

from pathlib import Path
from pytest  import fixture

from orpyste.data import ReadBlock


THE_DATAS_FOR_TESTING = None

def build_datas_block(
    file: str,
) -> None:
    global THE_DATAS_FOR_TESTING

    thisdir = Path(__file__).parent

    whatistested = Path(__file__).stem
    whatistested = whatistested.replace('test_', '')

    THE_DATAS_FOR_TESTING = ReadBlock(
        content = thisdir / f'{whatistested}.peuf',
        mode    = {"keyval:: =": ":default:"}
    )

@fixture(scope = "module")
def orpyste_fix_block(request):
    global THE_DATAS_FOR_TESTING

    THE_DATAS_FOR_TESTING.build()

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)