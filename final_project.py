import praw
import networkx as nx
import matplotlib.pyplot as plt
import json
import textwrap
import copy
import os
import time
from datetime import datetime

def buildCommentTree(comments):
    '''takes a list of dictionaries containing reddit comment data, 
    '''
    tree = []
    di = {}
    # create a deep copy of the comments list so that it is not altered
    # after running buildCommentTree() over the same slice of comment data
    # multiple times
    comments_copy = copy.deepcopy(comments)
    # create a dictionary with key-value pairs using the unique comment IDs as keys
    for comment in comments_copy:
        di[comment['comment_id']] = comment
    for comment in comments_copy:
        comment_id = comment['comment_id']
        # remove the t3 or t1 prefixes from parent IDs
        parent_id = comment['parent'][3:]
        # Check if the comment is a top-level comment
        # the parents of top-levels posts are the post itself, and therefore not present here
        if parent_id not in di:
            tree.append(di[comment_id])
        else:
            parent = di[parent_id]
            if "comments" not in parent:
                parent["comments"] = []
            parent["comments"].append(di[comment_id])
    return tree

# Load JSON data from file (obesity)
with open("json_data/top_comment_data.json", "r") as file:
    o_data = json.load(file)

# Load JSON data from file (fatlogic)
with open("json_data/fat_logic_comment_data.json", "r") as file:
    fl_data = json.load(file)

# replace the 'comments' part of the data with organized trees for both 
for post in o_data:
    post['comments'] = buildCommentTree(post['comments'])
for post in fl_data:
    post['comments'] = buildCommentTree(post['comments'])

# eliminate posts with no comments and retain those with 1 or more comments
# specifically for o_data because there are top posts with no comments
posts_with_comments = [post for post in o_data if 'comments' in post and post['comments']]

def convert_timestamp(timestamp):
    '''
    '''
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

def splitTitle(title, max_width=75):
    '''breaks up post titles that are too long by setting the width limit to 75 characters
    
    '''
    # Use textwrap to wrap the title at spaces
    wrapped_title = textwrap.fill(title, width=max_width)
    return wrapped_title