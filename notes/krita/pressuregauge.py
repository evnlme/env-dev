from typing import List

import krita as K

class Histogram(K.QWidget):
    def __init__(self, data: List[int], labels: List[str]) -> None:
        super().__init__()
        self._data = data
        self._labels = labels
        self._bars = []
        self._maxIndex = None
        self._maxCount = 1
        self.hConfigure()

    def hConfigure(self) -> None:
        layout = K.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(K.Qt.AlignBottom)
        self.setLayout(layout)
        for _ in range(len(self._data)):
            widget = K.QWidget()
            widget.setFixedHeight(0)
            widget.setStyleSheet(
                'background-color: lightblue;' +
                'border: 1px solid black')
            self._bars.append(widget)
            layout.addWidget(widget)

    def hIncrement(self, index: int) -> None:
        count = self._data[index] + 1
        self._data[index] = count
        if count > self._maxCount:
            self._maxCount = count
            self._maxIndex = index
        if index != self._maxIndex:
            self.hUpdateBar(index)
            return
        for i in range(len(self._data)):
            self.hUpdateBar(i)

    def hReset(self) -> None:
        n = len(self._data)
        for i in range(n):
            self._data[i] = 0
        self._maxIndex = None
        self._maxCount = 1

    def hUpdateBar(self, index: int) -> None:
        h = self.height() * self._data[index] / self._maxCount
        self._bars[index].setFixedHeight(int(h))

class PressureGauge(K.QWidget):
    # 0 to 100 inclusive.
    BIN_COUNT = 101

    def __init__(self) -> None:
        super().__init__()
        self._histogram = Histogram(
            data=[0] * PressureGauge.BIN_COUNT,
            labels=[str(i) for i in range(PressureGauge.BIN_COUNT)])
        self.pgConfigure()

    def pgConfigure(self) -> None:
        layout = K.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self._histogram)

    def tabletEvent(self, event: K.QTabletEvent) -> None:
        event.ignore()
        pressure = event.pressure()
        index = round(pressure * (PressureGauge.BIN_COUNT - 1))
        self._histogram.hIncrement(index)

    def pgReset(self) -> None:
        self._histogram.hReset()

pg = PressureGauge()
pg.show()
inst = K.Krita.instance()
inst._pg = pg
