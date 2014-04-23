
from array import array
from struct import pack

import tempfile
import time
import pyaudio
import sys
import wave
import os


class Microphone:

    def listen(self):
        print "Recording..."

        recording_rate = self.rate()

        # execute recording
        #(_, recording_wav_filename) = tempfile.mkstemp('.wav')
        #print tempfile.mkstemp('.wav')
        if not os.path.exists("wav/"):
            os.makedirs("wav/")
        recording_wav_filename = "wav/"+str(time.strftime("%Y-%m-%d_%X",time.localtime())).replace(':','_')+".wav"
        #tempfile.mkstemp('.wav')r"/wav/"+
        #f=open(recording_wav_filename)
        try:
            f=file(recording_wav_filename,'w')
            f.write('')
            f.close
        except:pass
        self.do_wav_recording(recording_wav_filename, recording_rate)

        self.recordedWavFilename = recording_wav_filename

        return self.recordedWavFilename

    def filename(self):
        return self.recordedWavFilename

    def rate(self):
        return 16000#44100

    def housekeeping(self):
        os.remove(self.recordedWavFilename)

    def is_silent(self, sound_data, threshold):
        return max(sound_data) < threshold

    def add_silence(self, sound_data, seconds, recording_rate):
        r = array('h', [0 for i in xrange(int(seconds*recording_rate))])
        r.extend(sound_data)
        r.extend([0 for i in xrange(int(seconds*recording_rate))])
        return r

    def do_wav_recording(self, recording_filename, recording_rate):
        THRESHOLD = 2000            # Set threshold of volume to consider as silence
        NUM_SILENT = 10             # Set amt of silence to accept before ending recording
        CHUNK = 1024    
        FORMAT = pyaudio.paInt16
        CHANNELS = 1#2

        if sys.platform == 'darwin':
            CHANNELS = 1

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=recording_rate,
                        input=True,
                        frames_per_buffer=CHUNK)

        num_silent = 0              
        speech_started = False       
        r = array('h')

        print("recording start"),time.time();timepoint = time.time()

        while 1:
            sound_data = array('h', stream.read(CHUNK))
            if sys.byteorder == 'big':
                sound_data.byteswap()
            #r.extend(sound_data)

            silent = self.is_silent(sound_data, THRESHOLD)

            if not silent:r.extend(sound_data)
            if silent and speech_started:
                num_silent += 1
            elif not silent and not speech_started:
                speech_started = True

            if speech_started and num_silent > NUM_SILENT:
                break

            if len(r)>34000:break
            
        print("recording end"),time.time(),time.time() - timepoint

        print recording_filename,
        stream.stop_stream()
        stream.close()
        p.terminate()
        print len(r)
        data = self.add_silence(r, 0.5, recording_rate)
        data = self.add_silence(r, 0, recording_rate)
        print len(data)
        data = pack('<' + ('h'*len(data)), *data)
        
        wf = wave.open(recording_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(recording_rate)
        wf.writeframes(b''.join(data))
        wf.close()





