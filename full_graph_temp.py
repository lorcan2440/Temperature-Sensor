import csv
import dateutil as dtu
from matplotlib import pyplot as plt

from live_graph_temp import OUTPUT_FILENAME


with open(OUTPUT_FILENAME, 'r') as f:

    data = [(dtu.parser.parse(line[1]), float(line[2])) for line in csv.reader(f) if line[0] != 'Number']

    plt.title('Temperature Sensor')
    plt.xlabel('Time / hr min sec ')
    plt.ylabel('Temperature / $ ^{\circ} C $ ')
    plt.xticks(rotation=30)
    plt.plot(*zip(*data))
    plt.show()
