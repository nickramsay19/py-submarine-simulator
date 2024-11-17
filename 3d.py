'''
backburner:
- consider how far down the length of the submarine a control surface is placed
- consider resistance to rotating a control surface itself (should always be based on just width and height). include rotor base force and deduct resistance
- consider a generic scalar control surface curvature variable that increases "glide" or "dampening" - drag coefficient (convexity)
- calculate surface cover, if one surface is covered by something else (in the direction of movement, otherwise it has no effect anyway), then only include the used area of the surface
- propeller thrust calculated from its fan sizes and spin
- natural drag along the hull sides perpendicular to thrust which still experience some friction
- fluid dynamics & water displacement
- hull rotation gradient torque resistance
- center of projected area radii from center of mass y,z as an optimized coefficient of torque
'''

from math import pi as PI, sqrt, sin, cos

G: float = 9.8

DRAG: float = 0.15 # approx drag coefficient of water against a streamline submarine
SURFACE_Z: float = 100.0

# pressure
RHO_AIR: float = 1.225 # kg/m^3
RHO_FRESHWATER_SURFACE: float = 1000
RHO_SEAWATER_SURFACE: float = 1025
BETA_SEAWATER: float = 0.0046 # approx gradient of pressure change per change increase in depth

'''
The submarine components perform calculations relative to a direction vector facing positive x.
The submarine tells the components when executing the calculation where the actual direction is (the direction the sub is facing)
'''

class ControlSurface:
    """on its own this cannot calculate any vectors relative to origin. it calculates control surface area that faces the x direction unit vector. this is then rotated by the owning submarine, depending on where the submarine chooses to place it."""
    width: float = 1    
    height: float = 1    

    xa, ya, za = 0.0, 0.0, 0.0

    def __init__(self, width, height, xa, ya, za):
        self.width = width
        self.height = height
        self.xa = xa
        self.ya = ya
        self.za = za

    def area(self, xa0, ya0, za0): # the surface area facing the input direction
        ya = ya0 + self.ya
        za = za0 + self.za

        h = sqrt(2*self.height**2 - 2*self.height**2*cos(ya))
        w = sqrt(2*self.width**2 - 2*self.width**2*cos(za))

        return h*w

class Propeller:
    """effectively a simple thrust vector calculator tool until further complexity is added e.g. spin"""
    xa, ya, za = 0.0, 0.0, 0.0

    def __init__(self, xa: float = 0.0, ya: float = 0.0, za: float = 0.0):
        self.xa = xa
        self.ya = ya
        self.za = za

    def force(self, xa0, ya0, za0, f) -> tuple[float,float,float]:
        xa = xa0 + self.xa
        ya = ya0 + self.ya
        za = za0 + self.za

        # flip the direction to get forward force
        xf = -f*cos(za)*cos(ya)
        yf = -f*sin(za)
        zf = -f*cos(za)*sin(ya)

        return xf, yf, zf

class BallastTank:
    vol: float # volume
    rho: float # density

    def __init__(self, vol: float = 10.0, rho: float = RHO_SEAWATER_SURFACE):
        self.vol = vol
        self.rho = rho

    def _water_rho(self, zs) -> float:
        depth: float = zs - SURFACE_Z
        return RHO_SEAWATER_SURFACE + BETA_SEAWATER*depth

    def force(self, xs: float, ys: float, zs: float, rho: float = 1.0) -> tuple[float,float,float]:
        # calculate (weight) force of the displaced quanity of water
        m = self.rho*self.vol
        f = m*g
        # TODO: account for rotation and torque that potentially produces other axis forces
        return 0.0, 0.0, f

    # utility function to set the rho parameter from known values of rho for air and water
    def set_air_water_displacement(self, air_prc: float = 0.0):
        water_rho = self._water_rho(zs)
        self.rho = air_prc*RHO_AIR + (1-air_prc)*water_rho
    
class Submarine:
    length: float = 100
    diameter: float = 5 # hull diameter
    rho: float = 1 # density, simpler to think about than to manually set mass, 
    # ... instead calc mass from cylindrical volume
    # NOTE: this is different to the whole sub density which includes the ballast tanks. this density is used for hull calculations

    xs, ys, zs = .0, .0, .0 # displacement (position)
    xv, yv, zv = .0, .0, .0 # velocity
    xa, ya, za = .0, .0, .0 # roll, yaw, pitch, from center of (hull-)mass to projected face, where 0s mean facing towards and along positive x

    # components should be passed angles relative to positive x facing vector, 
    # ... regardless of the angle you define your sub facing
    propeller = Propeller(.0,PI,0.0)
    surfaces = [
        #ControlSurface(1,1,PI/2,PI/2,.0) # plane
    ]
    ballast_tanks = [
        BallastTank()
    ]

    def __init__(self, length: float = 100, diameter: float = 5, density: float = 1, xs: float = .0, ys: float = .0, zs: float = .0, xa: float = .0, ya: float = .0, za: float = .0):
        self.length = length
        self.diameter = diameter
        self.density = density
        self.xs = xs
        self.ys = ys
        self.zs = zs
        self.xa = xa
        self.ya = ya
        self.za = za

        self.hull_projected_area = PI*(self.diameter/2)**2
        self.volume = self.length * self.hull_projected_area
        self.mass = self.volume*self.density

    def tick(self, thrust: float = 2.0, dt: float = 1.0) -> tuple[float,float,float]:

        # calculate projected area needed for friction calc
        area = PI*(self.diameter/2)**2 # hull face
        for surface in self.surfaces: # sum the thrust projected areas
            area += surface.area(self.xa,self.ya,self.za)
            
        # calculate friction 
        # TODO: consider torque of surface angle
        xf_friction = (RHO_WATER*DRAG*area*xv**2)/2
        yf_friction = (RHO_WATER*DRAG*area*yv**2)/2
        zf_friction = (RHO_WATER*DRAG*area*zv**2)/2

        # calculate all additional non-resistance forces
        # incl. the thrust force
        xf_thrust, yf_thrust, zf_thrust = self.propeller.force(self.xa, self.ya, self.za, thrust)

        # buoyant force
        # TODO: the buoyant force has a different projected area!!!
        xf_buoyancy, yf_buoyancy, zf_buoyancy = .0, .0, .0
        for tank in self.ballast_tanks:
            f_tank_buoyancy = tank.force(self.xs, self.ys, self.zs)
            xf_buoyancy += f_tank_buoyancy[0]
            yf_buoyancy += f_tank_buoyancy[1]
            zf_buoyancy += f_tank_buoyancy[2]

        xf = xf_thrust + xf_buoyancy - xf_friction
        yf = yf_thrust + yf_buoyancy - yf_friction
        zf = zf_thrust + zf_buoyancy - zf_friction

        # revert to accellerations (yes this is innefficient and unnecessary, but its very understandable)
        xc = xf / self.mass
        yc = yf / self.mass
        zc = zf / self.mass

        self.xv += xc / dt
        self.yv += yc / dt
        self.zv += zc / dt

        self.xs += self.xv
        self.ys += self.yv
        self.zs += self.zv
        
    def __str__(self) -> str:
        return f'Submarine({self.xs},{self.ys},{self.zs},{self.xa},{self.ya},{self.za})'

    def __repr__(self) -> str:
        return self.__str__()

    def reset(self): # for debugging
        self.xs = .0
        self.ys = .0
        self.zs = .0

        self.xv = .0
        self.yv = .0
        self.zv = .0

        self.xa = .0
        self.ya = .0
        self.za = .0
        
def main():
    propeller = Propeller()
    propeller.ya = PI/2
    print(propeller.force(.0, .0, .0, 100))

    sub = Submarine()
    sub.ya = PI/4
    sub.tick()
    print(sub)

if __name__ == '__main__':
    main()
    print()

    
