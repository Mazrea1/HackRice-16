"""
logic.py

Exercise catalog logic: machine swaps, saved exercises, and workout plans.
See demo.py for usage examples.
"""

import json
import os
from typing import Any, Dict, List, Optional, Tuple

# Anchored to this file's location so it always finds the sibling Data
# folder, regardless of the caller's working directory.
DEFAULT_SAVED_EXERCISES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "Data", "saved_exercises.json"
)


def load_exercises(filepath: str) -> List[Dict[str, Any]]:
    """Load the exercise catalog from a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def find_exercise_by_id(
    exercise_id: str,
    exercises: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Find one exercise by id, or None."""
    for exercise in exercises:
        if exercise.get("id") == exercise_id:
            return exercise
    return None


def find_alternative_by_type(
    muscle_group: str,
    exclude_id: str,
    exercises: List[Dict[str, Any]],
    want_machine: bool
) -> Optional[Dict[str, Any]]:
    """Fallback: first exercise of the given type (machine or not) for the same muscle group."""
    for candidate in exercises:
        if (
            candidate.get("id") != exclude_id
            and candidate.get("is_machine") is want_machine
            and candidate.get("muscle_group") == muscle_group
        ):
            return candidate
    return None


def find_reverse_swap(exercise_id: str, exercises: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find a machine exercise whose swap_id points back to exercise_id."""
    for candidate in exercises:
        if candidate.get("is_machine") and candidate.get("swap_id") == exercise_id:
            return candidate
    return None


def get_alternative_exercise(
    exercise_id: str,
    exercises: List[Dict[str, Any]]
) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Suggest an alternative for any exercise: a machine gets a free-weight/
    bodyweight swap, a free-weight/bodyweight exercise gets a machine
    option -- so there's always another option if someone doesn't like
    the one they're looking at.
    Returns (alternative_exercise, message).
    """
    exercise = find_exercise_by_id(exercise_id, exercises)
    if exercise is None:
        return None, f"No exercise found with id '{exercise_id}'."

    is_machine = exercise.get("is_machine")
    muscle_group = exercise.get("muscle_group")
    want_machine = not is_machine

    if is_machine and exercise.get("swap_id"):
        direct = find_exercise_by_id(exercise["swap_id"], exercises)
        if direct is not None:
            return direct, f"Swapped '{exercise['name']}' for '{direct['name']}' (direct swap)."

    if not is_machine:
        reverse = find_reverse_swap(exercise_id, exercises)
        if reverse is not None:
            return reverse, f"Swapped '{exercise['name']}' for '{reverse['name']}' (machine option)."

    alternative = find_alternative_by_type(muscle_group, exercise_id, exercises, want_machine)
    if alternative is not None:
        return alternative, f"Found '{alternative['name']}' as an alternative to '{exercise['name']}'."

    return None, f"No alternative found for '{exercise['name']}'."


def load_saved_exercises(filepath: str = DEFAULT_SAVED_EXERCISES_PATH) -> List[Dict[str, Any]]:
    """Load the user's saved-exercises list. Empty/missing/invalid file -> []."""
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


def write_saved_exercises(filepath: str, saved_exercises: List[Dict[str, Any]]) -> None:
    """Overwrite the saved-exercises file with the current list."""
    with open(filepath, "w") as f:
        json.dump(saved_exercises, f, indent=2)


def add_saved_exercise(
    exercise_id: str,
    exercises: List[Dict[str, Any]],
    saved_filepath: str = DEFAULT_SAVED_EXERCISES_PATH
) -> Tuple[Optional[Dict[str, Any]], str]:
    """Add an exercise to the saved list, if it exists and isn't already saved."""
    exercise = find_exercise_by_id(exercise_id, exercises)
    if exercise is None:
        return None, f"No exercise found with id '{exercise_id}'."

    saved_exercises = load_saved_exercises(saved_filepath)

    if find_exercise_by_id(exercise_id, saved_exercises) is not None:
        return exercise, f"'{exercise['name']}' is already saved."

    saved_exercises.append(exercise)
    write_saved_exercises(saved_filepath, saved_exercises)
    return exercise, f"Saved '{exercise['name']}' for later."


def delete_saved_exercise(
    exercise_id: str,
    saved_filepath: str = DEFAULT_SAVED_EXERCISES_PATH
) -> Tuple[bool, str]:
    """Remove an exercise from the saved list, if it's there."""
    saved_exercises = load_saved_exercises(saved_filepath)

    exercise = find_exercise_by_id(exercise_id, saved_exercises)
    if exercise is None:
        return False, f"No saved exercise found with id '{exercise_id}'."

    saved_exercises = [ex for ex in saved_exercises if ex.get("id") != exercise_id]
    write_saved_exercises(saved_filepath, saved_exercises)
    return True, f"Removed '{exercise['name']}' from saved exercises."


# 5-day: one muscle group per day. 3-day: Push/Pull/Legs-style grouping.
WORKOUT_PLAN_TEMPLATES: Dict[int, List[List[str]]] = {
    5: [["Chest"], ["Back"], ["Legs"], ["Shoulders"], ["Arms"]],
    3: [["Chest", "Shoulders"], ["Back", "Arms"], ["Legs"]],
}


def find_exercises_by_muscle_groups(
    muscle_groups: List[str],
    exercises: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """All exercises whose muscle_group is in muscle_groups."""
    return [ex for ex in exercises if ex.get("muscle_group") in muscle_groups]


def select_muscle_group_exercises(
    muscle_group: str,
    saved_exercises: List[Dict[str, Any]],
    exercises: List[Dict[str, Any]],
    min_count: int = 2,
    max_count: int = 4
) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Pick 2-4 exercises for one muscle group, preferring saved ones and
    topping up from the full catalog if under the minimum.
    Returns (exercises, was_topped_up).
    """
    picked = find_exercises_by_muscle_groups([muscle_group], saved_exercises)
    was_topped_up = False

    if len(picked) < min_count:
        picked_ids = {ex["id"] for ex in picked}
        for candidate in find_exercises_by_muscle_groups([muscle_group], exercises):
            if len(picked) >= min_count:
                break
            if candidate["id"] not in picked_ids:
                picked.append(candidate)
                picked_ids.add(candidate["id"])
                was_topped_up = True

    return picked[:max_count], was_topped_up


def build_workout_plan(
    num_days: int,
    exercises: List[Dict[str, Any]],
    saved_filepath: str = DEFAULT_SAVED_EXERCISES_PATH
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Build a workout plan (3 or 5 days) from saved exercises. Each muscle
    group gets 2-4 exercises for the whole week, topped up from the full
    catalog if needed -- picked once per muscle group, then placed on
    whichever day(s) train it.
    Returns (plan, message) where plan is a list of
    {"day": int, "muscle_groups": [...], "exercises": [...]}.
    """
    if num_days not in WORKOUT_PLAN_TEMPLATES:
        return [], f"No template for a {num_days}-day plan; choose 3 or 5."

    saved_exercises = load_saved_exercises(saved_filepath)
    template = WORKOUT_PLAN_TEMPLATES[num_days]

    # Pick each muscle group's 2-4 exercises once for the whole week.
    all_muscle_groups = sorted({mg for day in template for mg in day})
    weekly_picks: Dict[str, List[Dict[str, Any]]] = {}
    topped_up_groups: List[str] = []

    for muscle_group in all_muscle_groups:
        picked, was_topped_up = select_muscle_group_exercises(
            muscle_group, saved_exercises, exercises
        )
        weekly_picks[muscle_group] = picked
        if was_topped_up:
            topped_up_groups.append(muscle_group)

    # Assign each day its muscle groups' exercises from the weekly picks.
    plan: List[Dict[str, Any]] = []
    for day_number, muscle_groups in enumerate(template, start=1):
        day_exercises = [
            ex for muscle_group in muscle_groups for ex in weekly_picks[muscle_group]
        ]
        plan.append({
            "day": day_number,
            "muscle_groups": muscle_groups,
            "exercises": day_exercises,
        })

    if topped_up_groups:
        message = (
            f"Built a {num_days}-day plan (2-4 exercises per muscle group "
            f"per week). Topped up from the catalog for: {', '.join(topped_up_groups)}."
        )
    else:
        message = f"Built a {num_days}-day plan (2-4 exercises per muscle group per week) from your saved exercises."

    return plan, message