import snap

line_separator = "--------------------------------------------------"
new_line_separator = "\n" + line_separator + "\n"


class RoughPractice:
    def __init__(self):

        print(new_line_separator)

        # Integer vector
        int_vector = snap.TIntV()
        int_vector.append(1)
        int_vector.append(2)
        int_vector.append(3)
        int_vector.append(4)
        int_vector.append(5)
        int_vector.append(6)
        for index, integer in enumerate(int_vector):
            print(index, integer)
        print(len(int_vector))
        int_vector[0] = -1
        print(int_vector[0])

        print(new_line_separator)

        # String vector
        string_vector = snap.TStrV()
        string_vector.append("Naquee")
        string_vector.append("Rizwan")
        # string_vector.append("") - This will throw exception as given in documentation
        for index, string in enumerate(string_vector):
            print(index, string)
        print(len(string_vector))
        print(string_vector[0])

        print(new_line_separator)

        integer_string_hash = snap.TIntStrH()
        integer_string_hash[5] = "apple"
        integer_string_hash[3] = "orange"
        integer_string_hash[9] = "plum"
        integer_string_hash[6] = "mango"
        integer_string_hash[1] = "banana"
        print(len(integer_string_hash))

        for key in integer_string_hash:
            print(key, integer_string_hash[key])

        print(new_line_separator)

        # Pair types
        pair = snap.TIntStrPr(1, "one")
        print(pair.GetVal1())
        print(pair.GetVal2())

        print(new_line_separator)

