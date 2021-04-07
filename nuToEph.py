# nu to STK Ephemeris converter

# Made by Satsir
# linkedin.com/in/satsir

# Converts all your nu files from the specified directory NU_FILES_PATH to STK Ephemeris file.
# Source of nu files:
# ftp://ftp.kiam1.rssi.ru/pub/gps/spectr-rg/nu/

import datetime
from pathlib import Path

NU_FILES_PATH = 'D:/nu'
STK_VERSION = '9.0'
AUTHOR = 'Author'

def get_time(mylines):
    text1 = str(float(mylines[2]))[:8]
    text2 = str(float(mylines[3]))
    t1 = datetime.datetime.strptime(text1 + text2, "%Y%m%d%H%M%S.%f") - datetime.timedelta(hours=3)
    return t1

def get_eph(mylines):
    str1 = ''                            
    for i in range(4, 10):
        if i < 7:
            str1 += str(float(mylines[i])*1000) +' '
        else:
            str1 += str(float(mylines[i])) +' '
    return str1
    
run_once = 1
ephemeris = []
pathlist = Path(NU_FILES_PATH).rglob('*.nu')
for path in pathlist:
    path_in_str = str(path)
    if path.is_file():
        current_file = open(path, 'r')
        mylines = []
        for myline in current_file:
            mylines.append(myline)
        if run_once == 1:
            epoch = get_time(mylines)
        eph_time = get_time(mylines)
        s1 = str(get_time(mylines)) + ' ' + get_eph(mylines)
        ephemeris.append(str((get_time(mylines) - epoch).total_seconds()) + ' ' + get_eph(mylines))
        current_file.close()
    run_once = 0

epoch_UTCG = datetime.datetime.strftime(epoch, "%d %b %Y %H:%M:%S.%f UTCG")
ephemeris_lines = str('\n'.join(ephemeris))

stk_e_text = f'''stk.v.{STK_VERSION}

# WrittenBy    {AUTHOR}

BEGIN Ephemeris

NumberOfEphemerisPoints {len(ephemeris)}

ScenarioEpoch            {epoch_UTCG}

# Epoch in JDate format: TODO
# Epoch in YYDDD format:   TODO


InterpolationMethod     Lagrange

InterpolationSamplesM1      1

CentralBody             Earth

CoordinateSystem        J2000 

# Time of first point: TODO

DistanceUnit Kilometers

EphemerisTimePosVel

{ephemeris_lines}

END Ephemeris'''

f = open(f'{NU_FILES_PATH}/Ephemeris.e', 'w')
f.write(stk_e_text)
f.close()
