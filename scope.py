import pyvisa
from matplotlib import pyplot as plt


def main():
    rm = pyvisa.ResourceManager('@py')
    scope = rm.open_resource('TCPIP::192.168.88.2::INSTR')
    scope.timeout = 5000

    print(scope.query('*IDN?')[:-1])

    print('Collecting data...')

    scope.write('SCDP')
    res = scope.read_bytes(1)
    with open('test.bmp', 'wb') as f:
        f.write(res)
        f.close()

    vdiv = scope.query('C1:VDIV?')
    vdiv = float(vdiv[8:-2])

    ofst = scope.query('C1:OFST?')
    ofst = float(ofst[8:-2])

    tdiv = scope.query('TDIV?')
    tdiv = float(tdiv[5:-2])

    sr = scope.query('SARA?')
    sr = 1 / float(sr[5:-5])

    scope.write('C1:WF? DAT2')
    res = scope.read_bytes(1)
    data = list(res)[22:-2]
    voltages = []
    times = []

    print('Processing data...')
    count = 0
    for b in data:
        if b > 127:
            b -= 255
        v = b * (vdiv / 25) - ofst
        voltages.append(v)
        t = -(tdiv * 14 / 2) + count*sr
        times.append(t)
        count += 1

    print('Rendering...')
    plt.plot(times, voltages)
    plt.ylabel('scope')
    plt.show()

if __name__ == '__main__':
    main()
