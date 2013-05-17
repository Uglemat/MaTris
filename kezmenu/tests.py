# -*- coding: utf-8 -*-

import doctest

doctest.testfile("docs/README.txt", optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)