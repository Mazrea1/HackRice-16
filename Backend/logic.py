"""
logic.py

Machine -> free-weight/bodyweight exercise swap logic, plus a "saved
exercises" list the user can add to and remove from to view later.

The whole process is broken into small, single-purpose functions so each
step can be explained on its own:

    Machine swap:
        1. load_exercises              -- read the exercise data from disk
        2. find_exercise_by_id         -- look up one exercise by its id
        3. find_non_machine_alternative -- fallback search by muscle group
        4. get_machine_swap            -- ties the above into one answer

    Saved exercises (persisted to a JSON file):
        5. load_saved_exercises        -- read the user's saved list
        6. write_saved_exercises       -- write the user's saved list
        7. add_saved_exercise          -- add one exercise to the saved list
        8. delete_saved_exercise       -- remove one exercise from the list

Only `get_machine_swap`, `add_saved_exercise`, and `delete_saved_exercise`
are meant to be called from outside this file; the rest exist to keep each
piece of logic easy to point at and explain.

To see this in action, run demo.py in this same folder.
"""

import json
import os
from typing import Any, Dict, List, Optional, Tuple

# Absolute path to saved_exercises.json, anchored to this file's own
# location (Backend/logic.py) rather than the caller's working directory.
# This guarantees it always resolves to the sibling "Data" folder, no
# matter where the script is run from.
DEFAULT_SAVED_EXERCISES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "Data", "saved_exercises.json"
)


# ---------------------------------------------------------------------------
# Step 1: Load the data
# ---------------------------------------------------------------------------
def load_exercises(filepath: str) -> List[Dict[str, Any]]:
    """Read the exercise list from a JSON file into a Python list of dicts."""
    with open(filepath, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Step 2: Find one exercise by id
# ---------------------------------------------------------------------------
def find_exercise_by_id(
    exercise_id: str,
    exercises: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Return the exercise dict matching exercise_id, or None if not found."""
    for exercise in exercises:
        if exercise.get("id") == exercise_id:
            return exercise
    return None


# ---------------------------------------------------------------------------
# Step 3: Fallback search -- any non-machine exercise for the same muscle
# ---------------------------------------------------------------------------
def find_non_machine_alternative(
    muscle_group: str,
    exclude_id: str,
    exercises: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Return the first non-machine exercise that trains the same muscle_group,
    skipping the original exercise itself. Used when an exercise has no
    swap_id set.
    """
    for candidate in exercises:
        if (
            candidate.get("id") != exclude_id
            and candidate.get("is_machine") is False
            and candidate.get("muscle_group") == muscle_group
        ):
            return candidate
    return None


# ---------------------------------------------------------------------------
# Step 4: Put it all together
# ---------------------------------------------------------------------------
def get_machine_swap(
    exercise_id: str,
    exercises: List[Dict[str, Any]]
) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Given a machine exercise's id, return a free-weight/bodyweight
    alternative and an explanation of how it was chosen.

    Decision process (in order):
      a) Exercise not found                -> (None, error message)
      b) Exercise is not a machine         -> (None, "no swap needed")
      c) Exercise has a swap_id            -> return that exact exercise
      d) No swap_id                        -> return any non-machine
                                               exercise with the same
                                               muscle_group
      e) Nothing matches in (d)            -> (None, explanation)

    Returns:
        (swap_exercise, message)
    """
    exercise = find_exercise_by_id(exercise_id, exercises)
    if exercise is None:
        return None, f"No exercise found with id '{exercise_id}'."

    if not exercise.get("is_machine"):
        return None, f"'{exercise['name']}' is not a machine; no swap needed."

    swap_id = exercise.get("swap_id")
    muscle_group = exercise.get("muscle_group")

    # (c) Direct swap_id lookup
    if swap_id:
        swap_exercise = find_exercise_by_id(swap_id, exercises)
        if swap_exercise is not None:
            return swap_exercise, (
                f"Swapped '{exercise['name']}' for '{swap_exercise['name']}' "
                f"(direct swap)."
            )

    # (d) Fallback: any non-machine exercise for the same muscle group
    alternative = find_non_machine_alternative(muscle_group, exercise_id, exercises)
    if alternative is not None:
        return alternative, (
            f"'{exercise['name']}' had no direct swap set; found "
            f"'{alternative['name']}' as a {muscle_group.lower()} alternative."
        )

    # (e) Nothing found at all
    return None, (
        f"No swap available for '{exercise['name']}' -- no swap_id set and "
        f"no non-machine exercise found for muscle group '{muscle_group}'."
    )


# ---------------------------------------------------------------------------
# Step 5: Load the user's saved exercises
# ---------------------------------------------------------------------------
def load_saved_exercises(filepath: str = DEFAULT_SAVED_EXERCISES_PATH) -> List[Dict[str, Any]]:
    """
    Read the user's saved-exercises list from a JSON file.
    Returns an empty list if the file doesn't exist yet, is empty, or
    contains invalid/corrupted JSON -- rather than crashing the app.
    """
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        content = f.read().strip()
    if not content:
        return []
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return []


# ---------------------------------------------------------------------------
# Step 6: Write the user's saved exercises back to disk
# ---------------------------------------------------------------------------
def write_saved_exercises(filepath: str, saved_exercises: List[Dict[str, Any]]) -> None:
    """Overwrite the saved-exercises JSON file with the current list."""
    with open(filepath, "w") as f:
        json.dump(saved_exercises, f, indent=2)


# ---------------------------------------------------------------------------
# Step 7: Add an exercise to the saved list
# ---------------------------------------------------------------------------
def add_saved_exercise(
    exercise_id: str,
    exercises: List[Dict[str, Any]],
    saved_filepath: str = DEFAULT_SAVED_EXERCISES_PATH
) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Look up exercise_id in the full exercise catalog and, if found, add it
    to the user's saved list (persisted at saved_filepath).

    Returns:
        (exercise_dict, message) -- exercise_dict is None if exercise_id
        doesn't exist in the catalog at all.
    """
    exercise = find_exercise_by_id(exercise_id, exercises)
    if exercise is None:
        return None, f"No exercise found with id '{exercise_id}'."

    saved_exercises = load_saved_exercises(saved_filepath)

    if find_exercise_by_id(exercise_id, saved_exercises) is not None:
        return exercise, f"'{exercise['name']}' is already saved."

    saved_exercises.append(exercise)
    write_saved_exercises(saved_filepath, saved_exercises)
    return exercise, f"Saved '{exercise['name']}' for later."


# ---------------------------------------------------------------------------
# Step 8: Remove an exercise from the saved list
# ---------------------------------------------------------------------------
def delete_saved_exercise(
    exercise_id: str,
    saved_filepath: str = DEFAULT_SAVED_EXERCISES_PATH
) -> Tuple[bool, str]:
    """
    Remove exercise_id from the user's saved list (persisted at
    saved_filepath), if it's there.

    Returns:
        (success, message) -- success is False if the exercise wasn't in
        the saved list to begin with.
    """
    saved_exercises = load_saved_exercises(saved_filepath)

    exercise = find_exercise_by_id(exercise_id, saved_exercises)
    if exercise is None:
        return False, f"No saved exercise found with id '{exercise_id}'."

    saved_exercises = [ex for ex in saved_exercises if ex.get("id") != exercise_id]
    write_saved_exercises(saved_filepath, saved_exercises)
    return True, f"Removed '{exercise['name']}' from saved exercises."