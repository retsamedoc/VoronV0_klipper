#!/usr/bin/env python3
from datetime import timedelta, datetime
from os import error
from time import sleep
from requests import get, post
import re

######### META DATA #################
# For data collection organizational purposes
USER_ID = ''            # e.g. Discord handle
PRINTER_MODEL = ''      # e.g. 'voron_v2_350'
MEASURE_TYPE = ''       # e.g. 'nozzle_pin', 'microswitch_probe', etc.
NOTES = ''              # anything note-worthy about this particular run, no "=" characters
#####################################

######### CONFIGURATION #############
BASE_URL = 'http://127.0.0.1'       # printer URL (e.g. http://192.168.1.15)
                                    # leave default if running locally
BED_TEMPERATURE = 105               # bed temperature for measurements
HE_TEMPERATURE = 100                # extruder temperature for measurements
MEASURE_INTERVAL = 1.               # measurement interval (minutes)
N_SAMPLES = 3                       # number of repeated measures
HOT_DURATION = 3                    # time after bed temp reached to continue
                                    # measuring, in hours
COOL_DURATION = 0                   # hours to continue measuring after heaters
                                    # are disabled
MEASURE_GCODE = 'G28 Z'             # G-code called on repeated measurements, single line/macro only
# chamber thermistor config name. Change to match your own, or "" if none
# will also work with temperature_fan configs
CHAMBER_CONFIG = "temperature_sensor chamber"
#####################################


MCU_Z_POS_RE = re.compile(r'(?P<mcu_z>(?<=stepper_z:)-*[0-9.]+)')
DATA_FILENAME = "expansion_quant_%s_%s.csv" % (USER_ID,
    datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
last_measurement = datetime.now() - timedelta(minutes=MEASURE_INTERVAL)
start_time = datetime.now() + timedelta(days=1)
index = 0
BASE_URL = BASE_URL.strip('/') # remove any errant "/" from the address


def gather_metadata():
    resp = get(BASE_URL + '/printer/objects/query?configfile').json()
    config = resp['result']['status']['configfile']['settings']
    
    # Gather Z axis information
    config_z = config['stepper_z']
    if 'rotation_distance' in config_z.keys():
        rot_dist = config_z['rotation_distance']
        steps_per = config_z['full_steps_per_rotation']
        micro = config_z['microsteps']
        if 'gear_ratio' in config_z.keys():
            gear_ratio_conf = config_z['gear_ratio'].split(':')
            gear_ratio = float(gear_ratio_conf[0])/float(gear_ratio_conf[1])
        else:
            gear_ratio = 1.
        step_distance = (rot_dist / (micro * steps_per))/gear_ratio
    elif 'step_distance' in config_z.keys():
        step_distance = config_z['step_distance']
    else:
        step_distance = "NA"
    max_z = config_z['position_max']
    if 'second_homing_speed' in config_z.keys():
        homing_speed = config_z['second_homing_speed']
    else:
        homing_speed = config_z['homing_speed']

    # Frame expansion configuration
    config_frame_comp = config['frame_expansion_compensation']

    # Organize
    meta = {
        'user': {
            'id': USER_ID,
            'printer': PRINTER_MODEL,
            'measure_type': MEASURE_TYPE,
            'measure_gcode': '"%s"' % MEASURE_GCODE,
            'notes': NOTES,
            'timestamp': datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S")
        },
        'script':{
            'data_structure': 3,
            'hot_duration': HOT_DURATION,
            'cool_duration': COOL_DURATION
        },
        'z_axis': {
            'step_dist' : step_distance,
            'max_z' : max_z,
            'homing_speed': homing_speed
        },
        'frame_expansion_compensation' : config_frame_comp,
    }
    return meta

def write_metadata(meta):
    with open(DATA_FILENAME, 'w') as dataout:
        dataout.write('### METADATA ###\n')
        for section in meta.keys():
            print(section)
            dataout.write("## %s ##\n" % section.upper())
            for item in meta[section]:
                dataout.write('# %s=%s\n' % (item, meta[section][item]))
        dataout.write('### METADATA END ###\n')

def send_gcode(cmd='', retries=1):
    url = BASE_URL + "/printer/gcode/script?script=%s" % cmd
    resp = post(url)
    success = None
    for i in range(retries):
        try: 
            success = 'ok' in resp.json()['result']
        except KeyError:
            print("G-code command '%s', failed. Retry %i/%i" % (cmd, i+1, retries))
        else:
            return True
    return False

def set_bedtemp(t=0):
    temp_set = False
    cmd = 'SET_HEATER_TEMPERATURE HEATER=heater_bed TARGET=%.1f' % t
    temp_set = send_gcode(cmd, retries=3)
    if not temp_set:
        raise RuntimeError("Bed temp could not be set.")


def set_hetemp(t=0):
    temp_set = False
    cmd = 'SET_HEATER_TEMPERATURE HEATER=extruder TARGET=%.1f' % t
    temp_set = send_gcode(cmd, retries=3)
    if not temp_set:
        raise RuntimeError("HE temp could not be set.")

def get_cached_gcode(n=1):
    url = BASE_URL + "/server/gcode_store?count=%i" % n
    resp = get(url).json()['result']['gcode_store']
    return resp

def query_mcu_z_pos():
    send_gcode(cmd='get_position')
    gcode_cache = get_cached_gcode(n=1)
    for msg in gcode_cache:
        pos_matches = list(MCU_Z_POS_RE.finditer(msg['message']))
        if len(pos_matches) > 1:
            return int(pos_matches[0].group())
    return None

def query_frame_temp():
    url = BASE_URL + '/printer/objects/query?frame_expansion_compensation'
    resp = get(url).json()['result']
    temp = float(resp['status']['frame_expansion_compensation']['temperature'])
    return temp

def query_temp_sensors():
    url = BASE_URL + '/printer/objects/query?extruder&heater_bed&%s' % CHAMBER_CONFIG
    resp = get(url).json()['result']['status']
    try:
      chamber_current = resp[CHAMBER_CONFIG]['temperature']
    except KeyError:
      chamber_current = -180.
    bed_current = resp['heater_bed']['temperature']
    bed_target = resp['heater_bed']['target']
    he_current = resp['extruder']['temperature']
    he_target = resp['extruder']['target']
    return {
        'chamber_temp': chamber_current,
        'bed_temp': bed_current,
        'bed_target': bed_target,
        'he_temp': he_current,
        'he_target': he_target}

def collect_datapoint(index):
    if not send_gcode(MEASURE_GCODE):
        set_bedtemp()
        set_hetemp()
        err = 'MEASURE_GCODE (%s) failed. Stopping.' % MEASURE_GCODE
        raise RuntimeError(err)
    stamp = datetime.now()
    pos = query_mcu_z_pos()
    t_frame = query_frame_temp()
    t_sensors = query_temp_sensors()
    datapoint =  {
        index : {
            'timestamp': stamp,
            'mcu_z' : pos, 
            'frame_t' : t_frame,
            'chamber_t' : t_sensors['chamber_temp'],
            'bed_t' : t_sensors['bed_temp'],
            'bed_target' : t_sensors['bed_target'],
            'he_t' : t_sensors['he_temp'],
            'he_target' : t_sensors['he_target']}
    }
    return datapoint

def log_datapoint(datapoint:list):
    _index = list(datapoint[0].keys())[0]
    with open(DATA_FILENAME, 'a') as datafile:
        for sample in datapoint:
            datafile.write('\n%s,%s,%s,%s,%s,%s,%s,%s,%s'
            % (
            _index,
            sample[_index]['timestamp'].strftime("%Y/%m/%d-%H:%M:%S"),
            sample[_index]['mcu_z'],
            sample[_index]['frame_t'],
            sample[_index]['chamber_t'],
            sample[_index]['bed_t'],
            sample[_index]['bed_target'],
            sample[_index]['he_t'],
            sample[_index]['he_target']
            ))

def wait_for_bedtemp():
    global start_time
    at_temp = False
    print('Heating started')
    while(1):
        temps = query_temp_sensors()
        if temps['bed_temp'] >= BED_TEMPERATURE-0.5:
            at_temp = True
            break
        measure()
    start_time = datetime.now()
    print('\nBed temp reached')

def measure():
    global last_measurement, index, start_time
    now = datetime.now()
    if (now - last_measurement) >= timedelta(minutes=MEASURE_INTERVAL):
        last_measurement = now
        data = []
        print('\r', ' '*50,end='\r')
        print('Measuring (#%i)...' % index, end='',flush=True)
        for n in range(N_SAMPLES):
            print('%i/%i...' % (n+1, N_SAMPLES), end='', flush=True)
            data.append(collect_datapoint(index))
        index += 1
        log_datapoint(data)
        print('DONE', " "*20)
    else:
        t_minus = ((last_measurement + timedelta(minutes=MEASURE_INTERVAL))-now).seconds
        if now >= start_time:
            total_remaining = (start_time + timedelta(hours=HOT_DURATION+COOL_DURATION)-now).seconds/60
            print('%imin remaining. ' % total_remaining, end='')
        print('Next measurement in %02is' % t_minus, end='\r', flush=True)

def main():
    global last_measurement, start_time
    write_metadata(gather_metadata())
    print("Starting!\nHoming...", end='')
    # Home all
    if send_gcode('G28'):
        print("DONE")
    else:
        raise RuntimeError("Failed to home. Aborted.")

    send_gcode('SET_FRAME_COMP enable=0')

    with open(DATA_FILENAME, 'a') as datafile:
        header = 'sample,time,mcu_pos_z,frame_t,chamber_t,bed_t,bed_target,he_t,he_target'
        datafile.write(header)

    set_bedtemp(BED_TEMPERATURE)
    set_hetemp(HE_TEMPERATURE)

    wait_for_bedtemp()

    while(1):
        now = datetime.now()
        if (now - start_time) >= timedelta(hours=HOT_DURATION):
            break
        measure()
        sleep(0.2)
    print('Hot measurements complete!')
    set_bedtemp()

    start_time = datetime.now()
    while(1):
        now = datetime.now()
        if (now - start_time) >= timedelta(hours=HOT_DURATION+COOL_DURATION):
            break
        measure()
        sleep(0.2)

    set_hetemp()
    send_gcode('SET_FRAME_COMP enable=1')
    print('Cooldown measurements complete!')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        set_bedtemp()
        set_hetemp()
        send_gcode('SET_FRAME_COMP enable=1')
        print("\nAborted by user!")
