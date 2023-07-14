# Example 2 - classes.py
class Patient:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def get_age_difference(
        self, other: "Patient"
    ) -> int:
        return abs(self.age - other.age)


def main():
    p1 = Patient("Rob", 100)
    p2 = Patient("Chris", 75)

    age_difference = p1.get_age_difference(p2)
    print(age_difference)


if __name__ == "__main__":
    main()
