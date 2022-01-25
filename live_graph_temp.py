import datetime as dt
import time

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.animation as anim

from serial import Serial
from serial.serialutil import PortNotOpenError
from serial.tools.list_ports import comports

# can change these
VALS_WINDOW = 60  # seconds before moving graph along
USE_COM_PORT = None  # can be autodetected if not known e.g. 'COM3'
OUTPUT_FILENAME = 'all_temp_vals.csv'  # output all temp data after closing
STYLESHEET = r'C:\Users\lnick\Documents\Personal\Programming\Python\Resources\proplot_style_dark.mplstyle'  # larger screen size

# set by microcontroller program
T_OS = 28  # maximum safe temperature
T_HIST = 26  # temp must fall below this after overheating (hysteresis) to turn off warning light
_TIME_STEP = 1  # value sent once per second

# hardware properties
_BAUD_RATE = 9600  # STM32 Nucleo baud rate (always 9600)
_PORT_DESC_KEYWORD = 'STMicroelectronics'  # search COM port descriptions for this keyword

if STYLESHEET is not None:
    plt.style.use(STYLESHEET)


def read_last_temp(frame: int, current_time: dt.datetime):

    data = str(s.readline())

    while 'Measurement' not in data:
        time.sleep(_TIME_STEP / 1000)
        data = str(s.readline())
    else:
        temp = float(data.split('Temperature = ')[-1].split(r'\r')[0])
        print(f'T = {temp} \t\t t = {current_time} \t\t frame = {frame}')
        return temp


def animate(frame: int, times_raw: list[float], temps_raw: list[float]):

    current_time = dt.datetime.now()
    last_temp = round(read_last_temp(frame, current_time), 3)

    times_raw.append(current_time)
    temps_raw.append(last_temp)

    times = [timestamp.strftime('%H:%M:%S') for timestamp in times_raw[-1 * VALS_WINDOW :]]
    temps = temps_raw[-1 * VALS_WINDOW :]

    plt.cla()

    plt.title('Temperature Sensor')
    plt.xlabel('Time / hr min sec ')
    plt.ylabel('Temperature / $ ^{\circ} C $ ')
    plt.xticks(rotation=30)
    plt.gca().xaxis.set_major_locator(MaxNLocator(15))

    plt.plot(times, [T_OS] * len(times),
        label=r'$ T_{OS} = $' + f'{T_OS} ' + r'$ ^{\circ} C $', color='red', linestyle='dashed')
    plt.plot(times, [T_HIST] * len(times),
        label=r'$ T_{hist} = $' + f'{T_HIST} ' + r'$ ^{\circ} C $', color='green', linestyle='dashed')

    plt.plot(times, temps, label=f'Last temp = {last_temp}' + r' $ ^{\circ} C $')
    plt.legend(loc='upper left')


if __name__ == '__main__':

    # init
    times_raw, temps_raw = [], []
    fig = plt.figure()

    # find COM port of STM32 Nucleo
    if USE_COM_PORT is None:
        port_nos = [(portno, desc) for portno, desc, _ in comports() if _PORT_DESC_KEYWORD in desc]
        port_nos.sort(key=lambda p: p[0])
        if port_nos != []:
            port, desc = port_nos[-1]
        else:
            raise NameError('Could not find a COM port with an STMicroelectronics device. '
                'Try specifying the port number in USE_COM_PORT.')
    else:
        port, desc = USE_COM_PORT, None

    # read data continuously from serial and make animated live plot
    with Serial(port, _BAUD_RATE, timeout=1) as s:
        if not s.is_open:
            raise PortNotOpenError
        print(f'Connected to {port}: {desc}')
        ani = anim.FuncAnimation(fig, animate, fargs=(times_raw, temps_raw))
        plt.show()

    # export all data as .csv when graph window closed
    with open(OUTPUT_FILENAME, 'a') as f:
        f.truncate(0)
        f.write('Number,Time / hh:mm:ss,Temperature / C\n')
        for frame, (timestamp, temp) in enumerate(zip(times_raw, temps_raw)):
            f.write(f'{frame},{timestamp},{temp}\n')
        print(f'Output data written to {OUTPUT_FILENAME}')
