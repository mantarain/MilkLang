import main

debug = 'run("tests/struct.mlk")'

while True:
	text = input('milk > ')
	if text.strip() == "": continue
	if text == "run": text = debug
	result, error = main.run('<terminal>', text)

	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))
