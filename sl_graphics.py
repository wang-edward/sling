from tkinter import *


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


if __name__ == "__main__":
    print("""
    =======================================================
        test round rectangles
    =======================================================
    """)

    root = Tk()
    canvas = Canvas(root, width = 1000, height = 1000)
    canvas.pack()

    my_rectangle = roundPolygon([50, 550, 550, 50], [50, 50, 550, 550], 0, canvas, width=5, outline="#82B366", fill="#D5E8D4")
    # my_triangle = roundPolygon([50, 650, 50], [400, 700, 1000], 8, canvas, width=5, outline="#82B366", fill="#D5E8D4")

    root.mainloop()


