from tkinter import *
import math

def roundPolygon(x, y, sharpness, canvas, **kwargs):

    # The sharpness here is just how close the sub-points
    # are going to be to the vertex. The more the sharpness,
    # the more the sub-points will be closer to the vertex.
    # (This is not normalized)
    if sharpness < 2:
        sharpness = 2

    ratioMultiplier = sharpness - 1
    ratioDividend = sharpness

    # Array to store the points
    points = []

    # Iterate over the x points
    for i in range(len(x)):
        # Set vertex
        points.append(x[i])
        points.append(y[i])

        # If it's not the last point
        if i != (len(x) - 1):
            # Insert submultiples points. The more the sharpness, the more these points will be
            # closer to the vertex. 
            points.append((ratioMultiplier*x[i] + x[i + 1])/ratioDividend)
            points.append((ratioMultiplier*y[i] + y[i + 1])/ratioDividend)
            points.append((ratioMultiplier*x[i + 1] + x[i])/ratioDividend)
            points.append((ratioMultiplier*y[i + 1] + y[i])/ratioDividend)
        else:
            # Insert submultiples points.
            points.append((ratioMultiplier*x[i] + x[0])/ratioDividend)
            points.append((ratioMultiplier*y[i] + y[0])/ratioDividend)
            points.append((ratioMultiplier*x[0] + x[i])/ratioDividend)
            points.append((ratioMultiplier*y[0] + y[i])/ratioDividend)
            # Close the polygon
            points.append(x[0])
            points.append(y[0])
    print (points)
    print (len(points))
    return canvas.create_polygon(points, **kwargs, smooth=TRUE)


def create_good_rectangle(canvas, x1, y1, x2, y2, feather, res=5, **kwargs):
    points = []
    # top side
    points += [x1 + feather, y1,
               x2 - feather, y1]
    # top right corner
    for i in range(res):
        points += [x2 - feather + math.sin(i/res*2) * feather,
                   y1 + feather - math.cos(i/res*2) * feather]
    # right side
    points += [x2, y1 + feather,
               x2, y2 - feather]
    # bottom right corner
    for i in range(res):
        points += [x2 - feather + math.cos(i/res*2) * feather,
                   y2 - feather + math.sin(i/res*2) * feather]
    # bottom side
    points += [x2 - feather, y2,
               x1 + feather, y2]
    # bottom left corner
    for i in range(res):
        points += [x1 + feather - math.sin(i/res*2) * feather,
                   y2 - feather + math.cos(i/res*2) * feather]
    # left side
    points += [x1, y2 - feather,
               x1, y1 + feather]
    # top left corner
    for i in range(res):
        points += [x1 + feather - math.cos(i/res*2) * feather,
                   y1 + feather - math.sin(i/res*2) * feather]
        
    return canvas.create_polygon(points, **kwargs, smooth=TRUE)
    # return canvas.create_polygon(points, fill=color) #?


if __name__ == "__main__":
    print("""
    =======================================================
        test round rectangles
    =======================================================
    """)

    root = Tk()
    canvas = Canvas(root, width = 1000, height = 1000)
    canvas.pack()

    # my_rectangle = roundPolygon([50, 550, 550, 50], [50, 50, 550, 550], 0, canvas, width=5, outline="#82B366", fill="#D5E8D4")
    # my_triangle = roundPolygon([50, 650, 50], [400, 700, 1000], 8, canvas, width=5, outline="#82B366", fill="#D5E8D4")

    second_rect = create_good_rectangle(canvas, 10, 10, 500, 500, 20, width = 50, outline = "#FF0000", fill = "#00FF00")

    root.mainloop()


