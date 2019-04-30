# ------------------------------------------
# Writtern by Subhashis Suara / QuantumBrute
# ------------------------------------------

from psaw import PushshiftAPI
import praw
import time
import re
import json


# --------------------------------------------------------------------------------

subreddit_name = 'QuantumBrute' # Mention the subreddit that bot should work on
limitno = 30000 # Set the maximum number of posts to get in the given timeframe
end_epoch=int(time.time()) # Current time
x = int(input("Enter the number of days you want to search for:"))
start_epoch=int(end_epoch - (60*60*24*x)) # Current time - the amount you mention in seconds

#---------------------------------------------------------------------------------

print("Starting Bot...")

reddit = praw.Reddit(client_id= ' ',         
		     client_secret= ' ',
		     username= ' ',
		     password= ' ',
		     user_agent= ' ') # Login to reddit API

api = PushshiftAPI() # Variable to use the PushShiftAPI
subreddit = reddit.subreddit(subreddit_name)

print("From: "+ str(start_epoch))
print("Till: "+ str(end_epoch))


result = list(api.search_submissions(after=start_epoch, 
                                    before=end_epoch,
                                    subreddit=subreddit_name,
                                    filter=['author', 'id'],
                                    limit=limitno)) # Gets the data with the parameters mentioned from PushShift and makes it into a list

def Delete_Submissions():
    print("Opening database...")
    with open('Database.txt', 'r') as infile: # Opens the database
        info = json.load(infile,)
    
    print("Going through posts & comments for !qualitypost...")
    print(' ')

    data = []

    for b in range(len(info)): # Copies the database to a list named data to make it easier to modify the elements of the database
        data.append(info[b])

    post_ids = []

    for i in range(len(result)):
        post_ids.append(result[i].id) # Gathers the ids of all posts in given time frame

    post_ids_size = len(post_ids)

    for j in range(post_ids_size):
        submission = reddit.submission(post_ids[j])
        submission.comments.replace_more(limit=None)
        author = result[j].author
        comment_authors = []

        for comment in submission.comments.list(): # Goes through comments of post; Note: .list() is used to flatten all hierarchy of comments into a single list
            if comment.saved:
                continue
            flag = 0
            keyword = re.search("!qualitypost", comment.body) # Searches for !nominate in the comment
            if keyword: # Whole process of checking and deleting
                if comment.author == author:
                    comment.save()
                    print("!qualitypost comment found! Made by OP: u/" + author)
                    print("Deleting comment and adding OP to database...")
                    print(' ')
                    comment.mod.remove(spam=False)
                    item = { "Name" : str(author), "ID" : comment.id }
                    data.append(item)
                    continue
                else:
                    for a in range(len(comment_authors)):
                        if comment.author == comment_authors[a]: # Searches author in the author's list stored from comments of that post
                            comment.save()
                            print("Duplicate !qualitypost comment found! Made by u/" + str(comment.author))
                            print("Deleting comment and adding u/" + str(comment.author) + " to database...")
                            print(' ')
                            item = { "Name" : str(comment.author), "ID" : comment.id }
                            data.append(item)
                            comment.mod.remove(spam=False)
                            flag = 1
                            break
                            
                    if flag == 0:    
                        comment_authors.append(comment.author) # If author is not in list, adds the author to list for next rounds of search
                    
    with open('Database.txt', 'w') as outfile: # Overwites the JSON file with updated data
        json.dump(data, outfile, indent=2)
        print("Database updated successfully!")
    print(' ')
    input("Press ENTER to exit...")




def main():
    Delete_Submissions()
    
if __name__ == "__main__": 
    main()
