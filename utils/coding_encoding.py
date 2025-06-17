import heapq

from models.city import City
import json


class Node:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.right = None
        self.left = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def huffman_code(city: City, max_flow: int, min_cost: int):
    data = {
        "fields": [item.to_dict() for item in city.fields],
        "breweries": [item.to_dict() for item in city.breweries],
        "inns": [item.to_dict() for item in city.inns],
        "roads": [item.to_dict() for item in city.roads],
        "shire_sectors": [item.to_dict() for item in city.sectors],
        "max_flow": max_flow,
        "min_cost": min_cost
    }

    frequency_data = {}
    json_text = json.dumps(data)

    for char in json_text:
        if char in frequency_data:
            frequency_data[char] += 1
        else:
            frequency_data[char] = 1

    '''
    for char in frequency_data:
        print(f"'{char}': {frequency_data[char]}")
    '''

    heap = []
    for char, frequency in frequency_data.items():
        heapq.heappush(heap, Node(char, frequency))

    while len(heap) > 1:
        left: Node = heapq.heappop(heap)
        right: Node = heapq.heappop(heap)

        new_node = Node(None, left.frequency + right.frequency)
        new_node.left = left
        new_node.right = right

        heapq.heappush(heap, new_node)

    tree_root: Node = heap[0]

    codes = {}

    def generate_codes(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
            return
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(tree_root, "")

    encoded = ""
    for char in json_text:
        encoded += codes[char]

    print(f"\nZakodowany tekst: {encoded}")
    print(f"Dlugosc zakodowanego: {len(encoded)} bitów")

    with open("./output/encoded_output.txt", "w") as file:
        file.write(encoded)

    with open("./output/huffman_codes.txt", "w") as file:
        file.write(json.dumps(codes))

    return encoded, codes


def decode_huffman(encoded: str, codes: dict) -> str:
    reversed_codes = {code: char for char, code in codes.items()}

    decoded_text = ""
    current_code = ""

    for bit in encoded:
        current_code += bit
        if current_code in reversed_codes:
            decoded_text += reversed_codes[current_code]
            current_code = ""

    return decoded_text

