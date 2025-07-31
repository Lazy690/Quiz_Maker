def choose_from_list(options, prompt="Choose an option:"):
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(input(prompt + " "))
            return options[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice. Try again.")

# Example usage
fruits = ["apple", "banana", "cherry"]
selected = choose_from_list(fruits)
print("You selected:", selected)
