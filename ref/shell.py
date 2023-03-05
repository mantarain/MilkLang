import src.main.baltic as baltic

print("Baltic language")
print("v0.1\n\n")

while True:
    text = input("baltic > ")
    if text.strip() == "": continue
    result, error = baltic.run('<stdin>', text)

    if error:
        print(error.as_string())
    
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))