#!/usr/bin/env python3

from pathlib import Path

from orpyste.data import ReadBlock


def build_datas_block(
    file: str,
) -> ReadBlock:
    thisdir = Path(file).parent

    whatistested = Path(file).stem
    whatistested = whatistested.replace('test_', '')

    return ReadBlock(
        content = thisdir / f'{whatistested}.peuf',
        mode    = {"keyval:: =": ":default:"}
    )
