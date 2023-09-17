<h1 align="center">Orienteering Path Planner - Python</h1>
<div align="center">
     <h4 align="center">This project aims to assist orienteering participants in finding the optimal path through a given course.
        It takes into account terrain information, elevation contours, and a set of control points to visit. The algorithm used for pathfinding is A*
     </h4><br/>
     <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
</div>

-----------------------------------------

### Introduction
In the sport of orienteering, participants are given a map with terrain information, elevation contours, and a sequence of locations to visit known as "controls".
The goal is to find the best path considering both terrain types and elevation changes.

-----------------------------------------

### Map Information
* `Terrain Map`: A 395x500 color-coded map representing different types of terrain. Each pixel corresponds to an area of 10.29 m (X) by 7.55 m (Y).
* `Elevation Map`: A 400x500 text file containing elevation values (in meters) corresponding to the terrain map. The last five values on each line are ignored.

-----------------------------------------

### Basic Event
The event consists of a set of control points to visit. These points are provided in a text file, with two integers per line representing the (x,y) pixel coordinates on the terrain map.

-----------------------------------------

### Terrain Legend

* `Open land (A)`: #F89412 (248,148,18)
* `Rough meadow (B)`: #FFC000 (255,192,0)
* `Easy movement forest (C · D)`: #FFFFFF (255,255,255)
* `Slow run forest (E)`: #02D03C (2,208,60)
* `Walk forest (F)`: #028828 (2,136,40)
* `Impassible vegetation (G)`: #054918 (5,73,24)
* `Lake/Swamp/Marsh (H · I · J)`: #0000FF (0,0,255)
* `Paved road (K · L)`: #473303 (71,51,3)
* `Footpath (M · N)`: #000000 (0,0,0)
* `Out of bounds`: #CD0065 (205,0,101)

-----------------------------------------

### Finding the Optimal Path
To find the best path, the program uses the A* search algorithm. The heuristic function is crucial, so choose it carefully to avoid suboptimal paths.

-----------------------------------------

### Project Structure

* `lab1.py`: Main program file.
* `terrain.png`: Simplified terrain map.
* `mpp.txt`: Elevation data.
* `red.txt`: Control points file.
* `output.png`: Output image with the optimal path.

-----------------------------------------

### Implementation

* `elevationData()`: reads the elevation data from a file.
* `readPath()`: reads the control points from a file.
* `makeGraph()`: generates a graph of nodes representing each point on the map.
* `hn()`: computes the heuristic function based on Euclidean distance and elevation.
* `gn()`: computes the cost of moving from one node to another.
* `AstarSearch()`: implements the A* algorithm to find the optimal path.
* `fallChange()`: and winterChange() adjust weights and colors based on seasonal changes.
* `winterBFS()`: and springBFS() perform BFS for winter and spring seasons respectively.

-----------------------------------------

### Seasons
* `Summer`: Finds the optimal path for summer conditions.
* `Winter`: Considers winter conditions, adjusting weights and colors accordingly.
* `Fall`: Takes into account fall conditions, potentially altering traversal costs.
* `Spring`: Considers spring conditions, potentially changing traversal costs.

-----------------------------------------

### Dependencies

Python 3.x

PIL (Pillow)

-----------------------------------------

### Author
Shivam Mahajan
