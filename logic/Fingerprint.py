import numpy as np
from pydub import AudioSegment
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
from hashlib import sha1
from operator import itemgetter
from pydub import AudioSegment
import hashlib
import time
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (binary_erosion,
                                      generate_binary_structure,
                                      iterate_structure)



class Fingerprint:

    def __init__(self):
        self.DEFAULT_WINDOW_SIZE = 4096
        self.DEFAULT_FS = 44100
        self.DEFAULT_OVERLAP_RATIO = 0.5
        self.DEFAULT_FAN_VALUE = 5 
        self.DEFAULT_AMP_MIN = 10
        self.PEAK_NEIGHBORHOOD_SIZE = 10
        self.wsize = self.DEFAULT_WINDOW_SIZE
        self.wratio = self.DEFAULT_OVERLAP_RATIO
        self.fan_value = self.DEFAULT_FAN_VALUE
        self.amp_min  = self.DEFAULT_AMP_MIN
        self.CONNECTIVITY_MASK = 2
        self.PEAK_SORT = True
        self.MIN_HASH_TIME_DELTA = 0
        self.MAX_HASH_TIME_DELTA = 200
        self.FINGERPRINT_REDUCTION = 20
        
    def shazam_similarity(self, original_hashes,test_hash,songn):
        matches = 0
        for hash in test_hash:
            if hash in original_hashes:
                matches+=1
        return matches

    def shazzam(self,audio_path):
        start = time.time()
        self.audio_hash = self.audio_process(audio_path)
        fig =''
        lookup = {}
        with open ('database/database.txt','r') as file:
            while True:
                st = file.readline()
                if not st:
                    break
                if st == "\n":
                    score = self.shazam_similarity(eval(fig),self.audio_hash,song_name)
                    lookup[song_name] = score
                    fig = ''
                if st.startswith('song'):
                    song_name = st.split(":")[1]
                    lookup[song_name] = 0
                else:
                    fig += st
        
        Key_max = max(lookup, key = lookup.get)
        print("\nTotal time taken:",time.time() - start)  
        return Key_max
        
    def add_song(self,audio_path):
        song_hash = self.audio_process(audio_path)
        if ("/") in audio_path:
            audio_path = audio_path.split("/")[-1]
        with open ("database.txt","a") as file:
            file.write(f"song:{audio_path}")
            file.write("\n")
            file.write(str(song_hash))
            file.write("\n\n")
        print("Succesfully added:",audio_path)
        
        
    def audio_process(self,audio_path):
        self.audio_path = audio_path
        sound = AudioSegment.from_wav(self.audio_path)
        sound = sound.set_channels(1)
        if ("/") in self.audio_path:
            self.audio_path = audio_path.split("/")[-1]
        sound.export(f"converted_mono/mono_{self.audio_path}", format="wav")
        
        self.audiofile = AudioSegment.from_file(f"converted_mono/mono_{self.audio_path}")
        self.channel_samples = np.frombuffer(self.audiofile.raw_data, np.int16)
        audio_hash = set()

        self.hashes= (self.fingerprint(self.channel_samples))
        audio_hash |= set(self.hashes)
        

        return audio_hash
        
    def fingerprint(self,channel_samples) :
        Fs = self.DEFAULT_FS
        fan_value = self.DEFAULT_FAN_VALUE
        amp_min = self.DEFAULT_AMP_MIN
        arr2D = mlab.specgram(
            channel_samples,
            NFFT=self.wsize,
            Fs=Fs,
            window=mlab.window_hanning,
            noverlap=int(self.wsize * self.wratio))[0]

        arr2D = 10 * np.log10(arr2D, out=np.zeros_like(arr2D), where=(arr2D != 0))

        local_maxima = self.get_2D_peaks(arr2D)

        return self.generate_hashes(local_maxima)
    
    
    def get_2D_peaks(self,arr2D):
        amp_min = self.DEFAULT_AMP_MIN
       
        struct = generate_binary_structure(2, self.CONNECTIVITY_MASK)

        neighborhood = iterate_structure(struct, self.PEAK_NEIGHBORHOOD_SIZE)

        local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D

        background = (arr2D == 0)
        eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

        detected_peaks = local_max != eroded_background

        amps = arr2D[detected_peaks]
        freqs, times = np.where(detected_peaks)

        amps = amps.flatten()

        filter_idxs = np.where(amps > amp_min)

        freqs_filter = freqs[filter_idxs]
        times_filter = times[filter_idxs]

        
        return list(zip(freqs_filter, times_filter))
    
    def generate_hashes(self,peaks):
        fan_value: int = self.DEFAULT_FAN_VALUE

        idx_freq = 0
        idx_time = 1

        if self.PEAK_SORT:
            peaks.sort(key=itemgetter(1))

        hashes = []
        for i in range(len(peaks)):
            for j in range(1, fan_value):
                if (i + j) < len(peaks):

                    freq1 = peaks[i][idx_freq]
                    freq2 = peaks[i + j][idx_freq]
                    t1 = peaks[i][idx_time]
                    t2 = peaks[i + j][idx_time]
                    t_delta = t2 - t1
                    if self.MIN_HASH_TIME_DELTA <= t_delta <= self.MAX_HASH_TIME_DELTA:
                        h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8'))
                        hashes.append((h.hexdigest()[0:self.FINGERPRINT_REDUCTION]))

        return hashes