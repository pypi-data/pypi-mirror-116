class Tomato:
    def __init__(self, color):
        self.color = color
    def __str__(self):
        return "Tomato is of " + str(self.color) + " color."

# t1 = Tomato("red")
# print(t1)