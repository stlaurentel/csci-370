import time
import spidev
# from time import sleep
import numpy as np
from datetime import datetime


def baseADC(channel=0, device=0):
    bus = 0

    spi = spidev.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = int(1e5)

    if (channel == 0): 
        config = [0b01101000, 0]
    else:
        config = [0b01111000, 0]

    myBytes = spi.xfer2(config)
    myData = (myBytes[0] << 8) | myBytes[1]

    spi.close()

    return myData


def readADC(channel=0, device=0):
    myData = baseADC(channel, device)
    return myData * 3.3 / 1023


def readHeartData(sampleDuration=10):
    # adc = readADC(channel=0)
    # initialization
    # curState = 0
    thresh = 2.0  # mid point in the waveform
    peak = 2  # Peak of wave
    trough = 2  # Trough of wave
    # stateChanged = 0
    sampleCounter = 0
    lastBeatTime = 0
    firstBeat = True
    secondBeat = False
    Pulse = False
    IBI = 600
    rate = [0] * 10
    amp = 100

    lastTime = int(time.time() * 1000)
    initialTime = time.time()  # Record start time of sample read
   
    bpmArray = np.empty(0)
    uterineArray = np.empty(0)
    motherBpmArray = np.empty(0)

    current_timestamp = datetime.now()
    
    # Format the timestamp as a string in the desired format
    formatted_timestamp = current_timestamp.strftime("%m/%d/%y %H:%M:%S")

    bpmArray = np.append(bpmArray, formatted_timestamp)
    bpmArray = np.append(bpmArray, "HR2")
    bpmArray = np.append(bpmArray, "external") # In given datasheet, this is either "external" or "INOP"
    uterineArray = np.append(uterineArray, formatted_timestamp)
    uterineArray = np.append(uterineArray, "UA")
    uterineArray = np.append(uterineArray, "TOCO") # In given datasheet, this is either "TOCO" or "No-Trans"
    motherBpmArray = np.append(motherBpmArray, formatted_timestamp)
    motherBpmArray = np.append(motherBpmArray, "MHR")
    # No third column tag associated with mother heart rate

    # Main loop.
    while (time.time() - initialTime) <= sampleDuration:
        # read from the ADC
        Signal = readADC(0)   # TODO: Select the correct ADC channel. I have selected A0 here
        uterineSignal = readADC(1)
        # mhrSignal = readADC(0, 1) TODO: Implement reading and processing extra mother heart rate signal
        curTime = int(time.time() * 1000)

        sampleCounter += curTime - lastTime     # keep track of the time in mS with this variable
        lastTime = curTime
        N = sampleCounter - lastBeatTime     # monitor the time since the last beat to avoid noise
        # print N, Signal, curTime, sampleCounter, lastBeatTime
        
        #  find the peak and trough of the pulse wave
        if Signal < thresh and N > (IBI / 5.0) * 3.0:  # avoid dichrotic noise by waiting 3/5 of last IBI
            if Signal < trough:                        # T is the trough
                trough = Signal                         # keep track of lowest point in pulse wave

        if Signal > thresh and Signal > peak:           # thresh condition helps avoid noise
            peak = Signal                             # P is the peak
            # keep track of highest point in pulse wave

        #  NOW IT'S TIME TO LOOK FOR THE HEART BEAT
        # signal surges up in value every time there is a pulse
        if N > 250:                                   # avoid high frequency noise
            if (Signal > thresh) and (not Pulse) and (N > (IBI/5.0)*3.0):
                Pulse = True                               # set the Pulse flag when we think there is a pulse
                IBI = sampleCounter - lastBeatTime         # measure time between beats in mS
                lastBeatTime = sampleCounter               # keep track of time for next pulse

            if secondBeat:                        # if this is the second beat, if secondBeat == TRUE
                secondBeat = False                  # clear secondBeat flag
                for i in range(0, 10):             # seed the running total to get a realisitic BPM at startup
                    rate[i] = IBI

            if firstBeat:                        # if it's the first time we found a beat, if firstBeat == TRUE
                firstBeat = False                   # clear firstBeat flag
                secondBeat = True                   # set the second beat flag
                continue                              # IBI value is unreliable so discard it

            # keep a running total of the last 10 IBI values
            runningTotal = 0                  # clear the runningTotal variable    

            for i in range(0, 9):                # shift data in the rate array
                rate[i] = rate[i+1]                  # and drop the oldest IBI value
                runningTotal += rate[i]              # add up the 9 oldest IBI values

            rate[9] = IBI                          # add the latest IBI to the rate array
            runningTotal += rate[9]                # add the latest IBI to runningTotal
            runningTotal /= 10                     # average the last 10 IBI values
            BPM = 60000/runningTotal               # how many beats can fit into a minute? that's BPM!
            print(f"BPM {BPM}")
            bpmArray = np.append(bpmArray, str(BPM))    # need to cast to string, since we are also sending timestamp
            motherBpmArray = np.append(motherBpmArray, str(BPM)) # TODO: Read from separate sensor. Currently using the same exact sensor as HR2
            uterineArray = np.append(uterineArray, str(uterineSignal))    # Currently just the voltage read by the ADC from the uterine sensor

        if Signal < thresh and Pulse:   # when the values are going down, the beat is over
            Pulse = False                         # reset the Pulse flag so we can do it again
            amp = peak - trough                           # get amplitude of the pulse wave
            thresh = amp/2 + trough                    # set thresh at 50% of the amplitude
            peak = thresh                            # reset these for next time
            trough = thresh

        if N > 2500:                          # if 2.5 seconds go by without a beat
            thresh = 2.0                          # set thresh default
            peak = 2                               # set P default
            trough = 2                               # set T default
            lastBeatTime = sampleCounter          # bring the lastBeatTime up to date        
            firstBeat = True                      # set these to avoid noise
            secondBeat = False                    # when we get the heartbeat back
            print("no beats found")

        time.sleep(0.25)
    print(f"Fetal bpm: {bpmArray}")
    print(f"Mother bpm: {motherBpmArray}")
    print(f"Uterine activity: {uterineArray}")
    return bpmArray, motherBpmArray, uterineArray


if __name__ == '__main__':
    heartData = readHeartData(30)
    print(heartData)
