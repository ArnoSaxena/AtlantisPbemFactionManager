from math import cos, sin, radians


class ProvinceHexagon:
    def __init__(self, parent_canvas, top_left_x, top_left_y, hex_side_size, fill_colour, tags):
        self.parent_canvas = parent_canvas
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.hex_side_size = hex_side_size
        self.fill_colour = fill_colour
        self.tags = tags

        self.draw()

    def draw(self):
        start_x = self.top_left_x
        start_y = self.top_left_y
        angle = 60
        coords = []
        for i in range(6):
            end_x = start_x + self.hex_side_size * cos(radians(angle * i))
            end_y = start_y + self.hex_side_size * sin(radians(angle * i))
            coords.append([start_x, start_y])
            start_x = end_x
            start_y = end_y
        self.parent_canvas.create_polygon(coords[0][0],
                                          coords[0][1],
                                          coords[1][0],
                                          coords[1][1],
                                          coords[2][0],
                                          coords[2][1],
                                          coords[3][0],
                                          coords[3][1],
                                          coords[4][0],
                                          coords[4][1],
                                          coords[5][0],
                                          coords[5][1],
                                          fill=self.fill_colour,
                                          outline="gray",
                                          tags=self.tags)
