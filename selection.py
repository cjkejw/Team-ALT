import os

def main():
    print("Welcome to the Exercise Tracker AI!")

    scripts = {
        "1": "bicepcurls_detection.py",
        "2": "shoulderpress_detection.py",
        "3": "squats_detection.py"
    }

    while True:
        print("\nSelect an exercise:")
        print("1. Bicep Curls Detection")
        print("2. Shoulder Press Detection")
        print("3. Squats Detection")
        print("q. Quit")

        choice = input("Enter the number of your choice: ").strip()

        if choice == "q":
            print("Exiting Exercise Tracker AI. Goodbye!")
            break
        elif choice in scripts:
            os.system(f"python {scripts[choice]}")
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
