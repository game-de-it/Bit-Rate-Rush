class SpatialHash:
    """固定セルサイズの空間ハッシュ。毎フレーム rebuild して近傍探索に使う。"""

    def __init__(self, cell=32):
        self.cell = cell
        self.cells = {}

    def rebuild(self, items):
        cells = self.cells
        cells.clear()
        c = self.cell
        for it in items:
            k = (int(it.x // c), int(it.y // c))
            lst = cells.get(k)
            if lst is None:
                cells[k] = [it]
            else:
                lst.append(it)

    def nearby(self, x, y, r):
        """(x, y) を中心とした半径 r の正方形に重なるセルの中身をまとめて返す。"""
        c = self.cell
        x0 = int((x - r) // c)
        x1 = int((x + r) // c)
        y0 = int((y - r) // c)
        y1 = int((y + r) // c)
        get = self.cells.get
        out = []
        for cx in range(x0, x1 + 1):
            for cy in range(y0, y1 + 1):
                lst = get((cx, cy))
                if lst:
                    out.extend(lst)
        return out
