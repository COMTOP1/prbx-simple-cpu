class Flags:
    __negative: bool = False
    __positive: bool = False
    __overflow: bool = False
    __carry: bool = False
    __zero: bool = False

    def get1a(self):
        return self.__zero

    def get1d(self):
        return int(f'{self.__negative}{self.__positive}{self.__overflow}{self.__carry}{self.__zero}', 2)

    def set1a(self, zero: bool):
        self.__zero = zero

    def set_negative(self, negative: bool):
        self.__negative = negative

    def set_positive(self, positive: bool):
        self.__positive = positive

    def set_overflow(self, overflow: bool):
        self.__overflow = overflow

    def set_carry(self, carry: bool):
        self.__carry = carry

    def set_zero(self, zero: bool):
        self.__zero = zero