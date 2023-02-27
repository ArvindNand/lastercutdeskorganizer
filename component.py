import math
import random
import matplotlib.font_manager as fm


# The Shape class represents a basic shape in a 2D plane.
# It contains the points that make up the shape, as well
# as its center x and y coordinates.
class Shape:
    # Initialize Shape class with points
    def __init__(self, points=None):
        if points:
            self.set_points(points)
        self.junction_points = []

    # Get the points of the shape
    def get_points(self):
        points = self.points
        if not points:
            raise ValueError("Error: No points have been set for this component")
        return points

    # Get the bounding box of the shape
    def get_bounding_box(self):
        x_values = [point[0] for point in self.get_points()]
        y_values = [point[1] for point in self.get_points()]
        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)
        return (min_x, min_y, max_x, max_y)

    # Get the x point of the shape (center)
    def get_x(self):
        points = self.get_points()
        l = len(points)
        return sum(p[0] for p in self.get_points()) / l

    # Get the y point of the shape (center)
    def get_y(self):
        points = self.get_points()
        l = len(points)
        return sum(p[1] for p in self.get_points()) / l

    # Get the center of the shape as an x,y tuple
    def get_center(self):
        return (self.get_x(), self.get_y())

    # Get the width of the shape
    def get_width(self):
        return max(p[0] for p in self.get_points()) - min(p[0] for p in self.get_points())

    # Get the length of the shape
    def get_length(self):
        return max(p[1] for p in self.get_points()) - min(p[1] for p in self.get_points())
    
    # return a list where each item is list of points for a junction
    def get_junction_points(self):
        return self.junction_points
    
    def store_junction_points(self, points:list):
        self.junction_points.append(points)

    # Get the area of the shape
    def get_area(self) -> float:
        n = len(self.points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.points[i][0] * self.points[j][1]
            area -= self.points[j][0] * self.points[i][1]
        area = abs(area) / 2.0
        return area

    # Set the points of the shape
    def set_points(self, points):
        if type(points) != list or not all(isinstance(p, tuple) and len(p) == 2 for p in points):
            raise ValueError("points must be a list of (x, y) tuples")
        self.points = points

    # Move the shape to the specified x and y location
    def move_to(self, x, y):
        offset_x = x - self.get_x()
        offset_y = y - self.get_y()
        self.set_points([(x_ + offset_x, y_ + offset_y) for x_, y_ in self.get_points()])

    # Calculate the new point based on the given point, length, and angle
    def calculate_new_point(self, point, length, angle):
        x, y = point
        new_x = x + length * math.cos(math.radians(angle))
        new_y = y + length * math.sin(math.radians(angle))
        return (new_x, new_y)

    # rotate all the points in the shape by the given angle
    # around the center point of the shape.
    def rotate(self, angle):
        origin_x, origin_y = self.get_x(), self.get_y()
        self.set_points([self.rotate_point(point, origin_x, origin_y, angle) for point in self.get_points()])

    # rotate a single point using the given rotation matrix
    def rotate_point(self, point, origin_x, origin_y, angle):
        x, y = point
        new_x = (x - origin_x) * math.cos(math.radians(angle)) - (y - origin_y) * math.sin(math.radians(angle)) + origin_x
        new_y = (x - origin_x) * math.sin(math.radians(angle)) + (y - origin_y) * math.cos(math.radians(angle)) + origin_y
        return (new_x, new_y)

    # generate complex junction as a list of points
    def complex_junction(self, point, direction, junction_name: str, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter):
        new_points = [point]
        # parameters that will change depending on the type
        # of screw, nut and thickness of the sheet being cut
        a = sheet_thickness
        b = slot_length
        e = nut_thickness
        f = nut_width
        d = screw_length - a - e
        g = screw_diameter
        c = (f - g) / 2
        c1 = 6*c
        c2 = c1 + (f - 2*c) + c1

        junction_types = {
            'captive joint slot':[[-90, 0, 90, 0, 90, 180, 90, 0, -90, 180, -90, 0, -90, 0, 90],
                                    [a, b, a, c1, d, c, e, f, e, c, d, c1, a, b, a]],
            'captive joint base':[[90, 0, -90, 0, 90, 0, -90], [a, b, a, c2, a, b, a]],
            'plain slot':[[-90, 0, 90, 0, -90, 0, 90], [a, b, a, c2, a, b, a]]
        }

        angles = junction_types[junction_name][0]
        distances = junction_types[junction_name][1]
        for i in range(len(angles)):
            new_angle = (direction + angles[i] + 360) % 360
            new_points.append(self.calculate_new_point(new_points[-1], distances[i], new_angle))
        c = new_points.copy()
        self.store_junction_points(c)
        return new_points

    # generate side with desired number of junctions as a list of points
    def generate_side_with_complex_junction(self, point, length, direction, junction_name, num_junctions, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter):
        # parameters that will change depending on the type
        # of screw, nut and thickness of the sheet being cut
        a = sheet_thickness
        b = slot_length
        e = nut_thickness
        f = nut_width
        d = screw_length - a - e
        g = screw_diameter
        c = (f - g) / 2
        c1 = 6*c
        c2 = c1 + (f - 2*c) + c1
        if junction_name == 'captive joint slot':
            junction_length =  b + c1 + g + c1 + b
        else:
            junction_length = b + c1 + g + c1 + b
        remaining_length = (length - (junction_length * num_junctions)) / (num_junctions + 1)
        new_points = []
        for i in range(int(num_junctions)):
            new_points.append(self.calculate_new_point(new_points[-1] if i > 0 else point, remaining_length, direction))
            new_points.extend(self.complex_junction(new_points[-1], direction, junction_name, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter))
            new_points.append(self.calculate_new_point(new_points[-1], remaining_length, direction))
        return new_points

    # generate rectangular shelf with desired length, width, and total number of
    # junctions for the short sides as a list of points starting from input
    # point
    def generate_rectangle_shelf(self, length, width, junction_name, num_junctions, starting_point, direction, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter):
        new_points = [starting_point]
        half_captive_junctions = num_junctions / 2
        new_angle = direction
        new_points.extend(self.generate_side_with_complex_junction(new_points[-1], width, new_angle, junction_name, half_captive_junctions, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter))
        new_angle = (new_angle + 90 + 360) % 360
        new_points.append(self.calculate_new_point(new_points[-1], length, new_angle))
        new_angle = (new_angle + 90 + 360) % 360
        new_points.extend(self.generate_side_with_complex_junction(new_points[-1], width, new_angle, junction_name, half_captive_junctions, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter))
        new_angle = (new_angle + 90 + 360) % 360
        new_points.append(self.calculate_new_point(new_points[-1], length, new_angle))
        return new_points

    def generate_rectangle_tower(self, length, width, junction_name, num_junctions, starting_point, direction, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter):
        new_points = [starting_point]
        half_captive_junctions = num_junctions / 2
        new_angle = direction
        new_points.extend(self.generate_side_with_complex_junction(new_points[-1], width, new_angle, junction_name, half_captive_junctions, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter))
        new_angle = (new_angle + 90 + 360) % 360
        new_points.append(self.calculate_new_point(new_points[-1], length, new_angle))
        new_angle = (new_angle + 90 + 360) % 360
        new_points.append(self.calculate_new_point(new_points[-1], width, new_angle))
        new_angle = (new_angle + 90 + 360) % 360
        new_points.append(self.calculate_new_point(new_points[-1], length, new_angle))
        return new_points


    # generate polygon with the desired number of sides, of desired length
    # as a list of points starting from input point.
    def generate_polygon(self, num_sides, side_length, starting_point):
        angle = 360 / num_sides
        new_points = [starting_point]
        current_point = starting_point
        for i in range(num_sides - 1):
            current_point = self.calculate_new_point(current_point, side_length, angle * (i + 1))
            new_points.append(current_point)
        return new_points

    # generate polygon with the desired number of sides, of desired length
    # as a list of points starting from input point.
    def generate_polygon_with_junctions(self, num_sides, junction_name, num_junctions, side_length, starting_point):
        angle = 360 / num_sides
        new_points = [starting_point]
        current_point = starting_point
        for i in range(num_sides - 2):
            current_point = self.calculate_new_point(current_point, side_length, angle * (i + 1))
            new_points.append(current_point)
        new_points.extend(self.generate_side_with_complex_junction(new_points[-1], side_length, angle * (num_sides-1), junction_name, num_junctions, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter))
        return new_points

    def generate_rectangle(self, length, width, direction, starting_point:tuple):
        x, y = starting_point
        new_angle = direction
        new_points = [starting_point]
        new_points.append(self.calculate_new_point(starting_point, length, new_angle))
        new_angle = (new_angle + 90 + 360) % 360
        new_points.append(self.calculate_new_point(new_points[-1], width, new_angle))
        new_angle = (new_angle + 90 + 360) % 360
        new_points.append(self.calculate_new_point(new_points[-1], length, new_angle))
        new_points.append(starting_point)
        return new_points

    # generate circle with the desired radius as a list of points starting 
    # from the input point. Default number of points is 50, but can be set 
    # to be coarser or finer
    def generate_circle(self, radius, start_point, num_points=50):
        new_points = []
        for i in range(num_points + 1):
            angle = 2 * math.pi * i / num_points
            x = start_point[0] + radius * math.cos(angle)
            y = start_point[1] + radius * math.sin(angle)
            new_points.append((x, y))
        return new_points        

    # Convert the shape to SVG code
    def to_svg(self, scaling_factor=1):
        svg = '\n  <polygon points="'
        for point in self.points:
            svg += str(point[0] * scaling_factor) + ',' + str(point[1] * scaling_factor) + ' '
        svg = svg[:-1]  # remove the last space
        svg += '" style="fill:none;stroke:black;stroke-width:1"/>\n'
        return svg



# The Component class represents a group of 2D shapes needed.
# to make a component. It contains a dictionary of shapes
# which each contain all the points needed to make that shape.
# The outermost shape that contins all the other shapes is set
# as the mother shape. The component can be moved around as a
# whole and rotated.
class Component:
    # Initialize Component class with a name, mother shape, and shapes
    def __init__(self, name = 'default', mother_shape=None, shapes=[], components=[], fractal=[]):
        self.name = name
        if shapes is None:
            self.shapes = []
        else:
            self.shapes = shapes
        if components is None:
            self.components = []
        else:
            self.components = components
        self.data = {
            'mother_shape': mother_shape,
            'shapes': shapes,
            'components': components,
            'fractal' : fractal
        }

    # Checks if point is a tuple of two numbers
    def __is_valid_point(self, point):
        if not isinstance(point, tuple) or len(point) != 2:
            raise ValueError("Point must be a tuple of two numbers.")
        if not all(isinstance(i, (int, float)) for i in point):
            raise ValueError("Both values in the point tuple must be numbers.")
        return True

    # Get the shapes in the component
    def get_shapes(self):
        shapes = self.data['shapes']
        if not shapes:
            raise ValueError("Error: No shapes have been set for this component")
        return shapes

    # Get the components in the component
    def get_components(self):
        components = self.data['components']
        if not components:
            raise ValueError("Error: No components have been set for this component")
        return components

    # Get the fractal in the component
    def get_fractal(self):
        fractal = self.data['fractal']
        if not fractal:
            raise ValueError("Error: No fractal has been set for this component")
        return fractal

    # Get the mother shape of the component
    def get_mother_shape(self, ignore_Error=False):
        mother_shape = self.data['mother_shape']
        if not ignore_Error and not mother_shape:
            raise ValueError("Error: No mother shape has been set for this component.")
        return mother_shape

    # Get the center point of the entire component as an x,y tuple
    def get_center(self):
        return self.get_mother_shape().get_center()

    def set_mother_shape(self, shape):
        if not isinstance(shape, Shape):
            raise ValueError("Error: Input variable is not a shape")
        self.data['mother_shape'] = shape

    # Returns the bounding box of the mother shape, or an error message if no mother shape has been set
    def get_bounding_box(self):
        return self.get_mother_shape().get_bounding_box()

    # Returns the length of the Component
    def get_length(self):
        return self.get_mother_shape().get_length()

        # Returns the length of the Component
    def get_width(self):
        return self.get_mother_shape().get_width()

    # Private Method that will report True if Bound Box 1 is inside Bounding Box 2
    def __inside_shape(self, box1, box2):
        bb1 = box1.get_bounding_box()
        bb2 = box2.get_bounding_box()
        return bb1[0] >= bb2[0] and bb1[1] >= bb2[1] and bb1[2] <= bb2[2] and bb1[3] <= bb2[3]

    # Add a shape to the component
    def add_shape(self, shape, point, mother=False, ignore_error=False):
        if mother:
            self.set_mother_shape(shape)
        else:
            if not ignore_error and not self.__inside_shape(shape, self.get_mother_shape()) and not self.__is_valid_point(point):
                raise ValueError("Error: The shape you are trying to add is larger than mother shape")
            else:
                shape.move_to(point[0], point[1])
                self.data['shapes'].append(shape)

    # Add a component to the component
    def add_component(self, component, point):
        current_box = self.get_bounding_box()
        new_box = component.get_bounding_box()
        if self.__inside_shape(new_box, current_box) and self.__is_valid_point(point):
            component.move_to(point[0], point[1])
            self.data['components'].append(component)
        else:
            return "Error: The component you are trying to add is larger than mother component"

    # Moves the component to a new x and y position
    def move_to(self, x, y):
        self.get_mother_shape().move_to(x, y)
        try:
            for shape in self.get_shapes():
                shape.move_to(x, y)
        except ValueError:
            pass
        try:
            for component in self.get_components():
                component.move_to(x, y)
        except ValueError:
            pass

    # Rotate the component and its child components by a specified angle around the center.
    def rotate(self, angle):
        self.get_mother_shape().rotate(angle)
        try:
            for shape in self.get_shapes():
                shape.rotate(angle)
        except ValueError:
            pass
        try:
            for component in self.get_components():
                component.rotate(angle)
        except ValueError:
            pass

    def generate_junction_holes(self, point, direction, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter, include_screw=True):
            # parameters that will change depending on the type
            # of screw, nut and thickness of the sheet being cut
            a = sheet_thickness
            b = slot_length
            e = nut_thickness
            f = nut_width
            d = screw_length - a - e
            g = screw_diameter
            c = (f - g) / 2
            c1 = 6*c
            c2 = 3*c + (f - 2*c) + 3*c

            slot1 = Shape()
            slot1.set_points(slot1.generate_rectangle(b, a, direction, point))
            self.add_shape(slot1, point, ignore_error=True)

            dist = c1 + g + c1
            next_point1 = (point[0] + b + dist, point[1])
            slot2 = Shape()
            slot2.set_points(slot2.generate_rectangle(b, a, direction, next_point1))
            self.add_shape(slot2, next_point1, ignore_error=True)

            gap_start = slot1.get_points()[1]
            gap_end = slot2.get_points()[0]
            gap_center_x = (gap_start[0] + gap_end[0]) / 2
            gap_center_y = (gap_start[1] + gap_end[1] + a) / 2
            next_point = (gap_center_x, gap_center_y)

            if include_screw:
                circle = Shape()
                circle.set_points(circle.generate_circle(g, next_point))
                self.add_shape(circle, next_point, ignore_error=True)

    def generate_text(self, text, point, direction):
        x, y = point
        font_size = int(0.001 * self.get_mother_shape().get_area())
        text_width = len(text) * font_size / 2.35
        x -= text_width / 2
        y += font_size / 2 + self.get_length() / 5
        svg_code = f'<text x="{x}" y="{y}" font-size="{font_size}" transform="rotate({direction}, {x}, {y})">{text}</text>\n'
        return svg_code

    def embed_logo(self, point, scaling_factor):
        logo_file = "logo.svg"
        with open(logo_file, "r") as file:
            logo_svg = file.read()
        width, height = self.get_logo_dimensions(logo_svg)
        x, y = point
        x -= width * scaling_factor / 2
        y -= height * scaling_factor / 2
        svg_code = f'<g transform="translate({x}, {y}) scale({scaling_factor})">\n{logo_svg}\n</g>\n'
        return svg_code

    def get_logo_dimensions(self, logo_svg):
        width_start = logo_svg.index("width") + 7
        width_end = logo_svg.index("\"", width_start)
        height_start = logo_svg.index("height") + 8
        height_end = logo_svg.index("\"", height_start)

        width = float(logo_svg[width_start:width_end])
        height = float(logo_svg[height_start:height_end])

        return (width, height)

    # Converts the component to an SVG representation as a string
    def to_svg(self, svg_code="", scaling_factor=1):
        svg_code += self.get_mother_shape().to_svg(scaling_factor)
        try:
            for shape in self.get_shapes():
                svg_code += shape.to_svg(scaling_factor)
        except ValueError:
            # Handle the error by not adding any shapes to the svg code
            pass
        try:
            for component in self.get_components():
                svg_code += component.to_svg(scaling_factor)
        except ValueError:
            # Handle the error by not adding any components to the svg code
            pass
        try:
            fractal = self.data['fractal']
            if fractal:
                points = " ".join(f"{x * scaling_factor},{y * scaling_factor}" for x, y in fractal)
                svg_code += f'<polyline points="{points}" style="fill:none;stroke:black;stroke-width:1"/>\n'
        except ValueError:
            # Handle the error by not adding any fractals to the svg code
            pass
        return svg_code

if __name__ == '__main__':


    while True:
        try:
            length = float(input(f"Enter Height (default is {100}): "))
            if length <= 0:
                raise ValueError("Height must be greater than 0.")
            break
        except ValueError as e:
            print(f"Error: {e}")
            
    while True:
        try:
            width = float(input(f"Enter width (default is {50}): "))
            if width <= 0:
                raise ValueError("Width must be greater than 0.")
            break
        except ValueError as e:
            print(f"Error: {e}")
            
    while True:
        try:
            shelf_area = float(input(f"Enter shelf area (default is {175}): "))
            if shelf_area <= 0:
                raise ValueError("Shelf area must be greater than 0.")
            break
        except ValueError as e:
            print(f"Error: {e}")
            
    while True:
        try:
            num_shelves = int(input(f"Enter number of shelf holes (default is {2}): "))
            if num_shelves <= 0:
                raise ValueError("Number of shelves must be greater than 0.")
            break
        except ValueError as e:
            print(f"Error: {e}")

    # Define the parameters for the desk organizer
    kerf = 0.2
    num_junctions = 2
    screw_length = 8.5
    nut_width = 4.5
    sheet_thickness = 3 
    nut_thickness = 1.5
    base_area = 250
    font_size = 0.25
    slot_length = 5 
    screw_diameter = 2.1 - kerf

    
    # Convert the input to the correct data type or use the default value if no input is provided
    length = int(length) if length else 100
    width = int(width) if width else 50
    num_shelves = int(num_shelves) if num_shelves else 2
    shelf_area = int(shelf_area) if shelf_area else 175

    # Create the starting point for the rectangular shelf
    starting_point = (20, 20)

    # Generate Rectangular Tower Piece
    tower_shape = Shape()
    tower_shape.set_points(Shape().generate_rectangle_tower(length, width,'plain slot', num_junctions, starting_point, 0, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter))
    desk_organizer = Component()
    desk_organizer.add_shape(tower_shape, starting_point, True)
    c = (nut_width - screw_diameter) / 2
    c1 = 6*c
    junction_length = slot_length + c1 + screw_diameter + c1 + slot_length
    tower_x = tower_shape.get_x() - (c1 + screw_diameter/2)
    tower_y = starting_point[1]
    shelf_height = length / (num_shelves + 1)
    for i in range(num_shelves):
        tower_y += shelf_height
        desk_organizer.generate_junction_holes((tower_x, tower_y), 0, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter)
    components = []

    # Generate Shelves
    starting_points = [(starting_point[0]+(width*2), starting_point[1]),
                    (starting_point[0]+(width*2), starting_point[1]+(length*0.6)),
                    (starting_point[0]+(width*3.5), starting_point[1]),
                    (starting_point[0]+(width*3.5), starting_point[1])]

    num_sides = [6, 4, 3]

    for i in range(len(num_sides)-1):
        new_starting_point = starting_points[i]
        shelf_shape = Shape()
        shelf_shape.set_points(shelf_shape.generate_polygon_with_junctions(num_sides[i],'captive joint slot', 1, shelf_area/num_sides[i], new_starting_point))
        shelf = Component()
        shelf.add_shape(shelf_shape, new_starting_point, True)
        components.append(shelf)
    
    # Generate Base Piece
    shelf_shape = Shape()
    shelf_shape.set_points(shelf_shape.generate_polygon(7, base_area/7, starting_points[3]))
    shelf = Component()
    shelf.add_shape(shelf_shape, new_starting_point, True)
    shelf.generate_junction_holes((shelf_shape.get_x() - (c1 - screw_diameter/2 + slot_length), shelf_shape.get_y()), 0, screw_length, nut_width, sheet_thickness - kerf, nut_thickness, slot_length - kerf, screw_diameter, False)
    text = shelf.generate_text("Digital Manufacturing", (shelf_shape.get_x(), shelf_shape.get_y()), 0)
    logo = shelf.embed_logo((shelf_shape.get_x(), shelf_shape.get_y() - shelf.get_length()/4), 0.05)
    components.append(shelf)


    # Add header to the SVG code
    svg_width = str(500)
    svg_height = str(500)
    scaling_factor = 1
    svg_header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n\n<svg width="{0}" height="{1}"\nxmlns="http://www.w3.org/2000/svg">\n\n'.format(svg_width * scaling_factor, svg_height * scaling_factor)    
    svg_code = svg_header + desk_organizer.to_svg("") + text + logo 
    for c in components:
        svg_code += c.to_svg("")
    svg_code += "</svg>"

    # Save the SVG code to a file
    with open('desk_organizer.svg', 'w') as file:
        file.write(svg_code)
