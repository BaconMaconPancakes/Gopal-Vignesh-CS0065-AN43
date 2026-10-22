
def get_initial_state(room_name):
    while True:
        state = input(f"Is room {room_name} Dirty or Clean? ").strip().lower()
        if state in {"dirty", "clean"}:
            return state.capitalize()
        print("Please enter only 'dirty' or 'clean'.")


def is_dirty(environment, room_name):
    return environment[room_name] == "Dirty"


def clean_room(environment, room_name):
    if is_dirty(environment, room_name):
        environment[room_name] = "Clean"
        return True
    return False


def main():
    environment = {
        "A": get_initial_state("A"),
        "B": get_initial_state("B"),
    }

    print("\nInitial environment state:", environment)

    for room_name in environment:
        if is_dirty(environment, room_name):
            print(f"Room {room_name} is dirty. Cleaning it...")
            clean_room(environment, room_name)
        else:
            print(f"Room {room_name} is already clean.")

    print("Final environment state:", environment)


if __name__ == "__main__":
    main()
