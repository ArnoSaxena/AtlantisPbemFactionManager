from math import cos, sin, radians


class ProvinceHexagon:
    def __init__(self, parent_canvas, center_x, center_y, hex_side_size, fill_colour, tags):
        angle = 60
        self.center_x = center_x
        self.center_y = center_y
        self.parent_canvas = parent_canvas
        self.hex_side_size = hex_side_size
        self.top_left_x = center_x - hex_side_size/2
        self.top_left_y = center_y - self.hex_side_size * sin(radians(angle))
        self.fill_colour = fill_colour
        self.tags = tags
        self.report = None

        """
        self.parent_canvas.create_rectangle(
            self.top_left_x - 1,
            self.top_left_y - 1,
            self.top_left_x + 1,
            self.top_left_y + 1,
            fill="blue")
        """

        start_x = self.top_left_x
        start_y = self.top_left_y
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
