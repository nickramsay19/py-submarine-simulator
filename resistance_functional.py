from math import pi as PI, sqrt, sin, cos, atan2
from vec import VecXZ, VecY, VecX

def line_projected_area2d(a: VecY, line_s: VecXZ, line_a: VecY, line_d: VecX) -> float:
    a_normalized = line_a - a # normalise line angle to the camera
    # ... assuming that line_a.y = 0 is horizontal projected area of the full line_h

    # positions of both line endpoints
    p0 = Vec2D(line_s.x - (line_d.x/2)*cos(a_normalized.y), line_s.z - (line_d.x/2)*sin(a_normalized.y))
    p1 = Vec2D(line_s.x + (line_d.x/2)*cos(a_normalized.y), line_s.z + (line_d.x/2)*sin(a_normalized.y))
    p2 = Vec2D(p1.x, p2.z) # a third point forming a right angle at p0p2p1

    # the hypotenuse p0p1 has length line_d.x
    # p1p2 has length p1.z - p0.z

    # the camera has no position since its a flat infinite width projection, 
    # ... so we assume its "positioned" at p1, which forms an angle p2p1p3
    # ... we want the projected area of the line segment p1p3

    return sqrt(line_h**2 - (p1.z-p0.z)**2)

def circle_projected_area2d(a: VecY, circle_s: VecXZ, circle_a: VecY, circle_r: VecX) -> float:
    return 2*PI*line_projected_area(a, circle_s, circle_a, circle_r)

def cylinder_projected_area2d(a: VecY, cylinder_s: VecXZ, cylinder_a: VecY, cylinder_h: VecX, cylinder_r: VecX) -> float:
    # since its a flat projection, we don't need to worry about perspective.
    # specifically, we allow the cylinder diameter to be fully projected 
    # ... over the flat projection, thus:
    body_area = (2*cylinder_r.x)*line_projected_area(a, cylinder_s, cylinder_a, cylinder_h.x)

    # we must also consider the cylinder circle top and bottom, 
    # however, at least one will always be covered
    # interestingly, we can pick either of the two circle caps and use it, since
    # ... either will be the exact same contribution of area

    cap_s = Vec2D(cylinder_s.x - (cylinder_h/2)*cos(a.y), cylinder.s.z - (cylinder_h.x/2)*sin(a.y))
    cap_a = cylinder_a + PI/2 # the cylinder caps are perpendicular to the cylinder body
    cap_area = = circle_projected_area(a, cap_s, cap_a, cylinder_r)

    return body_area + cap_area

def square_projected_area2d(a: VecY, square_s: VecXZ, square_a: VecY, square_d: VecXZ) -> float:
    a_normalized = square_s - a

    p00 = VecXZ(square_s.x - (square_d.x/2)*cos(a_normalized), square_s.z - (square_d.z/2)*sin(a_normalized))
    p10 = VecXZ(p00.x + square_d.x, p00.z)
    p01 = VecXZ(p00.x, p00.z + square_d.z)
    p11 = VecXZ(p10.x, p01.z)

    p00p10 = sqrt(square_d.x**2 - (p10.z-p00.z)**2)
    p00p01 = sqrt(square_d.z**2 - (p01.x-p00.x)**2)

    return p00p10*p00p01

def resistant_force2d(rho: float, v: VecXZ, area: float, drag_coeff: float) -> VecXZ:
    return rho*v**2*area*drag*coeff/2

def cylinder_resistant_force2d(a: VecY, cylinder_s: VecXZ, cylinder_v: VecXZ, cylinder_r: float, cyclinder_drag_coeff: float, medium_rho: float) -> VecXZ:
    cylinder_a = VecY(atan2(cylinder_v.x, cylinder_v.z))
    return resistance_force2d(medium_rho, cylinder_v, cylinder_projected_area2d(a, cylinder_s, cylinder_a, cylinder_r), cylinder_drag_coeff)

def square_resistant_force2d(a: VecY, square_s: VecXZ, square_v: VecXZ, square_d: VecXZ, square_drag_coeff: float, medium_rho: float) -> VecXZ:
    square_a = VecY(atan2(square_v.x, square_v.z))
    area: float = square_projected_area2d(a, square_s, square_a, square_d)
    return resistance_force2d(medium_rho, square_v, area, square_drag_coeff)
