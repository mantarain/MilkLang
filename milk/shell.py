from src import main

print("Milk 1")
print("v0.1")  # TODO: extract info from info.txt and display instead of here

while True:
    text = input("Milk > ")
<<<<<<< HEAD
    if text.strip() == "": continue
    if text == "exit":
        break
=======
    if text.strip() == "":
        continue
>>>>>>> origin/master
    result, error = main.run("<console>", text)

    if error:
        print(error.as_string())

    elif result:
        print(result)
