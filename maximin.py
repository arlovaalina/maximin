from variables import *
from functools import reduce
from tkinter import *
import random
import math

def paint_points(points, centroids):
    canvas.delete("all")
    for i in range(0, points_count):
        canvas.create_oval(points[i]["x"], points[i]["y"], points[i]["x"] + 1, points[i]["y"] + 1,
            fill=COLORS[points[i]["class"]], outline=COLORS[points[i]["class"]])
    for j in range(0, len(centroids)):
        canvas.create_oval(centroids[j]["x"], centroids[j]["y"], centroids[j]["x"] + 10, centroids[j]["y"] + 10,
            fill=COLORS[centroids[j]["class"]], outline=COLORS[centroids[j]["class"]])

def euclid_distance(a, b):
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2)

def initialize_points():
    points = [{
        'x': random.randint(0, FIELD_WIDTH),
        'y': random.randint(0, FIELD_HEIGHT),
        'class': 0,
    } for point in range(points_count)]
    return points

def initialize_first_centroid(points):
    centroid = points[random.randint(0, points_count)]
    return centroid

def find_second_centroid(points, first_centroid):
    centroid = max(points, key=lambda x: euclid_distance(first_centroid, x))
    centroid.update({"class": 1})
    return centroid

def allocate_classes(points, centroids):
    for i in range(points_count):
        centroid = min(centroids, key=lambda x: euclid_distance(points[i], x))
        points[i].update({"class": centroid["class"]})

def find_new_centroid(points, centroids):
    distances = []
    for i in range(len(centroids)):
        class_points = list(filter(lambda x: x["class"] == i, points))
        max_distance_point = max(points, key=lambda x: euclid_distance(centroids[i], x))
        max_distance = euclid_distance(centroids[i], max_distance_point)
        max_distance_point.update({ "distance": max_distance})
        distances.append(max_distance_point)
    new_centroid = max(distances, key=lambda x: x["distance"])
    return new_centroid

def check_new_centroid(centroid, centroids):
    distance = 0
    for i in range(len(centroids)):
        for j in range(len(centroids)):
            distance = distance + euclid_distance(centroids[i], centroids[j])
    distance = distance / 2
    mean_distance = distance / len(centroids)
    if (centroid["distance"] < mean_distance / 2):
        return False
    return True

def start_algorithm(event):
    print('start')
    points = initialize_points()
    first_centroid = initialize_first_centroid(points)
    second_centroid = find_second_centroid(points, first_centroid)
    centroids = [first_centroid, second_centroid]
    continue_clasterization = True
    while (continue_clasterization):
        paint_points(points, centroids)
        root.update()
        allocate_classes(points, centroids)
        new_centroid = find_new_centroid(points, centroids)
        centroid_checked = check_new_centroid(new_centroid, centroids)
        if (centroid_checked):
            new_centroid.update({"class": len(centroids)})
            centroids.append(new_centroid)
        else:
            continue_clasterization = False
    print('finish')

root = Tk()
root.geometry("{0}x{1}".format(WINDOW_WIDTH, WINDOW_HEIGHT))
canvas = Canvas(root, width = FIELD_WIDTH, height = FIELD_HEIGHT, borderwidth = 1, background='white')
canvas.place(x = 200, y = 10)
start_button = Button(root, text = "Start algorithm", width = 10)
start_button.place(x = 20, y = 10)
start_button.bind("<Button-1>", start_algorithm)

root.mainloop()
