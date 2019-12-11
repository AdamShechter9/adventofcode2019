

class Day08(object):
    def __init__(self, read_file_fn):
        self.raw_data = read_file_fn('day8').split('\n')[0]
        self.data = [int(x) for x in self.raw_data]

    def run_solution1(self):
        """
        :return:
        """
        space_image_format = SpaceImageFormat(6, 25, self.data)
        return space_image_format.find_layer_fewest_0s()

    def run_solution2(self):
        """
        :return:
        """
        space_image_format = SpaceImageFormat(6, 25, self.data)
        space_image_format.print_image()
        return


class SpaceImageFormat(object):
    def __init__(self, height, width, data):
        self.height = height
        self.width = width
        self.data = data
        self.image = self.generate_image(self.height, self.width, self.data)
        self.decoded_image = self.decode_image()

    @staticmethod
    def generate_image(height, width, image_data):
        image = []
        i = 0
        while i < len(image_data):
            new_layer = []
            for h in range(height):
                current_row = image_data[i:i + width]
                new_layer.append(current_row)
                i += width
            image.append(new_layer)
        return image

    def find_layer_fewest_0s(self):
        zero_count = -1
        layer_index = -1
        for i, layer in enumerate(self.image):
            current_count = 0
            for row in layer:
                current_count += row.count(0)
            if current_count < zero_count or zero_count == -1:
                zero_count = current_count
                layer_index = i
        print(f'Layer {layer_index} has the fewest 0s.  Count is {zero_count}')
        ones_count = 0
        twos_count = 0
        for row in self.image[layer_index]:
            ones_count += row.count(1)
            twos_count += row.count(2)
        return ones_count * twos_count

    def decode_image(self):
        decoded_image = []
        for i, row in enumerate(self.image[0]):
            decoded_row = []
            for j, col in enumerate(row):
                if col < 2:
                    decoded_row.append(col)
                else:
                    for k in range(1, len(self.image)):
                        if self.image[k][i][j] < 2:
                            decoded_row.append(self.image[k][i][j])
                            break
            decoded_image.append(decoded_row)
        return decoded_image

    def print_image(self):
        for row in self.decoded_image:
            str_row = []
            for c in row:
                if c == 1:
                    str_row.append('X')
                else:
                    str_row.append(' ')
            print(' '.join(str_row))
        return
