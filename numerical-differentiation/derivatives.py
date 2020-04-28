from abc import ABC


class Derivative(ABC):
    def __init__(self, values, h):
        self._values = values
        self._count = len(values)
        self._h = h

        self._derivatives = []

        self._calculate_derivatives()

    def _calculate_derivatives(self):
        self._derivatives.append(self.forward(0))

        for i in range(1, self._count - 1):
            self._derivatives.append(self.central(i))

        self._derivatives.append(self.backward(self._count - 1))

    def forward(self, i):
        raise NotImplementedError

    def backward(self, i):
        raise NotImplementedError

    def central(self, i):
        raise NotImplementedError

    def __call__(self, i):
        return self._derivatives[i]


class FirstDerivative(Derivative):
    def __init__(self, values, h):
        assert len(values) >= 2
        super().__init__(values, h)

    def _calculate_derivatives(self):
        super()._calculate_derivatives()

    def forward(self, i):
        return (self._values[i + 1] - self._values[i]) / self._h

    def backward(self, i):
        return (self._values[i] - self._values[i - 1]) / self._h

    def central(self, i):
        return (self._values[i + 1] - self._values[i - 1]) / (2 * self._h)


class SecondDerivative(Derivative):
    def __init__(self, values, h):
        assert len(values) >= 4
        super().__init__(values, h)

    def _calculate_derivatives(self):
        super()._calculate_derivatives()

    def forward(self, i):
        return (self._values[i + 2] - 2 * self._values[i + 1] + self._values[i]) / (self._h ** 2)

    def backward(self, i):
        return (self._values[i] - 2 * self._values[i - 1] + self._values[i - 2]) / (self._h ** 2)

    def central(self, i):
        return (self._values[i + 1] - 2 * self._values[i] + self._values[i - 1]) / (self._h ** 2)


class ThirdDerivative(Derivative):
    def __init__(self, values, h):
        assert len(values) >= 5
        super().__init__(values, h)

    def _calculate_derivatives(self):
        self._derivatives.append(self.forward(0))
        self._derivatives.append(self.forward(1))

        for i in range(2, self._count - 2):
            self._derivatives.append(self.central(i))

        self._derivatives.append(self.backward(self._count - 2))
        self._derivatives.append(self.backward(self._count - 1))

    def forward(self, i):
        return (self._values[i + 3] - 3 * self._values[i + 2] + 3 * self._values[i + 1] - self._values[i]) / (
                self._h ** 3)

    def backward(self, i):
        return (self._values[i] - 3 * self._values[i - 1] + 3 * self._values[i - 2] - self._values[i - 3]) / (
                self._h ** 3)

    def central(self, i):
        return (self._values[i + 2] - 2 * self._values[i + 1] + 2 * self._values[i - 1] - self._values[i - 2]) / (
                2 * (self._h ** 3))
