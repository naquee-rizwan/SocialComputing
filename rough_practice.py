import snap

separator = "---------------------------------------------------------------------------"


class RoughPractice:
    def __init__(self):

        print(separator)

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
        print(int_vector[0])

        print(separator)

        # String vector
        string_vector = snap.TStrV()
        string_vector.append("Naquee")
        string_vector.append("Rizwan")
        # string_vector.append("") - This will throw exception as given in documentation
        for index, string in enumerate(string_vector):
            print(index, string)
        print(len(string_vector))
        print(string_vector[0])

        print(separator)
