import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound
import os.path as path
import time
def play(file_path):
        
    #file_path = "test.mp3"
    root,ext = path.splitext(file_path)
    demuxer = muxer.Demuxer(ext[1:].lower())
    decoder = None
    output = None

    file = open(file_path,'rb')
    data = ' '
    while data:
        data = file.read(90000)
        if len(data):
            frames = demuxer.parse(data)
            for frame in frames:
                if decoder == None:
                    decoder = acodec.Decoder(demuxer.streams[0])

                audio_frame = decoder.decode(frame[1])
                if audio_frame and audio_frame.data:
                    if output==None:
                        output = sound.Output(audio_frame.sample_rate,audio_frame.channels,sound.AFMT_S16_LE)
                    
                    #while self.stop:
                        #time.sleep(1)

                    output.play(audio_frame.data)
            
            while output.isPlaying(): 
                time.sleep( 0.05 )
