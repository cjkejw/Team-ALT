# Menu
'''
1. Squats
2. Shoulder Press
3. Bicep Curls
'''

import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))

print("Welcome to the Exercise Tracker AI!")

while True:
    try:
        print("\nSelect an exercise:")
        print("1. Squats")
        print("2. Shoulder Press")
        print("3. Bicep Curls")
        print("4. Exit")

        option = input("Enter option: ").strip()

        if option == "1":
            subprocess.run(["python3", os.path.join(script_dir, "squats_detection.py")])
        elif option == "2":
            subprocess.run(["python3", os.path.join(script_dir, "shoulderpress_detection.py")])
        elif option == "3":
            subprocess.run(["python3", os.path.join(script_dir, "bicepcurls_detection.py")])
        elif option == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please enter 1, 2, 3, or 4.")

    except ValueError:
        print("Invalid input. Please enter a number.")
