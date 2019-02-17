import sys 
import json
import sys
from urllib import *
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import  urlopen
from textblob import TextBlob
import matplotlib
import matplotlib.pyplot as plt 

YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

list = []
new_list = []
pos = []
neg = []
neu = []
class YouTubeApi():

    def load_comments(self, mat):
        
        # with open('in.json', 'w') as outfile:
            for item in mat["items"]:
                comment = item["snippet"]["topLevelComment"]
                author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]
                
                if 'replies' in item.keys():
                    for reply in item['replies']['comments']:
                        rauthor = reply['snippet']['authorDisplayName']
                        rtext = reply["snippet"]["textDisplay"]
                #     outfile.write("{}".format(rtext)) 
                # outfile.write("{}".format(text))
                    list.append("{}".format(rtext)) 
                list.append("{}".format(text)) 
            for x in list:
                p = TextBlob(x)
                new_list.append(p.sentiment.polarity)

            for line in new_list:
                v = float(line)
                if v > 0:
                    pos.append(v)
                elif v == 0:
                    neu.append(v)
                else:
                    neg.append(v)

            p = len(pos)
            nu = len(neu)
            n = len(neg)

            sentiments = [p,nu,n]
            labels = ['positive', 'neutral', 'negative']
            colors = ['green', 'yellow', 'red']
            plt.pie(sentiments, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
 
            plt.axis('equal')
            plt.show()


    def get_video_comment(self):
        parser = argparse.ArgumentParser()
        mxRes = 20
        vid = str()
        parser.add_argument("--c", help="calls comment function by keyword function", action='store_true')
        parser.add_argument("--max", help="number of comments to return")
        parser.add_argument("--videourl", help="Required URL for which comments to return")
        parser.add_argument("--key", help="Required API key")

        args = parser.parse_args()

        if not args.max:
            args.max = mxRes

        if not args.videourl:
            exit("Please specify video URL using the --videourl=parameter.")

        if not args.key:
            exit("Please specify API key using the --key=parameter.")

        try:
            video_id = urlparse(str(args.videourl))
            q = parse_qs(video_id.query)
            vid = q["v"][0]

        except:
            print("Invalid YouTube URL")

        parms = {
                    'part': 'snippet,replies',
                    'maxResults': args.max,
                    'videoId': vid,
                    'textFormat': 'plainText',
                    'key': args.key
                }

        try:

            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            i = 2
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            
            
            self.load_comments(mat)

            while nextPageToken:
                parms.update({'pageToken': nextPageToken})
                matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
                mat = json.loads(matches)
                nextPageToken = mat.get("nextPageToken")
                
                

                self.load_comments(mat)

                i += 1
        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")



    

    def openURL(self, url, parms):
            f = urlopen(url + '?' + urlencode(parms))
            data = f.read()
            f.close()
            matches = data.decode("utf-8")
            return matches



def main():
    y = YouTubeApi()

    
    if str(sys.argv[1]) == "--c":
        y.get_video_comment()
    
    else:
        print("Invalid Arguments\nAdd --s for searching video by keyword after the filename\nAdd --c to list comments after the filename\nAdd --sc to list vidoes based on channel id")


if __name__ == '__main__':
    main()