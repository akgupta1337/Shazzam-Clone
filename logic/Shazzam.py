import numpy as np
from pydub import AudioSegment
from matplotlib import mlab
from matplotlib import pyplot as plt
from scipy.ndimage import (generate_binary_structure,
                                      iterate_structure,
                                      binary_erosion,)

from scipy.ndimage import maximum_filter
import pandas as pd
import hashlib
from operator import itemgetter
import os

structure = generate_binary_structure(2, 2)
no_of_iteration = 2
neighborhood = iterate_structure(structure, no_of_iteration)


class Shazzam:
    def __init__(self):
        pass
    
    def load_file(self,file_name):
        audio_file = AudioSegment.from_file(file_name)
        audio_data = np.frombuffer(audio_file.raw_data, np.int16)
        channels = []
        for chn in range(audio_file.channels):
            channels.append(audio_data[chn::audio_file.channels])
        return channels

    def find_specgram(self,channel):
        window_size = 2**12
        window_overlap = int(window_size * 0.5)
        dfreq = 44100

        spectrogram = mlab.specgram(
                        channel,
                        NFFT=window_size,
                        Fs=dfreq,
                        window=mlab.window_hanning,
                        noverlap=window_overlap)[0]

        spectrogram = 10 * np.log10(spectrogram, out=np.zeros_like(spectrogram), where=(spectrogram != 0))
        return spectrogram

        
    def get_peaks(self,specgram, no_of_iteration = 10, min_amplitude = 10):
        
        structure = generate_binary_structure(2, 2)
        neighborhood = iterate_structure(structure, no_of_iteration)

        local_max = maximum_filter(specgram, footprint=neighborhood) == specgram

        background = (specgram == 0)
        eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

        # Applying XOR between matrices to get the boolean mask of specgram
        detected_peaks = local_max ^ eroded_background

        # just getting the peaks, their frequency and time
        peaks = specgram[detected_peaks].flatten()
        peak_freqs, peak_times = np.where(detected_peaks)

        # get indices for frequency and time
        peak_indices = np.where(peaks > min_amplitude)

        freqs = peak_freqs[peak_indices]
        times = peak_times[peak_indices]

        return list(zip(freqs, times))


    def get_hashes(self,peaks, peak_combination = 5):
        hash_func = lambda freq1, freq2, offset: hashlib.sha1(
        f"{str(freq1)}|{str(freq2)}|{str(offset)}".encode('utf-8')).hexdigest()[:25]
        peaks.sort(key=itemgetter(1))

        freq_links = []
        for i in range(len(peaks)):
            for j in range(1, peak_combination):
                if (i + j) < len(peaks):

                    freq1 = peaks[i][0]
                    freq2 = peaks[i + j][0]
                    t1 = peaks[i][1]
                    t2 = peaks[i + j][1]
                    t_delta = t2 - t1 
                    freq_links.append((freq1, t1, freq2, t2, t_delta))

        freq_links = pd.DataFrame(freq_links, columns=['freq1', 'time1', 'freq2', 'time2', 'offset'])
        freq_links = freq_links[(freq_links.offset >= 0) & (freq_links.offset < 100)].reset_index(drop=True)
        freq_links['hash'] = freq_links.apply(lambda x: hash_func(x['freq1'], x['freq2'], x['offset']), axis=1)
        return freq_links

    def add_songs(self):
        path = './mp3'
        hash_df = pd.DataFrame(columns=['song_id', 'song_name', 'freq1', 'time1', 'freq2', 'time2', 'offset', 'hash'])
        song_id = 1
        file_exist=True
        try:
            old = pd.read_pickle('database/Database.pkl')
        except FileNotFoundError:
            file_exist = False
        for file_name in os.listdir(path):
            if file_name.endswith(('.wav','.mp3','.m4a', '.ogg')):
                song_name = file_name[:-4]
                if file_exist and song_name in old.song_name.unique():
                    print(f"{song_name} already fingerprinted...")
                    add_to_db = False
                    continue
                else:
                    add_to_db = True
                print("-----------------------------------------------------------")
                print(f'Started reading file: {song_name} ...')
                channels = self.load_file(os.path.join('./mp3', file_name))

                for channel in channels:
                    spectrogram = self.find_specgram(channel)
                    peaks = self.get_peaks(spectrogram)
                    hashes = self.get_hashes(peaks)

                    hashes.loc[:, 'song_id'] = song_id
                    hashes.loc[:, 'song_name'] = song_name
                    hash_df = hash_df._append(hashes)
                print(f'Completed reading file: {song_name} ...')
                print("------------------------------------------------------------\n")
                song_id += 1
        if add_to_db:
            hash_df = hash_df.drop_duplicates(subset=['song_id', 'song_name', 'time1', 'hash'])
            hash_df.reset_index(drop=True, inplace=True)
            hash_df = hash_df[['song_id', 'song_name', 'freq1', 'time1', 'freq2', 'time2', 'offset', 'hash']]
            hash_df.to_pickle('database/Database.pkl')
            return None
        return None


    def match_song(self,song_name):
        hash_df = pd.read_pickle('database/Database.pkl')

        sample_file_name = song_name
        sample_file_path = os.path.join('./test/', sample_file_name)
        song_name = sample_file_name[:-4]

        sample_channels = self.load_file(sample_file_path)

        sample_hash_df = pd.DataFrame(columns=['freq1', 'time1', 'freq2', 'time2', 'offset', 'hash'])
        for channel in sample_channels:
            sample_specgram = self.find_specgram(channel)
            sample_peaks = self.get_peaks(sample_specgram)
            sample_hashes = self.get_hashes(sample_peaks)
            sample_hash_df = sample_hash_df._append(sample_hashes)

        sample_hash_df = sample_hash_df.drop_duplicates(subset=['time1', 'hash'])
        sample_hash_df.reset_index(drop=True, inplace=True)


        matches = []
        for sid in hash_df.song_id.unique():
            temp_hash_df = hash_df[hash_df.song_id == sid]
            merge_df = temp_hash_df.merge(sample_hash_df, on='hash', suffixes=('_o', '_s'))
            merge_df['start_time_diff'] = merge_df.apply(lambda x: x['time1_o'] - x['time1_s'], axis=1)
            
            song_name = temp_hash_df.song_name.iloc[0]
            hashes_matched = temp_hash_df[temp_hash_df.hash.isin(sample_hash_df.hash.unique())].shape[0]
            try:
                match_time = merge_df['start_time_diff'].value_counts().index[0]
                matches_at_match_time = merge_df['start_time_diff'].value_counts().iloc[0]
            except KeyError:
                match_time = 'Error 404'
                matches_at_match_time = 'Error 404'
            
            matches.append((sid, song_name, hashes_matched, match_time, matches_at_match_time))


        best_match = sorted(matches, key=lambda x: x[2] if type(x[2]) == int else 0)[-1]
        print("\n------------------------------------------------------------")
        print('Best Match found in mp3 directory:')
        print(f'Song id: {best_match[0]}')
        print(f'Song name: "{best_match[1]}"')
        print(f'Match time: {best_match[3]}')
        print("------------------------------------------------------------\n")

if __name__ == '__main__':
    engine = Shazzam()
    engine.add_songs()
    engine.match_song('sean_secs.wav')