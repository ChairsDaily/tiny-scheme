#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest 
from tiny import core

class TestParser (unittest.TestCase):
    """
    Run simple tests for the tiny scheme parser
    """
    def test (self):
        self.code = """(begin (+ 1 ( * 1 (/ 10 2))))"""
        self.ast = core.parse(core.tokenize(
            self.code
        ))
        self.assertEqual(self.ast, 
            ['begin', ['+', 1, ['*', 1, ['/', 10, 2]]]])
        


