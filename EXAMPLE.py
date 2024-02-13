from logic.Shazzam import Shazzam

engine = Shazzam()


'''
this will add songs present in 'mp3' folder to database
run it only once to load hashes in database, after that comment it out 
and only run match_song()
'''
engine.add_songs()

'''
just write song name, which is present in 'test' folder 
no need to mention relative path
'''
engine.match_song('sean_secs.wav')
