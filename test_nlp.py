from nlp import extract_train_number

print(extract_train_number("Tell me about train 04601"))

print(extract_train_number("Show details of train 12345"))

print(extract_train_number("Train number is 22691"))

print(extract_train_number("Hello"))