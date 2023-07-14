import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patheffects as path_effects
from ..io.output import Output


class Fulfillment_Visualizer():

    def __init__(self):

        self.PATH = Output.DATA_FOLDER_PATH + "visualization/"

        self.total_courses = 0
        self.total_templates = 0

        self.height = 0.5
        self.width = 1
        self.counter = 0

    def visualize(self, fulfillments:dict, title='Untitled'):
        # Define the course names and their coordinates
        boxes = list()

        i = 0
        templates = list(fulfillments.keys())
        templates.sort()
        templates.reverse()
        length = len(fulfillments)
        for template in templates:
            fulfillment = fulfillments.get(template)
        #for template, fulfillment in fulfillments.items():
            key = template.name
            if 'dummy' in key:
                length -= 1
                continue
            courses = [course.name for course in fulfillment.get_fulfillment_set()]
            courses.sort()
            j = 3
            boxes.append((key,(i, 4)))
            for course in courses:
                boxes.append((course,(i, j)))
                j -= self.height
            i += self.width
        # Create a figure and axis
        fig, ax = plt.subplots()

        # Set the axis limits
        
        ax.set_xlim(-1, length)
        ax.set_ylim(-1, 5)

        # Iterate over the courses and create a rounded rectangle with text for each one in both subplots
        for (course, coordinates) in boxes:
            x, y = coordinates
            if course.isdigit():
                color_pick = int(int(course) * 8 + 50)
            else:
                color_pick = 1
            color = self.rgb2hex(color_pick, int(color_pick * 0.7), int(color_pick * 1.1))
            fill_color = self.rgb2hex(int(color_pick * 0.3 + 80), int(color_pick * 0.7 * 0.3 + 80), int(color_pick * 1.1 * 0.3 + 80))
            rect = Rectangle((x, y), self.width * 0.9, self.height * 0.9, fill=True, linewidth=3, edgecolor=color, color=fill_color)
            print(color)
            ax.add_patch(rect)
            text = ax.text(x + self.width/2, y + self.height/2, course, ha="center", va="center", fontsize=8, color='white')
            text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()])

        self.counter += 1
        self.print_plots(ax, title, self.counter)


    def rgb2hex(self, r,g,b):
        r = '{:02x}'.format(r)
        g = '{:02x}'.format(g)
        b = '{:02x}'.format(b)
        return f'#{r}{g}{b}'


    def print_plots(self, ax, name='untitled', counter=1):
        plt.show()
        # Save each subplot as a separate image file
        ax.set_title(f"{name}")
        ax.set_xlabel("X Label")
        ax.set_ylabel("Y Label")
        plt.savefig(f"{self.PATH}subplot_{counter}_{name}.png", dpi=300)
        plt.clf()