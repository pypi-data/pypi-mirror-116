#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the garoupa project.
#  Please respect the license - more about this in the section (*) below.
#
#  garoupa is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  garoupa is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with garoupa.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.

from garoupa.colors import colorize128bit
from garoupa.core import cells_id_fromblob, id_fromcells, cells_fromid
from garoupa.math import int2m4, m42int, m4m, m4inv


class Hash:
    """
    etype = ordered, hybrid, unordered
    According to subgroup: Z, H\Z or G\H

    Usage:
    >>> a = Hash(b"lots of data")
    >>> b = Hash(b"lots of data 2")
    >>> a.id
    'fw-IowLZVKdeXCNkqsTHFiIe06Pv0.oaAXY.fN6xJ2E7.fe36iBXxOYpmm83Q7ZL'
    >>> b.id
    'ttXOjA4WLwyrOF6tk2YJeYHhrydN6hrm315uFyZRa9Z0OBPm2NWRkoOYtNHYGlwv'
    >>> (a * b).id
    'I-WuI4QUFeHGKfTNKvQq1X5jqz-rfMJC19-pIAVniOF3ScY-1ac3fMqhAElcjexK'
    >>> (b * a).id
    'I-WuI4QUFeHGKfTNKvQq1-T.MqLLanrR4nsDP4B2SuNUeN7xgiWFtVokR7Qcb05-'
    >>> a * b * ~b == a
    True
    >>> c = Hash(b"lots of data 3")
    >>> (a * b) * c == a * (b * c)
    True
    >>> e = Hash(b"lots of data 4")
    >>> f = Hash(b"lots of data 5")
    >>> e * f != f * e
    True
    >>> a * b != b * a
    True
    >>> x = Hash(b"lots of data 6", "hybrid")
    >>> y = Hash(b"lots of data 7", "hybrid")
    >>> z = Hash(b"lots of data 8", "unordered")
    >>> x * y == y * x
    True
    >>> x * a != a * x
    True
    >>> x * z == z * x
    True
    >>> a * z == z * a
    True
    """
    _repr = None
    _n, _id, _cells = None, None, None
    _bits = None

    def __init__(self, blob, etype="ordered", version="UT64.4"):
        self.etype = etype
        if version == "UT32.4":
            self.p = 4294967291
            self.bytes = 24
            self.digits = 32
            self.order = 6277101691541631771514589274378639120656724268335671295241
        elif version == "UT64.4":
            self.p = 18446744073709551557
            self.bytes = 48
            self.digits = 64
            self.order = 39402006196394478456139629384141450683325994812909116356652328479007639701989040511471346632255226219324457074810249
        else:
            raise Exception("Unknown version:", version)
        if blob is not None:  # None is for internal use only.
            self._cells, self._id = cells_id_fromblob(blob, etype, self.bytes, self.p)

    @classmethod
    def fromcells(cls, cells, p=18446744073709551557,
                  order=39402006196394478456139629384141450683325994812909116356652328479007639701989040511471346632255226219324457074810249):
        hash = Hash(None, "H")
        hash._cells = cells
        hash.p = p
        hash.order = order
        return hash

    @classmethod
    def fromid(cls, id, p=18446744073709551557,
               order=39402006196394478456139629384141450683325994812909116356652328479007639701989040511471346632255226219324457074810249):
        """
        Usage:
        >>> Hash.fromid("I-WuI4QUFeHGKfTNKvQq1.nvrF1g78jBUgN73RMYyoXehzfULkYQHPYdppZW5ar2").n
        27694086209736845103299750681684630473246580734449841275786785442935721031358612476242143296609286791135053038790338

        :param id:
        :return:
        """
        hash = Hash(None, "H")
        hash._id = id
        hash.p = p
        hash.order = order
        return hash

    @classmethod
    def fromn(cls, n: int, p=18446744073709551557,
              order=39402006196394478456139629384141450683325994812909116356652328479007639701989040511471346632255226219324457074810249):
        """Hash representing the given int.

        Default 'p' is according to version UT64.4.

        Usage:
        >>> h = Hash.fromn(7647544756746324134134)
        >>> h.id
        '0000000000000000000000000000000000000000000000000001DFc0Ttk5MszS'
        """
        if n > order:
            raise Exception(f"Element outside allowed range: {n} >= {order}")
        return Hash.fromcells(int2m4(n, p), p, order)

    def calculate(self):
        if self._cells is not None:
            self._id = id_fromcells(self._cells, self.digits, self.p)
        elif self._id:
            self._cells = cells_fromid(self._id, self.p)
        else:
            raise Exception("Missing argument.")
        if self.n >= self.order:
            raise Exception(f"Element outside allowed range: {self.n} >= {self.order}")

    @property
    def cells(self):
        if self._cells is None:
            self.calculate()
        return self._cells

    @property
    def n(self):
        if self._n is None:
            self._n = m42int(self.cells, self.p)
        return self._n

    @property
    def id(self):
        if self._id is None:
            self.calculate()
        return self._id

    # @property
    # def bits(self):
    #     if self._bits is None:
    #         self._bits = bin(self.n)[2:].rjust(256, "0")
    #     return self._bits

    def __mul__(self, other):
        return Hash.fromcells(m4m(self.cells, other.cells, self.p), self.p, self.order)

    def __invert__(self):
        return Hash.fromcells(m4inv(self.cells, self.p), self.p, self.order)

    def __truediv__(self, other):
        return Hash.fromcells(m4m(self.cells, m4inv(other.cells, self.p), self.p), self.p, self.order)

    def __add__(self, other):
        return Hash.fromn((self.n + other.n) % self.order, self.p, self.order)

    def __sub__(self, other):
        return Hash.fromn((self.n - other.n) % self.order, self.p, self.order)

    def __repr__(self):
        if self._repr is None:
            self._repr = colorize128bit(self.id, self.digits)
        return self._repr

    @property
    def idc(self):
        return repr(self)

    def __str__(self):
        return self.id

    def __eq__(self, other):
        return self.n == other.n


identity = Hash.fromn(0)
