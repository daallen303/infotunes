from music.song import Song
import matplotlib.pyplot as plt 
import numpy as np
from math import pi
import pandas as pd
#import plotly.plotly as py
#import plotly.graph_objs as go

class Graph:

    @staticmethod
    def SongFeatures(song):
        
        labels = ('danceability', 'speechiness', 'acousticness','energy', 'instrumentalness', 'liveness')
        y_pos = np.arange(len(labels))
        confidence = [song.danceability, song.speechiness, song.acousticness, song.energy, song.instrumentalness, song.liveness]

        plt.bar(y_pos, confidence, align='center', alpha=.1, color='blue',linewidth=1)
        plt.xticks(y_pos, labels)
        plt.ylabel('Confidence')
        plt.title(song.name +' Song Features')
        plt.ylim(0,1)
        plt.show()
    
    #need to add Mode as well so it shows if the song is minor or major
    #also need to make it more optimal
    @staticmethod
    def Key(songs):
        C=Db=D=Eb=E=F=Gb=G=Ab=A=Bb=B=0
        for song in songs:
            if song.key == 0:
                C += 1
            if song.key == 1:
                Db += 1
            if song.key == 2:
                D += 1
            if song.key == 3:
                Eb += 1
            if song.key == 4:
                E += 1
            if song.key == 5:
                F += 1
            if song.key == 6:
                Gb += 1
            if song.key == 7:
                G+= 1
            if song.key == 8:
                Ab += 1
            if song.key == 9:
                A += 1
            if song.key == 10:
                Bb += 1
            if song.key == 11:
                B += 1
        labels = ['C','Db','D','Eb','E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        sizes = [C,Db,D,Eb,E,F,Gb,G,Ab,A,Bb, B]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','blue', 'orange', 'pink','yellow', 'purple', 'red', 'green', 'grey']

        delete_indexes = []
        for i in range(len(sizes)):
            if sizes[i] == 0:
                delete_indexes.append(i)
        count = 0
        for i in delete_indexes:
                del sizes[i-count]
                del labels[i-count]
                del colors[i-count]
                count+=1
        print(len(sizes))
        explode = (0,0.1,0,0,0,0)
        plt.title("Song Keys for the Lumineers Cleopatra")    
        plt.pie(sizes, labels=labels, explode=explode, colors=colors, autopct='%1.1f%%')
        
        plt.axis('equal')
        plt.show()

    # Fix to more accurately represent a song
    @staticmethod
    def RadarPlot(song):
       # Set data
       df = pd.DataFrame({
           'Tempo': [song.tempo],
           'popularity' : [song.popularity],
           'valence' : [song.valence*100],
           'loudness' : [song.loudness*-10],
           'duration' : [song.duration_ms/10000]

           })
        
       # number of variable
       categories=list(df)[:]
       N = len(categories)
       print(categories)
       
       # We are going to plot the first line of the data frame.
       # But we need to repeat the first value to close the circular graph:
       values=df.loc[0].values.flatten().tolist()
       values += values[:1]
       print(values)
         
       # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
       angles = [n / float(N) * 2 * pi for n in range(N)]
       angles += angles[:1]
       print(angles)   
       # Initialise the spider plot
       ax = plt.subplot(111, polar=True)
           
       # Draw one axe per variable + add labels labels yet
       plt.xticks(angles[:-1], categories, color='grey', size=8)
            
       # Draw ylabels
       ax.set_rlabel_position(0)
       plt.yticks([25,50,75,100], ["25", "50","75","100"], color="grey", size=7)
       plt.ylim(0,100)
             
       # Plot data
       ax.plot(angles, values, linewidth=1, linestyle='solid')
              
       # Fill area
       ax.fill(angles, values, 'b', alpha=0.1)
       plt.title(song.name)
       plt.show()

    @staticmethod
    def AlbumPopularityOverTime(artist):
        
        x = []
        y = []
        z = []

        for album in artist.albums:
            # year
            year = int(album.release_date[:4],10)
            x.append(year)
            
            y.append(album.song_count)
            # album popularity
            z.append(album.popularity)


        plt.axis([min(x)-2,max(x)+2,0, max(y)+2])
        plt.ylabel('Number of Songs')
        plt.xlabel('Year released')
        #use the scatter function
        plt.scatter(x, y, s=z*100)
        plt.show()
