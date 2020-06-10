# CoordinatePython

Line Class is the class that represents line between two points.(limited functions)

Triangle class is the class that represents triangle.(limited functions)

Point Class is the class that represents Point.

CartesianCoordinate Class is class for static methods:
- calculate_angle(point1: Point, point2: Point, point3: Point) 
  -> Calculates angle between lines point1-point3 and point2-point3. Returns angle value. Uses Law of Cosines
  
- calculate_distance_to_origin(point: Point) -> Calculates distance between origin and given point. Returns distance value.

- calculate_area(*args: Point) -> Calculates area of polygon that contains given points. Returns area value.

- calculate_triangle_area(point1: Point, point2: Point, point3: Point) -> Calculates area of triangle that created by given points
Returns area value. Uses Law of Cosines and Law of Sines.

- check_is_on_same_line(point1: Point, point2: Point, point3: Point) -> Checks are these points on same line. Returns bool value

- check_point_situation_to_line(point1: Point, point2: Point, point_to_check: Point) -> Checks situation of point to the line that is between point1 and point2. Returns SituationsForPointAndLine based on Points is on the line(.Contains), below the line(.Below), above the line(.Above).

- calculate_slope_two(point1: Point, point2: Point) -> Calculates slope of line that is between point1 and point2. Returns slope value.

- calculate_distance(point1: Point, point2: Point) -> Calculates distance between given points. Returns distance value. Uses Pythagorean Theorem.

- center_point_between_two(point1: Point, point2: Point) -> Calculates center point of line between point1 and point2. Returns Point

- find_region(point: Point) ->  Returns region of point.
