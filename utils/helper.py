#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

CLR_GRN = "\033[92m"
CLR_YLW = "\033[93m"
CLR_RST = "\033[00m"


def lineBreak(someChar: str) -> None:
    print(f"\n{CLR_YLW}{someChar * 125}{CLR_RST}\n")


def printInfo(cat: str, text: str, removeNewLine: bool = True) -> None:
    if removeNewLine:
        text = str(text).strip().replace("\r\n", " ")
        text = text.strip().replace("\n\n", " ")  # zero-width non joiner -> \u200c
        text = re.sub(" +", " ", text)

    print(f"{CLR_GRN}{cat}:{CLR_RST} {text}")
