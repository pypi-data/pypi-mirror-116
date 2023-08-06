import re


def parse_prettytable(s):
    """ Give a prettytable string, return a dict with key as the field name, and value as a list of items
    """
    # intialize
    s = s.strip()
    num_of_field = 0

    lines = s.split("\n")
    header_line = lines[1]
    header_array = header_line.split("|")
    header_array = list(filter(None, header_array))
    header_array = list(map(str.strip, header_array))

    num_of_field = len(header_array)

    pairs = re.split("\+-*\+-*\+\n?", s)[2:-1]
    final_arrays = [[] for i in range(num_of_field)]
    for p in pairs:
        arrays = [[] for i in range(num_of_field)]
        for l in p.split('\n'):
            pair = l.strip().split('|')
            pair = list(filter(None, pair))
            if len(pair) > 1:
                for j in range(len(pair)):
                    if pair[j] == "":
                        continue
                    arrays[j].append(pair[j].strip())
        for i in range(num_of_field):
            final_arrays[i].append(" ".join(arrays[i]))

    final_dict_array = {}
    for i in range(num_of_field):
        final_dict_array[header_array[i]] = final_arrays[i]
    return final_dict_array
