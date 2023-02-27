# Laser Cut Desk Organizer
Generates an svg file of parts for a desk organizer that can be laser cut

Software Description:

For this assignment I built two classes to abstract shape and component creation in such a way that I can effectively create any combination of parts, joints, and size that I desire, as well as the ability to adjust for various screws and nuts. By using these classes in my main method, I can design any desk organizer I want. The SVG printout provided above was just one potential implementation. Beyond this assignment, my next step will be to generate a third class called ‘Desk Organizer’ that will make it easier for users to change design parameters via command line.

Shape Class

The Shape class represents a 2D shape with a set of points defining its boundaries. It provides methods for generating and manipulating shapes, and for converting shapes to and from SVG code.

Constructor
def __init__(self, points=None):
The constructor initializes a Shape object with a list of points. If no points are specified, an empty list is used.

Parameters
points (list of tuples, optional): A list of tuples representing the x, y coordinates of the shape's boundary points. The default value is None.

Methods

get_points()
This method returns a list of tuples representing the x, y coordinates of the shape's boundary points.

get_center()
This method returns the center point of the shape as an x, y tuple.

get_bounding_box()
This method returns the bounding box of the shape as a tuple containing the x, y coordinates of the top-left corner, and the width and height of the box.

get_length()
This method returns the length of the shape.

get_width()
This method returns the width of the shape.

get_area()
This method returns the area of the shape.

set_points(points)
This method sets the list of points that define the shape's boundaries.

move_to(x, y)
This method moves the shape to a new location by changing the coordinates of all its boundary points.

rotate(angle)
This method rotates the shape around its center by a specified angle.

generate_circle(radius, center)
This method generates a circle with a given radius and center.

generate_rectangle(width, height, direction, point)
This method generates a rectangle with a given width and height, at a specified direction and point.

generate_rectangle_tower(length, width, joint_type, num_joints, point, direction, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter)
This method generates a rectangular tower shape with a given length and width, number and type of joints, and screw and nut specifications.

generate_polygon(num_sides, side_length, center)
This method generates a regular polygon with a specified number of sides, side length, and center.

generate_polygon_with_junctions(num_sides, joint_type, num_joints, area, point)
This method generates a polygon with a given number of sides, type of joints, number of joints, area, and starting point.

to_svg(scaling_factor)
This method returns an SVG representation of the shape as a string, with all coordinates scaled by a specified factor.


Component Class
The Component class represents a group of 2D shapes needed to make a component. It contains a dictionary of shapes which each contain all the points needed to make that shape. The outermost shape that contains all the other shapes is set as the mother shape. The component can be moved around as a whole and rotated.

Constructor
def __init__(self, name = 'default', mother_shape=None, shapes=[], components=[], fractal=[]):
The constructor for the Component class. It takes in the following arguments:

Parameters:
name: a string representing the name of the component (default: 'default')
mother_shape: an instance of the Shape class representing the outermost shape that contains all other shapes (default: None)
shapes: a list of instances of the Shape class representing the shapes in the component (default: [])
components: a list of instances of the Component class representing the components in the component (default: [])
fractal: a list of tuples representing the points of the fractal in the component (default: [])

Methods:

get_shapes():
Returns a list of shapes in the component.

get_components():
Returns a list of components in the component.

get_mother_shape(ignore_Error=False):
Returns the mother shape of the component, or raises an error if no mother shape has been set.

get_bounding_box():
Returns the bounding box of the mother shape, or an error message if no mother shape has been set.

get_length():
Returns the length of the mother shape.


get_width():
Returns the width of the mother shape.

__inside_shape(box1, box2):
A private method that checks if Bound Box 1 is inside Bound Box 2.

get_logo_dimensions(logo_svg):
Returns the dimensions of the logo.

to_svg(svg_code="", scaling_factor=1):
Converts the component to an SVG representation as a string.

set_mother_shape(shape):
Sets the mother shape of the component.

add_shape(shape, point, mother=False, ignore_error=False):
Adds a shape to the component.

add_component(component, point):
Adds a component to the component.

move_to(x, y):
Moves the component to a new x and y position.

rotate(angle):
Rotates the component and its child components by a specified angle around the center.

generate_junction_holes(point, direction, screw_length, nut_width, sheet_thickness, nut_thickness, slot_length, screw_diameter, include_screw=True):
Generates junction holes for joining the shapes.

generate_text(text, point, direction):
Generates text at the specified point with the specified direction.

embed_logo(point, scaling_factor):
Embeds a logo at the specified point with the specified scaling factor.
