import math as m
import random as rand
import os as os


def main():
    points = get_points("points.txt")
    centroids = k_means(3, points)


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

    def eq(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y


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

    def eq(self, other: "Centroid") -> bool:
        if len(self.points) != len(other.points):
            return False
        if not self.center.eq(other.center):
            return False
        # assume all points are equal first
        pointseq = True
        for sp in self.points:
            pointeq = False
            for op in other.points:
                if op.eq(sp):
                    pointeq = True
            pointseq = pointseq and pointeq
        # return true if center and points are all equal
        return pointseq

    def __str__(self) -> str:
        sb = ""
        sb += str(self.center)
        sb += ", ["
        for index, p in enumerate(self.points):
            if index != len(self.points) - 1:
                sb += str(p) + ", "
            else:
                sb += str(p)
        sb += "]"
        return sb

    @staticmethod
    def equals(first: list["Centroid"], second: list["Centroid"]) -> bool:
        if len(first) != len(second):
            return False
        listeq = True
        for c1 in first:
            elemeq = False
            for c2 in second:
                if c1.eq(c2):
                    elemeq = True
            listeq = listeq and elemeq
        return listeq


def init_random_centroids(k: int, points: list[Point]) -> list[Centroid]:
    centroids = []
    rpoints = points.copy()
    for _ in range(k):
        ridx = rand.randint(0, len(rpoints) - 1)
        randp = rpoints.pop(ridx)
        # init with no points but randomly picked one
        centroid = Centroid([randp], randp)
        centroids.append(centroid)
    print_centroids(centroids)
    return centroids


def print_centroids(centroids: list[Centroid]):
    num = 0
    for c in centroids:
        print(f"{num} : {str(c)}")
        num += 1


def k_means(k: int, points: list[Point]) -> list[Centroid]:
    centroids = init_random_centroids(k, points)
    # create iterate loop where we assign clusers, then update cluster from assignment (mutual recursion step)
    converged = False
    iter = 1
    while converged == False:
        # first  assign new points
        new_centroids = update_centers(centroids)
        assign_points(new_centroids, points)
        if Centroid.equals(centroids, new_centroids):
            converged = True
        else:
            print(f"--ITERATION {iter}--")
            print("--CENTROIDS--")
            print_centroids(centroids)
            print("---NEW CENTROIDS--")
            print_centroids(new_centroids)
            iter += 1
            centroids = new_centroids
    return centroids


# expectation step
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


# maximization step
def update_centers(centroids: list[Centroid]) -> list[Centroid]:
    new_centroids = []
    for c in centroids:
        new_center = Point(0, 0)
        for p in c.points:
            new_center = Point.add(new_center, p)
        n = len(c.points)
        new_center.scale(1 / n)
        new_centroid = Centroid([], new_center)
        new_centroids.append(new_centroid)
    return new_centroids


if __name__ == "__main__":
    main()
