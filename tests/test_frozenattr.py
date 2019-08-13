from typing import ClassVar

import pytest
import attr



class TestFrozenAttr:

    @attr.s
    class A:
        print("aaa")
        a: int = attr.ib(default=0)
        b: int = attr.ib(default=3, frozen=True)
        c: ClassVar = 10

    def test_is_frozen(self):
        print('azaza')
        conv = self.A(3)
        conv.a = 4
        assert conv.a == 3

