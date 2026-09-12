import os

from logic import load_exercises, get_machine_swap

# exercises.json lives in ../data relative to this file
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "exercises.json")


def run_demo() -> None:
    exercises = load_exercises(DATA_PATH)

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


if __name__ == "__main__":
    run_demo()