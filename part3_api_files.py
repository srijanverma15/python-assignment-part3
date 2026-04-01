# ---------------- PART 3 ----------------

import requests
from datetime import datetime

# ---------------- TASK 1 ----------------

print("\n--- FILE WRITE ---")

notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes."
]

# write
with open("python_notes.txt", "w", encoding="utf-8") as file:
    for line in notes:
        file.write(line + "\n")

print("File written successfully.")

# append
with open("python_notes.txt", "a", encoding="utf-8") as file:
    file.write("Topic 6: Functions help reuse code.\n")
    file.write("Topic 7: APIs allow communication between systems.\n")

print("Lines appended.")

# read
print("\n--- FILE READ ---")

with open("python_notes.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    print(f"{i+1}. {line.strip()}")

print("Total lines:", len(lines))

keyword = input("Enter keyword to search: ").lower()

found = False
for line in lines:
    if keyword in line.lower():
        print(line.strip())
        found = True

if not found:
    print("No matching lines found.")


# ---------------- TASK 2 ----------------

print("\n--- API CALLS ---")

def fetch_products():
    try:
        response = requests.get("https://dummyjson.com/products?limit=20", timeout=5)
        data = response.json()["products"]

        print("\nID | Title | Category | Price | Rating")
        for p in data:
            print(p["id"], "|", p["title"], "|", p["category"], "|", p["price"], "|", p["rating"])

        return data

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except Exception as e:
        print("Error:", e)

products = fetch_products()

# filter + sort
if products:
    filtered = [p for p in products if p["rating"] >= 4.5]
    filtered.sort(key=lambda x: x["price"], reverse=True)

    print("\nFiltered Products:")
    for p in filtered:
        print(p["title"], "-", p["price"])

# laptops
try:
    res = requests.get("https://dummyjson.com/products/category/laptops", timeout=5)
    laptops = res.json()["products"]

    print("\nLaptops:")
    for l in laptops:
        print(l["title"], "-", l["price"])

except Exception as e:
    print("Error:", e)

# POST
try:
    res = requests.post(
        "https://dummyjson.com/products/add",
        json={
            "title": "My Custom Product",
            "price": 999,
            "category": "electronics",
            "description": "Created via API"
        },
        timeout=5
    )

    print("\nPOST Response:")
    print(res.json())

except Exception as e:
    print("Error:", e)


# ---------------- TASK 3 ----------------

print("\n--- EXCEPTION HANDLING ---")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


def read_file_safe(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")

print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))


# input validation loop

while True:
    user_input = input("Enter product ID (1-100) or 'quit': ")

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Invalid input")
        continue

    pid = int(user_input)

    if pid < 1 or pid > 100:
        print("Out of range")
        continue

    try:
        res = requests.get(f"https://dummyjson.com/products/{pid}", timeout=5)

        if res.status_code == 404:
            print("Product not found.")
        else:
            data = res.json()
            print(data["title"], "-", data["price"])

    except Exception as e:
        print("Error:", e)


# ---------------- TASK 4 ----------------

print("\n--- LOGGING ---")

def log_error(message):
    with open("error_log.txt", "a") as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {message}\n")

# trigger connection error
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except Exception as e:
    log_error(f"ERROR in fetch_products: {type(e).__name__}")

# trigger 404
res = requests.get("https://dummyjson.com/products/999", timeout=5)
if res.status_code != 200:
    log_error("ERROR in lookup_product: HTTPError — 404 Not Found")

# read log
print("\nError Log Content:")
with open("error_log.txt", "r") as f:
    print(f.read())
