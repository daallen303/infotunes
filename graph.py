from music.song import Song
import matplotlib.pyplot as plt 
import numpy as np
from math import pi
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import datetime

py.tools.set_credentials_file(username='daallen303', api_key='2ziGQf8CeGbtEZQdisEI') 

class Graph:

    @staticmethod
    def AudioFeaturesBarGraph(song):
        
        labels = ('danceability', 'speechiness', 'acousticness','energy', 'instrumentalness', 'liveness')
        y_pos = np.arange(len(labels))
        confidence = [song.danceability, song.speechiness, song.acousticness, song.energy, song.instrumentalness, song.liveness]

        plt.bar(y_pos, confidence, align='center', alpha=.1, color='blue',linewidth=1)
        plt.xticks(y_pos, labels)
        plt.ylabel('Confidence')
        plt.title(song.name +' Song Features')
        plt.ylim(0,1)
        plt.show()
    

    # Fix to more accurately represent a song
    @staticmethod
    def AudioFeaturesRadarPlot(song):
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
       
       # We are going to plot the first line of the data frame.
       # But we need to repeat the first value to close the circular graph:
       values=df.loc[0].values.flatten().tolist()
       values += values[:1]
         
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
        
        dates = []
        counts = []
        pops = []
        album_info = []
        album_type = []
        album_color = []
        
        for album in artist.albums:
            
            dates.append(album.release_date)
            counts.append(album.song_count)
            
            pops.append(album.popularity)
            album_info.append("<b><i>"+album.name+"</i></b><br><b>Recorded in:</b> "+
                    datetime.datetime.strftime(album.release_date, "%m-%d-%Y")+"<br><b>Popularity</b>: "+str(album.popularity))
            if album.popularity < 10 and album.popularity >= 0:
                album_color.append('#D3B073')
            elif album.popularity < 30 and album.popularity >= 10:
                album_color.append('#A6A27A')
            elif album.popularity < 50 and album.popularity >= 30:
                album_color.append('#3E4D56')
            elif album.popularity < 70 and album.popularity >= 50:
                album_color.append('#99BE0B')
            else:
                album_color.append('red')
        
        trace0 = go.Scatter(
                x = dates,
                y = pops,
                mode='markers',
                marker=dict(
                    size=counts,
                    color=album_color
                    ),
                text=album_info,
                )
        layout = go.Layout(
                title=dict(text = artist.name+" albums over time",
                            font = dict( size = 18,
                                color = 'white')),
                hovermode='closest',
                xaxis=dict(
                    title = "Release Date",
                    gridcolor = 'rgb(255,255,255)',
                    color='rgb(255,255,255)',
                    tickformat = "%m-%d-%Y",
                    zerolinewidth = 1,
                    ticklen=0,
                    gridwidth = 2
                ),
                yaxis=dict(
                    title='Popularity',
                    range = [0,100],
                    gridcolor='rgb(255,255,255)',
                    color='rgb(255,255,255)',
                    zerolinewidth=1,
                    ticklen=0,
                    gridwidth=2,
                ),
                paper_bgcolor='rgb(40,40,40)',
                plot_bgcolor='rgb(40,40,40)'
            )
        data = [trace0]
        fig = go.Figure(data=data, layout=layout) 
        py.plotly.plot(fig, filename=artist.name+" albums over time")

    @staticmethod
    def GraphPlaylist(songs, name):
        
        years = []
        nums = []
        pops = []
        song_info = []

        for song in songs:
            # year
            year = int(song.release_date[:4],10)
            print(year)
            years.append(year)
            
            nums.append(song.track_number)
            # song popularity
            pops.append(song.popularity)
            song_info.append("<b><i>"+song.artist_name+":</i></b> "+song.name+"<br><b>Recorded in:</b> "+
                    song.release_date+"<br><b>Popularity</b>: "+str(song.popularity))
        
        #plt.axis([min(x)-2,max(x)+2,0, max(y)+2])
        trace0 = go.Scatter(
                x = years,
                y = nums,
                mode='markers',
                marker=dict(
                    size=pops,
                    ),
                text=song_info,
                )
        layout = go.Layout(
                title=dict( text = name+" songs",
                            font=dict( size = 18,
                            color = 'rgb(255,255,255)')),
                hovermode='closest',
                xaxis=dict(
                    title = "Release Date",
                    gridcolor = 'rgb(255,255,255)',
                    color='rgb(255,255,255)',
                    zerolinewidth = 1,
                    ticklen = 0,
                    gridwidth = 2
                ),
                yaxis=dict(
                    title='Track number in album',
                    gridcolor='rgb(255,255,255)',
                    color='rgb(255,255,255)',
                    zerolinewidth=1,
                    ticklen=0,
                    gridwidth=2,
                ),
                paper_bgcolor='rgb(60,60,60)',
                plot_bgcolor='rgb(60,60,60)'
            )
        data = [trace0]
        fig = go.Figure(data=data, layout=layout)
        py.plotly.plot(fig, filename=name)

    @staticmethod
    def TopArtists(lr_artists, mr_artists, sr_artists):

        trace0 = go.Table(
            name = "dallen-us Top artists",
            header=dict(values=['<b>Spot</b>', '<b>Long range</b>', '<b>Medium Range</b>', '<b>Short Range</b>'],
                        fill_color="black",
                        line_color="black",
                        align = "center",
                        height = 30,
                        font=dict(color='rgb(255,255,255)',
                            size = 18)),
            
            cells=dict(values=[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                        lr_artists, mr_artists, sr_artists],
                        fill_color="rgb(60,60,60)",
                        line_color="black",
                        align = ["right","left", "left", "left"],
                        font=dict(color='rgb(255,255,255)',
                            size=18
                            ),
                        height=30),
            columnwidth=[100,400,400,400]
            )

        layout = go.Layout(
            title =dict(text = "dallen-us Top artists",
                font=dict(size = 18,
                    color = 'rgb(255,255,255)')),
                paper_bgcolor='rgb(60,60,60)'
                )
        
        data = [trace0]
        fig = go.Figure(data=data, layout=layout)
        py.plotly.plot(fig, filename="dallen-us Top Artists")


    @staticmethod
    def TopSongs(lr_songs, mr_songs, sr_songs):
        
        trace0 = go.Table(
            name = "dallen-us Top Songs",
            header=dict(values=['<b>Spot</b>', '<b>Long range</b>', '<b>Medium Range</b>', '<b>Short Range</b>'],
                        fill_color="black",
                        line_color="black",
                        align = "center",
                        height = 30,
                        font=dict(color='rgb(255,255,255)',
                            size = 18)),
            
            cells=dict(values=[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
                        lr_artists, mr_artists, sr_artists],
                        fill_color="rgb(60,60,60)",
                        line_color="black",
                        align = ["right","left", "left", "left"],
                        font=dict(color='rgb(255,255,255)',
                            size=18
                            ),
                        height=30),
            columnwidth=[100,400,400,400]
            )

        layout = go.Layout(
            title =dict(text = "dallen-us Top Songs",
                font=dict(size = 18,
                    color = 'rgb(255,255,255)')),
                paper_bgcolor='rgb(60,60,60)'
                )
        
        data = [trace0]
        fig = go.Figure(data=data, layout=layout)
        py.plotly.plot(fig, filename="dallen-us Top Songs")

    #need to add Mode as well so it shows if the song is minor or major
    #also need to make it more optimal
    @staticmethod
    def AlbumKeys(songs, album_name, artist_name):
        key_info=["<b>Song names:</b>"]*12
        C=Db=D=Eb=E=F=Gb=G=Ab=A=Bb=B=0
        for song in songs:
            if song.key == 0:
                C += 1
                key_info[0]+= song.name+'<br>'
            if song.key == 1:
                Db += 1
                key_info[1]+= song.name+'<br>'
            if song.key == 2:
                D += 1
                key_info[2]+= song.name+'<br>'
            if song.key == 3:
                Eb += 1
                key_info[3]+= song.name+'<br>'
            if song.key == 4:
                E += 1
                key_info[4]+= song.name+'<br>'
            if song.key == 5:
                F += 1
                key_info[5]+= song.name+'<br>'
            if song.key == 6:
                Gb += 1
                key_info[6]+= song.name+'<br>'
            if song.key == 7:
                G+= 1
                key_info[7]+= song.name+'<br>'
            if song.key == 8:
                Ab += 1
                key_info[8]+= song.name+'<br>'
            if song.key == 9:
                A += 1
                key_info[9]+= song.name+'<br>'
            if song.key == 10:
                Bb += 1
                key_info[10]+= song.name+'<br>'
            if song.key == 11:
                B += 1
                key_info[11]+= song.name+'<br>'
        labels = ['C','Db','D','Eb','E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        values = [C,Db,D,Eb,E,F,Gb,G,Ab,A,Bb, B]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','blue', 'orange', 'pink','yellow', 'purple', 'red', 'green', 'grey']

        delete_indexes = []
        for i in range(len(values)):
            if values[i] == 0:
                delete_indexes.append(i)
        count = 0
        for i in delete_indexes:
                del values[i-count]
                del labels[i-count]
                del colors[i-count]
                del key_info[i-count]
                count+=1
        trace0 = go.Pie(labels=labels,
                        values=values,
                        textinfo="percent",
                        text=key_info,
                        hole=.3,
                        hoverinfo='text',
                        marker=dict(colors=colors,
                            line=dict(width=2,
                                color="black"))
                            )
    

        layout = go.Layout(
            title =dict(text = "Song keys for "+ album_name + "By " + artist_name,
                font=dict(size = 18,
                    color = 'rgb(255,255,255)')),
                paper_bgcolor='rgb(60,60,60)',
            
                legend=dict(font=dict(
                                size=18,
                                color="white"),
                    borderwidth=2,
                    bordercolor="white")
                )

        data = [trace0]
        fig = go.Figure(data = data, layout = layout)        
        py.plotly.plot(fig, filename="Keys of album songs")
