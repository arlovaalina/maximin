def initialize_points():
    points = [{
        'x': random.randint(0, FIELD_WIDTH),
        'y': random.randint(0, FIELD_HEIGHT),
        'class': 0,
    } for point in range(points_count)]
    return points

def main():
    initialize_points()

if __name__ == "__main__":
    main()
