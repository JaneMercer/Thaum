class Aspect:

    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.image = []
        self.color_label = []
        self.dependencies = []
        self.value = 1

    def add_image(self, image):
        self.image = image

    def add_color_label(self, color_label):
        self.color_label = color_label

    def add_dependencies(self, dependencies):
        self.dependencies = dependencies

    def add_value(self, value):
        self.value = value

    def get_index(self):
        return self.index

    def get_image(self):
        return self.image

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_color_label(self):
        return self.color_label

    def get_dependencies(self):
        return self.dependencies
