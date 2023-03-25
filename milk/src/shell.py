import main

while True:
    text = input('milk > ')
    if text.strip() == "":
        continue
    result, error = main.run('<console>', text)

    if error:
        print(error.as_string())
    elif result:
        print(result)
