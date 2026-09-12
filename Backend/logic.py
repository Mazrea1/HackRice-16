import json
from typing import Any, Dict, List, Optional, Tuple


#Loading the data from the JSON file
def load_exercises(filepath: str) -> List[Dict[str, Any]]:
    """Read the exercise list from a JSON file into a Python list of dicts."""
    with open(filepath, "r") as f:
        return json.load(f)


#exercise search function
def find_exercise_by_id(
    exercise_id: str,
    exercises: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Return the exercise dict matching exercise_id, or None if not found."""
    for exercise in exercises:
        if exercise.get("id") == exercise_id:
            return exercise
    return None


#Finding replacement exercise
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