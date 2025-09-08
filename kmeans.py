import math as m
import numpy as np
import random as rand


def main():
    print("Hello, World")


# centroids
class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def distance(final: "Point", initial: "Point") -> float:
        return m.sqrt((final.x - initial.x) ** 2 + (final.y - initial.y) ** 2)

    def display(self):
        print(f"({self.x}, {self.y})")

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"


class Centroid:
    points: list[Point]
    center: Point

    def __init__(self, points: list[Point], center: Point) -> None:
        self.points = points
        self.center = center

    def display(self):
        print("Center:", str(self.center))
        print("Points =>")
        for p in self.points:
            print(str(p))

    @staticmethod
    def random_centroids(k: int, points: list[Point]) -> list["Centroid"]:
        centroids = []
        for _ in range(k):
            ridx = rand.randint(0, len(points) - 1)
            centroid = Centroid([], points[ridx])
            centroids.append(centroid)
        return centroids


if __name__ == "__main__":
    main()
