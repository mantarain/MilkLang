from src import main

print("Milk 1")
print("v0.1")  # TODO: extract info from info.txt and display instead of here

while True:
    text = input("milk > ")
    if text.strip() == "":
        continue
    result, error = main.run('<terminal>', text)

    if error:
        print(error.as_string())

    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))
