from typing import List, Optional
import uuid

# General
from dataclasses import dataclass

# Local libraries
from common import assign_name
from session import SessionContext

# LangChain
from langchain.tools import tool, ToolRuntime

# Topologic
from topologicpy.Vertex import Vertex
from topologicpy.Topology import Topology
from topologicpy.Cell import Cell
from topologicpy.Edge import Edge
from topologicpy.Wire import Wire
from topologicpy.Face import Face

@tool
def create_cylinder(
    runtime: ToolRuntime[SessionContext],
    radius: float,
    height: float,
    name: Optional[str] = None
):
    """Creates a cylinder given radius and height.
    Args:
        radius: radius of the cylinder.
        height: height of the cylinder.
        name (optional): custom name of the cylinder.
    """
    if name is None:
        name = f"cylinder {uuid.uuid4()}"
    
    cylinder = Cell.Cylinder(radius=radius, height=height)
    cylinder = assign_name(cylinder, name)
    runtime.context.session.add(name, cylinder)
    
    return f"A cylinder with name {name} has been created and registered"

@tool
def create_prism(
    runtime: ToolRuntime[SessionContext],
    width: float,
    length: float,
    height: float,
    name: Optional[str] = None
):
    """Creates a prism with a rectangular base given width, length, and height.
    Args:
        width: width of the base rectangle.
        length: length of the base rectangle.
        height: height of the prism.
        name (optional): custom name of the prism.
    """
    if name is None:
        name = f"prism {uuid.uuid4()}"
    
    prism = Cell.Prism(width=width, length=length, height=height)
    prism = assign_name(prism, name)
    runtime.context.session.add(name, prism)
    
    return f"A prism with name {name} has been created and registered"

@tool
def create_circle(
    runtime: ToolRuntime[SessionContext],
    radius: float,
    origin: Optional[List[float]] = None,
    name: Optional[str] = None
):
    """Creates a circle given radius.
    Args:
        radius: radius of the circle.
        origin (optional): origin of the circle that contains [x, y, z] coordinates, by default [0, 0, 0].
        name (optional): custom name of the circle.
    """
    if origin is not None:
        origin = Vertex.ByCoordinates(*origin)
    if name is None:
        name = f"circle {uuid.uuid4()}"
    
    circle = Face.Circle(origin=origin, radius=radius)
    circle = assign_name(circle, name)
    runtime.context.session.add(name, circle)
    
    return f"A circle with name {name} has been created and registered"

@tool
def create_rectangle(
    runtime: ToolRuntime[SessionContext],
    length: float,
    width: float,
    origin: Optional[List[float]] = None,
    name: Optional[str] = None
):
    """Creates a rectangle given length and width.
    Args:
        length: length of the rectangle.
        width: width of the rectangle.
        origin (optional): origin of the rectangle that contains [x, y, z] coordinates, by default [0, 0, 0].
        name (optional): custom name of the rectangle.
    """
    if origin is not None:
        origin = Vertex.ByCoordinates(*origin)
    if name is None:
        name = f"rectangle {uuid.uuid4()}"
    
    rectangle = Face.Rectangle(origin=origin, length=length, width=width)
    rectangle = assign_name(rectangle, name)
    runtime.context.session.add(name, rectangle)
    
    return f"A rectangle with name {name} has been created and registered"

@tool
def create_face(
    runtime: ToolRuntime[SessionContext],
    points: List[List[float]],
    name: Optional[str] = None
):
    """Creates a face given a list of vertexes.
    Args:
        points: A list of [x, y, z] coordinates to form the face.
        name (optional): custom name of the face.

        To create a face, provide a list of minimum three points with their [x, y, z] coordinates.
    """
    if len(points) < 3:
        return "Error: At least three points are required to create a face."
    if name is None:
        name = f"face {uuid.uuid4()}"
    
    vertices = [Vertex.ByCoordinates(*point) for point in points]
    face = Face.ByVertices(vertices)
    face = assign_name(face, name)
    runtime.context.session.add(name, face)
    
    return f"A face with name {name} has been created and registered"

@tool
def create_wire(
    runtime: ToolRuntime[SessionContext],
    points: List[List[float]],
    is_closed: Optional[bool] = True,
    name: Optional[str] = None
):
    """Creates a wire given a list of vertex names.
    Args:
        points: A list of [x, y, z] coordinates to form the wire.
        is_closed (optional): whether the wire is closed or not, by default True.
        name (optional): custom name of the wire.

        To create a wire, provide a list of minimum two points with their [x, y, z] coordinates.
    """
    if len(points) < 2:
        return "Error: At least two points are required to create a wire."
    if name is None:
        name = f"wire {uuid.uuid4()}"
    
    vertices = [Vertex.ByCoordinates(*point) for point in points]
    wire = Wire.ByVertices(vertices, close=is_closed)
    wire = assign_name(wire, name)
    runtime.context.session.add(name, wire)
    
    return f"A wire with name {name} has been created and registered"

@tool
def create_vertex(
    runtime: ToolRuntime[SessionContext],
    position: Optional[List[float]] = [0.0, 0.0, 0.0],
    name: Optional[str] = None
):
    """Creates a vertex in the 3D plane given its coordinates.
    Args:
        position: [x, y, z] coordinates of the vertex. By default [0.0, 0.0, 0.0].
        name (optional): custom name of the vertex.
    """
    if name is None:
        name = f"vertex {uuid.uuid4()}"
    
    vertex = Vertex.ByCoordinates(*position)
    vertex = assign_name(vertex, name)
    runtime.context.session.add(name, vertex)
    
    return f"A vertex with name {name} has been created and registered"

@tool
def create_edge(
    runtime: ToolRuntime[SessionContext],
    start: List[float],
    end: List[float],
    name: Optional[str] = None
):
    """Creates an edge given a start and end point.
    Args:
        start: [x, y, z] coordinates of the start point.
        end: [x, y, z] coordinates of the end point.
        name (optional): custom name of the edge.
    """
    if name is None:
        name = f"edge {uuid.uuid4()}"
    
    start_vertex = Vertex.ByCoordinates(*start)
    end_vertex = Vertex.ByCoordinates(*end)
    edge = Edge.ByVertices(start_vertex, end_vertex)
    edge = assign_name(edge, name)
    runtime.context.session.add(name, edge)
    
    return f"An edge with name {name} has been created and registered"

@tool
def create_cube(
    runtime: ToolRuntime[SessionContext],
    size: int,
    origin: Optional[List[float]] = None,
    name: Optional[str] = None
):
    """Creates a cube given an optional name and a size.
    Args:
        size: size of the cube.
        origin (optional): origin of the cube that contains [x, y, z] coordinates, by default [0, 0, 0].
        name (optional): custom name of the cube.
    """
    if origin is not None:
        origin = Vertex.ByCoordinates(*origin)
    if name is None:
        name = f"cube {uuid.uuid4()}"
    
    cube = Cell.Cube(origin=origin, size=size)
    cube = assign_name(cube, name)
    runtime.context.session.add(name, cube)
    
    return f"A cube with name {name} has been created and registered"

@tool
def get_object_info(
    runtime: ToolRuntime[SessionContext],
    name: str,
):
    """Retrieves information about an object in the current session by its name."""
    obj = runtime.context.session.get(name)
    if obj is None:
        return f"No object found with the name '{name}'."
    
    obj_type = type(obj).__name__

    # TODO: Expand with more types as needed
    if obj_type == "Vertex":
        coords = Vertex.Coordinates(obj)
        return f"Object '{name}' is a Vertex located at coordinates {coords}."

    return f"Object '{name}' is of type '{obj_type}'."

@tool
def list_session_items(
    runtime: ToolRuntime[SessionContext],
):
    """Lists all items in the current session."""
    names = runtime.context.session.get_all_names()
    if not names:
        return "The session is empty."
    
    item_list = "\n".join([f"- {name}" for name in names])
    return f"Current session items:\n{item_list}"

@tool
def clear_session(
    runtime: ToolRuntime[SessionContext],
):
    """Delete/Clear all objects from current session."""
    runtime.context.session.items = {}
    return f"The session has been deleted"
