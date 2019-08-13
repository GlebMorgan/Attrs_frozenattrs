
import pytest
import attr



class TestFrozenAttr:

    @attr.s
    class ConvFrozenattr:
        print("aaa")

        a: int = attr.ib(default=0, frozen=True)

    def test_is_frozen(self):
        print('azaza')
        conv = self.ConvFrozenattr(3)
        conv.a = 4
        assert conv.a == 3


# TODO: make fork again and manually edit last version of attrs to add frozenattrs based on 3 Tinche's commits