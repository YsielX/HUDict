from dataclasses import dataclass


@dataclass(frozen=True)
class Box:
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def center_x(self):
        return self.left + self.width / 2

    @property
    def center_y(self):
        return self.top + self.height / 2

    def distance_sq_to(self, x, y):
        dx = max(self.left - x, 0, x - self.right)
        dy = max(self.top - y, 0, y - self.bottom)
        return dx * dx + dy * dy

    def to_dict(self):
        return {
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
            "right": self.right,
            "bottom": self.bottom,
            "center_x": self.center_x,
            "center_y": self.center_y,
        }


@dataclass(frozen=True)
class Word:
    text: str
    box: Box

    def to_dict(self):
        return {"text": self.text, "box": self.box.to_dict()}


@dataclass(frozen=True)
class Line:
    text: str
    words: list[Word]
    box: Box

    def to_dict(self):
        return {
            "text": self.text,
            "box": self.box.to_dict(),
            "words": [word.to_dict() for word in self.words],
        }
