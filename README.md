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

  ```
  Should check if move is legal using legal_move method before adding it to the list:
  ```
  
  ``go.py:80`` modified ``available_moves`` method to check if move is legal using ``legal_move`` before adding it to ``moves`` as follows:
  ```python
  if self.legal_move((row, col)):
      moves.append((row, col))
  ```

  ______________

  ```
  Issues with capture logic. I attempted to set up the following board to see if a simple capture works.
  I would suggest you implement it and try to debug why captures are not working as expected:
  ·  ·  ·  ·  ·
  ·  B  B  B  ·
  B  W  W  W  ·
  ·  B  B  B  ·
  ·  ·  ·  ·  ·
  ```

  ``ZIAD COMMENT``
  ______________

  ```
  Shouldn't check if piece is not self._turn, you're allowed to have self-captures per the writeup on canvas.
  ```

  ``go.py:148`` modified line to no longer check if piece is not `self._turn` but only if piece is not `None`, allowing self-capture as follows:
  ```python
  if self.piece_at(adjacent_pos) is not None:
  ```

  ______________
  ```
    Also, there are some issues with scoring logic. I tried setting up a couple random board and testing your function on them and it didn't return the correct score. 
  
  ·  ·  ·  ·  ·  ·  ·  ·  ·
  ·  ·  B  ·  ·  ·  W  ·  ·
  ·  B  ·  B  ·  W  ·  W  ·
  ·  B  ·  B  ·  ·  W  ·  ·
  ·  ·  B  ·  ·  ·  ·  W  ·
  
  This returns player 1's score as 7 when in fact it should be 8. 
  
  Similarly, when I set up the following board, it also miscalculated the score:
  ·  ·  B  ·  W  ·
  .  B  ·  ·  ·  W
  B  ·  ·  ·  ·  ·
  
  I suggest working through these examples as a starting point to debug the function (note that these are not exhaustive and it is suggested to try to come up with more examples to test).
  ```
  
  ``ZIAD COMMENT``

  ______________
  ```
  This only checks if we have enough rows in our board, but you should check that each row has enough columns too.
  ```
  
  ``go.py:285`` modified `load_game` to check for individual row length as follows:
  ```python
  for row in grid:
      if len(row) != self._side:
          raise ValueError("Invalid grid size")
  ```
  ______________
  

  ```
  A value can be None which is technically not in this range but a completely valid value
  ```
  
  ``go.py:290`` modified line in `load_game` to not only check if value is not in range, but also not `None` as follows:
  ```python
  if piece not in range(1, self._players+1) and piece is not None
  ```

* **GUI**:
  This component received two S's in Milestone 2
  
* **TUI**:
  This component received two S's in Milestone 2

* **Bot**:
  This component received two S's in Milestone 2

* **QA**:
  This component received two S's in Milestone 2
