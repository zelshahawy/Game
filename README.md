# CMSC 14200 Course Project

Team members:
- Esslam Ashour (esslamashour) (TUI)
- Ziad El Shahawy (zelshahawy) (Bot)
- John Rugemalila (johnruge) (QA)
- Ray Simbiri (simbiri) (GUI)

Enhancements:
- GUI title screen
- GUI background music
- GUI animation
- Added `pyproject.toml`

Improvements:
* **Game logic**:

  ``Should check if move is legal using legal_move method before adding it to the list``
  - ``go.py:80``: modified ``available_moves`` method to check if move is legal using ``legal_move`` before adding it to ``moves``

```
Issues with capture logic. I attempted to set up the following board to see if a simple capture works. I would suggest you implement it and try to debug why captures are not working as expected:

·  ·  ·  ·  ·
 ·  B  B  B  ·
B  W  W  W  ·
·  B  B  B  ·
·  ·  ·  ·  ·
```
  

* **GUI**:
  This component received two S's in Milestone 2
  
* **TUI**:
  This component received two S's in Milestone 2

* **Bot**:
  This component received two S's in Milestone 2

* **QA**:
  This component received two S's in Milestone 2
