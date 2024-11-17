from __future__ import annotations
from typing import Any, override
import abc
from math import pi as PI, sqrt, sin, cos, atan2
from vec import VecXZ, VecY, VecX
from polytope import SizePolygon, Line, Circle, Cylinder

class ResistantPolygon(SizePolygon):
    cd: float # drag coefficient

    @staticmethod
    def _projected_area_drag_force(v: Vec, area: float, p: float, cd: float) -> float:
        '''
        Calculates the drag force exerted on an object based on its velocity, projected area, air density, and drag coefficient.
        
        Parameters:
        -----------
        v : Vec
            The velocity vector (or scalar magnitude) of the object relative to the fluid (e.g., air or water) in meters per second (m/s).
        
        area : float
            The projected area of the object facing the fluid flow (in square meters, m²). This is the area of the object as "seen" by the oncoming fluid.
        
        p : float
            The fluid density (in kilograms per cubic meter, kg/m³). For example, the density of air at sea level is approximately 1.225 kg/m³.
        
        cd : float
            The drag coefficient (dimensionless). This is a unitless number that quantifies the object's aerodynamic or hydrodynamic resistance. A streamlined object has a lower drag coefficient than a blunt object.
        
        Returns:
        --------
        float
            The drag force (in newtons, N) exerted on the object by the fluid. The drag force opposes the object's motion through the fluid.
        
        Formula:
        --------
        The drag force is calculated using the following formula:
        F_d = (1/2) * cd * p * A * v²
        
        Where:
            F_d = drag force (N)
            cd = drag coefficient (dimensionless)
            p = fluid density (kg/m³)
            A = projected area (m²)
            v = velocity (m/s)
        
        '''
        return (p * v**2 * area * cd)/2

    @abc.abstractmethod
    def _projected_area(self) -> float:
        pass

    def _drag_force(self, p: float) -> VecXZ:
        return self.projected_area_drag_force(v, self.projected_area(v), p, self.cd)

    def apply_drag_force(self, p: float):
        self.apply_force(self._drag_force(p))

class ResistantLine(ResistantPolygon, Line):
    @override
    def _projected_area(self) -> float:
        # positions of both line endpoints
        p0 = Vec2D(self.s.x - (self.d.x/2)*cos(self.a.y), self.s.z - (self.d.x/2)*sin(self.a.y))
        p1 = Vec2D(self.s.x + (self.d.x/2)*cos(self.a.y), self.s.z + (self.d.x/2)*sin(self.a.y))
        return sqrt(d.x**2 - (p1.z-p0.z)**2)

class ResistantCircle(ResistantPolygon, Circle):
    @override
    def _projected_area(self) -> float:
        return PI*(super(self, ResistantLine).projected_area()/2)**2

class ResistantCylinder(ResistantPolygon, Cylinder):
    cap: ResistantCircle

    @override
    def _projected_area(self) -> float:
        # since its a flat projection, we don't need to worry about perspective.
        # we can simply multiply the diameter by the line's projected area
        body_area = cap.diameter*super().projected_area()

        # we must also consider the cylinder circle top and bottom, 
        # however, at least one will always be covered
        # interestingly, we can pick either of the two circle caps and use it, since
        # ... either will be the exact same contribution of area
        return body_area + cap_projected_area() 
