from pytube import YouTube
import pytube
import vlc
import urllib.request
import re
import os
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

session = HTMLSession()
no = 0

#video_url = ""

def get_video_metadata(url):


    #First Way:

    #response = session.get(url)
    #response.html.render(sleep=5)

    # soup = bs(response.html.html, "html.parser")

    #video_meta = {}
    # Video Title
    #video_meta["title"] = soup.find("h1").text.strip()
    # Views
    #video_meta["view"] = int(''.join([c for c in soup.find("span", attrs={"class": "view-count"}).text if c.isdigit() ]))
    #Date Published
    #video_meta["date_published"] = soup.find("div", {"id": "date"}).text[1:]
    #Number of Likes
    #text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id" : "text", "class": "ytd-toggle-button-renderer"})
    # video_meta["likes"] = text_yt_formatted_strings[0].text
    #Dislikes
    # video_meta["dislikes"] = text_yt_formatted_strings[1].text
    #print(video_meta)

    #Second Way
    yt = YouTube(url)
    print("Title: " + yt.title)
    #print("Views: " + yt.views)
    #print("Publish Date: " + yt.publish_date)
    #print("\n")

def return_to_menu(menu_number):
    print("[!] Invalid Move, Please Hit Enter to Return to the Menu...")
    input()
    clear()
    if (menu_number == 0):
        menu()
    if (menu_number == 1):
        search()
    if (menu_number == 2):
        watch_from_url()

def watch_from_url():
    clear()
    print('***---Watch From URL Screen---***\nType "_menu" to return to Main Menu\n')
    try:
        url = input("Enter your Full YouTube Video Link, \n Ex: https://www.youtube.com/watch?v=dQw4w9WgXcQ\nEnter Link Here: ")
        if (url == "_menu"):
            clear()
            menu()
        else:
            yt = YouTube(url)
            while True:
                resolution = input("Enter Resolution (Enter 'high' for highest, 'low' for lowest resolution): ")
                if (resolution == 'high' or resolution == 'low'):
                    break
                else:
                    continue
            if (resolution == 'high'):
                yt = yt.streams.get_highest_resolution()
            if (resolution == 'low'):
                yt = yt.streams.get_lowest_resolution()
            yt.download()
            print("[+] Successfully Downloaded the Video, Launching VLC now... \n")
            # media = vlc.MediaPlayer(media_title + ".mp4")
            the_media = ""
            for i in os.listdir():
                if i.endswith(".mp4"):
                    the_media = i
            media = vlc.MediaPlayer(the_media)  # Input filename here
            media.play()

            input("When you are done watching, Press Enter Here to Delete the Video and Return to Menu\n\n")

            media.stop()
            os.remove(the_media)
            clear()
            menu()
    except:
        print("Invalid Input, Press Enter For Returning To Menu")
        input()
        return_to_menu(2)





def watch(action, video_ids, resolution):


    try:
        if (action == "_menu"):
            clear()
            menu()
        elif (int(action) >= len(video_ids)):
            return_to_menu(1)
        else:
            video_url = "https://www.youtube.com/watch?v=" + video_ids[int(action)]
            yt = YouTube(video_url)
            if (resolution == 'high'):
                yt = yt.streams.get_highest_resolution()
            if (resolution == 'low'):
                yt = yt.streams.get_lowest_resolution()
            yt.download()
            print("[+] Successfully Downloaded the Video, Launching VLC now... \n")
            #media = vlc.MediaPlayer(media_title + ".mp4")
            the_media = ""
            for i in os.listdir():
                if i.endswith(".mp4"):
                    the_media = i
            media = vlc.MediaPlayer(the_media) #Input filename here
            media.play()

            input("When you are done watching, Press Enter Here to Delete the Video and Return to Menu\n\n")

            media.stop()
            os.remove(the_media)
            clear()
            menu()

    except:
        print("Invalid Input, Press Enter For Returning To Menu")
        input()
        return_to_menu(1)


def search():
    clear()
    print('**---Video Search Screen---**\nType "_menu" to return to Main Menu\n')
    try:
        search_action = str(input("Please Enter the keyword you would like to search on YouTube: ")).replace(" ", "+")

        if (search_action == "_menu"):
            menu()
        else:
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_action)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            #EX: First Video Link is: url = "https://www.youtube.com/watch?v=" + video_ids[0]
            for id in video_ids:
                global no
                print("Video No: " + str(no) + "\n")
                url =  "https://www.youtube.com/watch?v=" + id
                get_video_metadata(url)
                print("\n")
                no += 1
            action = input("Enter the No. of video you would like to watch or type _menu to return to main menu: ")
            no = 0
            resolution = input("Enter Resolution (Enter 'high' for highest, 'low' for lowest resolution): ")
            watch(action, video_ids, resolution)
    except:
        return_to_menu(1)

def menu():
    print("***Hello and Welcome to the Lite Youtube Watcher***\nMain Menu:\n")
    print("1-) Search Youtube\n2-) Enter URL to watch\n0-)Exit")
    try:
        menu_action = int(input("Select an Action: "))

        if (menu_action == 1):
            search()
        elif(menu_action == 2):
            watch_from_url()
        elif(menu_action == 0):
            quit()
        else:
            return_to_menu(0)
    except:
        return_to_menu(0)




menu()


