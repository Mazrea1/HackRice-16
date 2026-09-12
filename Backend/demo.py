import os

from logic import (
    load_exercises,
    get_machine_swap,
    add_saved_exercise,
    delete_saved_exercise,
)

# Data files live in ../data relative to this file
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
EXERCISES_PATH = os.path.join(DATA_DIR, "exercises.json")
SAVED_PATH = os.path.join(DATA_DIR, "saved_exercises.json")


def demo_machine_swap(exercises) -> None:
    print("=== Machine swap ===\n")
    demo_ids = [
        "ex_chest_01",   # machine with a direct swap_id
        "ex_back_09",    # another machine with a direct swap_id
        "ex_chest_02",   # not a machine at all
        "ex_not_real",   # id that doesn't exist
    ]

    for ex_id in demo_ids:
        swap, message = get_machine_swap(ex_id, exercises)
        print(f"Input id: {ex_id}")
        print(f"  Message: {message}")
        print(f"  Swap result: {swap['name'] if swap else None}")
        print()


def demo_saved_exercises(exercises) -> None:
    print("=== Saved exercises (persisted to saved_exercises.json) ===\n")

    # Add two exercises to the saved list
    for ex_id in ["ex_chest_02", "ex_legs_04"]:
        exercise, message = add_saved_exercise(ex_id, exercises, SAVED_PATH)
        print(f"Add '{ex_id}': {message}")

    # Try adding the same one again -- should say "already saved"
    exercise, message = add_saved_exercise("ex_chest_02", exercises, SAVED_PATH)
    print(f"Add 'ex_chest_02' again: {message}")

    # Remove one
    success, message = delete_saved_exercise("ex_chest_02", SAVED_PATH)
    print(f"Delete 'ex_chest_02': {message}")

    # Try removing something that isn't saved
    success, message = delete_saved_exercise("ex_not_saved", SAVED_PATH)
    print(f"Delete 'ex_not_saved': {message}")
    print()


def run_demo() -> None:
    exercises = load_exercises(EXERCISES_PATH)
    demo_machine_swap(exercises)
    demo_saved_exercises(exercises)


if __name__ == "__main__":
    run_demo()