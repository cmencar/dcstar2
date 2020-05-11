import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget, QPushButton, QLineEdit, \
    QFileDialog, QHBoxLayout, QLabel, QMessageBox
from PyQt5 import QtGui
from matplotlib import colors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.title = 'DCViewer - DoubleClusteringStar Bidimensional Sequences Viewer - v0.1b'
        self.width = 1024
        self.height = 680

        self.elements = dict()
        self.plot = None
        self.filename = ""
        self.current_node = -1

        self.initUI()


    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        page_layout = QVBoxLayout()
        navbar_layout = QHBoxLayout()
        central_layout = QHBoxLayout()
        lateral_layout = QVBoxLayout()
        flow_buttons_layout = QHBoxLayout()
        jump_to_layout = QHBoxLayout()
        sequence_buttons_layout = QVBoxLayout()
        costs_label_layout = QVBoxLayout()

        load_button = QPushButton('Load data', self)
        load_button.setToolTip('Load a DoubleClustering log file')
        load_button.clicked.connect(self.open_log_file)

        navbar_layout.addWidget(load_button)
        navbar_layout.setAlignment(Qt.AlignLeft)

        previous_sequence_button = QPushButton('Previous', self)
        previous_sequence_button.setToolTip('Show the previous cuts configuration')
        previous_sequence_button.clicked.connect(self.plot_previous_sequence)
        previous_sequence_button.setFont((QtGui.QFont("arial", 12)))
        next_sequence_button = QPushButton('Next', self)
        next_sequence_button.setToolTip('Show the next cuts configuration')
        next_sequence_button.clicked.connect(self.plot_next_sequence)
        next_sequence_button.setFont((QtGui.QFont("arial", 12)))
        flow_buttons_layout.addWidget(previous_sequence_button)
        flow_buttons_layout.addWidget(next_sequence_button)
        flow_buttons_layout.setAlignment(Qt.AlignVCenter)

        jump_to_button = QPushButton('Jump to...', self)
        jump_to_button.setToolTip('Jump to a specific cuts configuration')
        jump_to_button.clicked.connect(self.plot_s_d_sequence_jumped)
        jump_to_button.setFont((QtGui.QFont("arial", 12)))
        self.jump_to_lineedit = QLineEdit('1', self)
        jump_to_end_button = QPushButton('Result', self)
        jump_to_end_button.setFont((QtGui.QFont("arial", 12)))
        jump_to_end_button.setToolTip('Jump to the final cuts configuration')
        jump_to_end_button.clicked.connect(self.plot_last_s_d_sequence_jumped)
        jump_to_layout.addWidget(jump_to_button)
        jump_to_layout.addWidget(self.jump_to_lineedit)
        jump_to_layout.addWidget(jump_to_end_button)
        jump_to_layout.setAlignment(Qt.AlignVCenter)

        costs_header_label = QLabel("COSTS")
        costs_header_label.setFont(QtGui.QFont("arial", 15, 200))
        self.first_priority_cost_label = QLabel("g+h's cost: \t")
        self.first_priority_cost_label.setFont(QtGui.QFont("arial", 12))
        self.second_priority_cost_label = QLabel("heuristic's cost: \t")
        self.second_priority_cost_label.setFont(QtGui.QFont("arial", 12))
        self.third_priority_cost_label = QLabel("GG similarity's cost: \t")
        self.third_priority_cost_label.setFont(QtGui.QFont("arial", 12))
        self.fourth_priority_cost_label = QLabel("cut distance's cost: \t")
        self.fourth_priority_cost_label.setFont(QtGui.QFont("arial", 12))
        self.fifth_priority_cost_label = QLabel("dimensions' cost: \t")
        self.fifth_priority_cost_label.setFont(QtGui.QFont("arial", 12))
        costs_label_layout.addWidget(costs_header_label)
        costs_label_layout.addWidget(self.first_priority_cost_label)
        costs_label_layout.addWidget(self.second_priority_cost_label)
        costs_label_layout.addWidget(self.third_priority_cost_label)
        costs_label_layout.addWidget(self.fourth_priority_cost_label)
        costs_label_layout.addWidget(self.fifth_priority_cost_label)
        costs_label_layout.setAlignment(Qt.AlignCenter)

        t_d_sequence_button = QPushButton("T_d sequences")
        t_d_sequence_button.setToolTip('Show the T_d cuts sequences')
        t_d_sequence_button.clicked.connect(self.plot_t_d_sequence)
        t_d_sequence_button.setFont(QtGui.QFont("arial", 12))
        gg_sequence_button = QPushButton("GG sequences")
        gg_sequence_button.setToolTip('Show the genetic guide individual sequences')
        gg_sequence_button.clicked.connect(self.plot_gg_sequence)
        gg_sequence_button.setFont(QtGui.QFont("arial", 12))
        s_d_sequence_button = QPushButton("S_d first sequences")
        s_d_sequence_button.setToolTip('Show the S_d cuts sequences')
        s_d_sequence_button.clicked.connect(self.plot_s_d_sequence)
        s_d_sequence_button.setFont(QtGui.QFont("arial", 12))

        sequence_buttons_layout.addWidget(t_d_sequence_button)
        sequence_buttons_layout.addWidget(gg_sequence_button)
        sequence_buttons_layout.addWidget(s_d_sequence_button)

        lateral_layout.addLayout(sequence_buttons_layout)
        lateral_layout.addLayout(costs_label_layout)
        lateral_layout.addLayout(flow_buttons_layout)
        lateral_layout.addLayout(jump_to_layout)

        self.plot = PlotCanvas(self, width=10, height=6)
        central_layout.addWidget(self.plot)
        central_layout.addLayout(lateral_layout)

        page_layout.addLayout(navbar_layout)
        page_layout.addLayout(central_layout)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

        self.show()


    def open_log_file(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open log file", "",
                                                  "Double Clustering Log Files (*.dcl)",
                                                  options=options)
        if filename:
            self.filename = filename
            self.elements = self.__parse_log_file(filename)

            if len(self.elements.get("Prototypes")[0][0]) == 2:
                self.plot.define_colors(self.elements.get("Prototypes"))
                self.plot_t_d_sequence()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText("Error opening log file")
                msg.setInformativeText("The log file you want to open is poorly formatted or is associated "
                                       "with a non-two-dimensional dataset")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()


    def __parse_log_file(self, filename):

        if ".dcl" in filename:
            file = open(filename, "r")
            file_content = file.readlines()

            elements = dict()
            for line in file_content:
                if "#" in line:
                    key = str(line)
                    key = key.replace("# ", "").replace("\n", "").replace(" ", "_")
                    elements.__setitem__(key, [])

            element_key = ""
            for line in file_content:

                if "#" in line:
                    element_key = line.replace("# ", "").replace("\n", "").replace(" ", "_")

                elif line != "\n":

                    formatted_line = line.replace("array([", "[").replace("[[", "[") \
                        .replace("])", "]").replace("]]","]").replace("\n", "") \
                        .replace("0. ", "0").replace("1. ", "1")

                    dictionary_objects = []
                    if element_key == "Prototypes":
                        parsed_string = formatted_line.split(";")
                        coordinates = [ float(coord) for coord in parsed_string[0].strip('][').split(",")]
                        dictionary_objects = [coordinates, parsed_string[1]]

                    elif element_key == "T_d_sequences":
                        sequences = formatted_line.replace("], [", ";").strip('][').split(";")
                        sequences = [[float(cut) for cut in sequence.split(",")] for sequence in sequences]
                        dictionary_objects = sequences

                    elif element_key == "S_d_sequences":
                        parsed_string = formatted_line.split(";")
                        sequences = parsed_string[0].replace("], [", ";").strip('][').split(";")
                        sequences = [[True if "True" in cut else False for cut in sequence.split(",")]
                                     for sequence in sequences]
                        costs = parsed_string[1].replace(")", "").replace("(","").split(",")
                        costs = [float(cost) for cost in costs]
                        dictionary_objects = [sequences, costs]

                    elif element_key == "Genetic_sequences":
                        sequences = formatted_line.replace("], [", ";").strip('][').split(";")
                        sequences = [[True if "True" in cut else False for cut in sequence.split(",")]
                                     for sequence in sequences]
                        dictionary_objects = sequences

                    elif element_key == "m_d" or element_key == "M_d":
                        boundaries = [float(m) for m in formatted_line.strip('][').split(",")]
                        dictionary_objects = boundaries

                    elements.get(element_key).append(dictionary_objects)

            file.close()

            return elements

        return None


    def plot_next_sequence(self):

        if len(self.elements.get("S_d_sequences")) > self.current_node + 1:
            self.current_node += 1
            self.plot.plot_S_d_sequence(self.elements, self.filename, self.current_node)
            self.show_costs()


    def plot_previous_sequence(self):

        if self.current_node > 0:
            self.current_node -= 1
            self.plot.plot_S_d_sequence(self.elements, self.filename, self.current_node)
            self.show_costs()


    def plot_t_d_sequence(self):

        self.reset_costs()
        self.current_node = 0
        self.plot.plot_T_d_sequence(self.elements, self.filename)


    def plot_gg_sequence(self):

        self.reset_costs()
        self.current_node = 0
        self.plot.plot_gg_sequence(self.elements, self.filename)


    def plot_s_d_sequence(self):

        self.plot.plot_S_d_sequence(self.elements, self.filename, self.current_node)
        self.show_costs()


    def plot_s_d_sequence_jumped(self):

        if 0 <= int(self.jump_to_lineedit.text()) < len(self.elements.get("S_d_sequences")):
            self.current_node = int(self.jump_to_lineedit.text())
            self.plot.plot_S_d_sequence(self.elements, self.filename, self.current_node)
            self.show_costs()


    def plot_last_s_d_sequence_jumped(self):

        self.current_node = len(self.elements.get("S_d_sequences")) - 1
        self.plot.plot_S_d_sequence(self.elements, self.filename, self.current_node)
        self.show_costs()


    def show_costs(self):

        costs = self.elements.get("S_d_sequences")[self.current_node][1]
        if len(costs) >= 1:
            self.first_priority_cost_label.setText("g+h's cost: \t\t" + str(costs[0]))
        if len(costs) >= 2:
            self.second_priority_cost_label.setText("heuristic's cost: \t\t" + str(costs[1]))
        if len(costs) >= 3:
            self.third_priority_cost_label.setText("GG similarity's cost: \t" + str(costs[2]))
        if len(costs) >= 4:
            self.fourth_priority_cost_label.setText("cut distance's cost: \t" + str(costs[3]))
        if len(costs) >= 5:
            self.fifth_priority_cost_label.setText("dimensions' cost: \t" + str(costs[4]))


    def reset_costs(self):

        self.first_priority_cost_label.setText("g+h's cost: \t")
        self.second_priority_cost_label.setText("heuristic's cost: \t")
        self.third_priority_cost_label.setText("GG similarity's cost: \t")
        self.fourth_priority_cost_label.setText("cut distance's cost: \t")
        self.fifth_priority_cost_label.setText("dimensions' cost: \t")



class PlotCanvas(FigureCanvas):

    def __init__(self, parent = None, width = 5, height = 4, dpi = 100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.subplot = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.setParent(parent)

        self.__starting_plot()

        self.colored_class = dict()


    def define_colors(self, prototypes):

        classes = set([prototype[1] for prototype in prototypes])
        colors_list = list(colors._colors_full_map.values())
        random.shuffle(colors_list)
        self.colored_class = {label: color for label, color in zip(classes, colors_list)}


    def __starting_plot(self):

        ax = self.figure.add_subplot(111)
        ax.set_title('No log loaded')
        self.draw()


    def plot_T_d_sequence(self, elements, title):

        if len(elements) == 0:
            return

        title = title.split("/")[-1] + "  -  T_d sequences"
        sequence_to_plot = elements.get("T_d_sequences")[0]
        points = elements.get("Prototypes")
        m_d = elements.get("m_d")[0]
        M_d = elements.get("M_d")[0]

        self.subplot.clear()

        for cut in sequence_to_plot[0]:
            self.subplot.plot([cut, cut], [m_d[0], M_d[0]], linestyle='--', color='gray')
        for cut in sequence_to_plot[1]:
            self.subplot.plot([m_d[1], M_d[1]], [cut, cut], linestyle='--', color='gray')
        for point in points:
            self.subplot.scatter(point[0][0], point[0][1], color=self.colored_class.get(point[1]))

        self.subplot.set_title(title)

        self.draw()


    def plot_gg_sequence(self, elements, title):

        if len(elements) == 0:
            return

        title = title.split("/")[-1] + "  -  Genetic individual sequences"
        sequence_to_plot = elements.get("Genetic_sequences")[0]
        T_d_sequence = elements.get("T_d_sequences")[0]
        points = elements.get("Prototypes")
        m_d = elements.get("m_d")[0]
        M_d = elements.get("M_d")[0]

        self.subplot.clear()

        for binary_cut, cut in zip(sequence_to_plot[0], T_d_sequence[0]):
            if binary_cut is True:
                self.subplot.plot([cut, cut], [m_d[0], M_d[0]], linestyle='-', color='red')
            else:
                self.subplot.plot([cut, cut], [m_d[0], M_d[0]], linestyle='--', color='lightgray')

        for binary_cut, cut in zip(sequence_to_plot[1], T_d_sequence[1]):
            if binary_cut is True:
                self.subplot.plot([m_d[1], M_d[1]], [cut, cut], linestyle='-', color='red')
            else:
                self.subplot.plot([m_d[1], M_d[1]], [cut, cut], linestyle='--', color='lightgray')

        for point in points:
            self.subplot.scatter(point[0][0], point[0][1], color=self.colored_class.get(point[1]))

        self.subplot.set_title(title)

        self.draw()


    def plot_S_d_sequence(self, elements, title, node):

        if len(elements) == 0:
            return

        title = title.split("/")[-1] + "  -  S_d sequences, Node " + str(node)
        sequence_to_plot = elements.get("S_d_sequences")[node][0]
        T_d_sequence = elements.get("T_d_sequences")[0]
        points = elements.get("Prototypes")
        m_d = elements.get("m_d")[0]
        M_d = elements.get("M_d")[0]

        self.subplot.clear()

        for binary_cut, cut in zip(sequence_to_plot[0], T_d_sequence[0]):
            if binary_cut is True:
                self.subplot.plot([cut, cut], [m_d[0], M_d[0]], linestyle='-', color='red')
            else:
                self.subplot.plot([cut, cut], [m_d[0], M_d[0]], linestyle='--', color='lightgray')

        for binary_cut, cut in zip(sequence_to_plot[1], T_d_sequence[1]):
            if binary_cut is True:
                self.subplot.plot([m_d[1], M_d[1]], [cut, cut], linestyle='-', color='red')
            else:
                self.subplot.plot([m_d[1], M_d[1]], [cut, cut], linestyle='--', color='lightgray')

        for point in points:
            self.subplot.scatter(point[0][0], point[0][1], color=self.colored_class.get(point[1]))

        self.subplot.set_title(title)

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

