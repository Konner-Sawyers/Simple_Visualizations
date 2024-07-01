class Vec2:
    def __init__(self, a: float = 0, b: float = 0) -> None:
        self.a = a
        self.b = b

    def add(self, A: any) -> any:
        return (Vec2(round(self.a + A.a, 4), round(self.b + A.b, 4)))

    def sub(self, A: any) -> any:
        return (Vec2(round(self.a - A.a, 4), round(self.b - A.b, 4)))