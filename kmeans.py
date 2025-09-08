import math as m
import random as rand
import os as os


def main():
    points = get_points("points.txt")
    for p in points:
        print(p)
    print("--SCALE--")
    for p in points:
        p.scale(2)
        print(p)


# centroids
class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def distance(final: "Point", initial: "Point") -> float:
        # NOTE: you can define different distances for k-means, but most common is euclidean or L2
        return m.sqrt((final.x - initial.x) ** 2 + (final.y - initial.y) ** 2)

    @staticmethod
    def add(lhs: "Point", rhs: "Point") -> "Point":
        return Point(lhs.x + rhs.x, lhs.y + rhs.y)

    def scale(self, scalar: float):
        self.x *= scalar
        self.y *= scalar

    def display(self):
        print(f"({self.x}, {self.y})")

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


def get_points(file_path: str) -> list[Point]:
    points = []
    with open(file_path, "r") as file:
        for line in file:
            coords = line.split(",")
            x = int(coords[0])
            y = int(coords[1])
            point = Point(x, y)
            points.append(point)
    return points


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

    def variance(self) -> float:
        # compute the variance / intra cluster distance
        return 0.0


def init_random_centroids(k: int, points: list[Point]) -> list[Centroid]:
    centroids = []
    for _ in range(k):
        ridx = rand.randint(0, len(points) - 1)
        # init with no points but randomly picked one
        centroid = Centroid([], points[ridx])
        centroids.append(centroid)
    return centroids


def k_means(k: int, points: list[Point]) -> list[Centroid]:
    centroids = init_random_centroids(k, points)
    # create iterate loop where we assign clusers, then update cluster from assignment (mutual recursion step)
    converged = False
    while converged == False:
        # first  assign new points
        assign_points(centroids, points)
        # recalc the center of each centroid
        new_centroids = update_centers(centroids)
        if new_centroids == centroids:
            converged = True
        else:
            centroids = new_centroids
    return centroids


def assign_points(centroids: list[Centroid], points: list[Point]):
    for p in points:
        min_distance = 1 << 32
        min_index = -1
        # for each centroid, find one with min distance to point and assign it
        for index, c in enumerate(centroids):
            distance = Point.distance(p, c.center)
            if distance < min_distance:
                # update min distance and candidate centroid
                min_index = index
                min_distance = distance
        # once we find centroid w/ min dist to point, assign point to it
        centroids[min_index].points.append(p)


def update_centers(centroids: list[Centroid]) -> list[Centroid]:
    new_centroids = []
    for c in centroids:
        new_center = Point(0, 0)
        n = len(c.points)
        for p in c.points:
            new_center = Point.add(new_center, p)
        new_center.scale(1 / n)
        new_centroid = Centroid([], new_center)
        new_centroids.append(new_centroid)
    return new_centroids


if __name__ == "__main__":
    main()
