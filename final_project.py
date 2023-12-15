import networkx as nx
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import json
import textwrap
import copy
import os
import random
from datetime import datetime

# define main function to take user input and determine the type of plot to draw
def main():
    '''The entry point for generating a graph from comment trees of posts
    '''
    uInput = input(""" ☆ Hello, please choose a subreddit sample from which you would like to generate images ★\n
Enter 1 to choose r/Obesity\nEnter 2 to choose r/Fatlogic\n\nChoose a subreddit: """)
    # generate for r/Obesity
    if uInput == '1':
        layout = input("""\nNow, please choose the layout format for your image(s).\n
Enter 1 to choose the Kamada_Kawai layout\nEnter 2 to choose the shell layout
Enter 3 to choose the spring layout\nEnter 4 to choose the spiral layout
Enter 5 to choose the planar layout\n\nChoose a layout: """)
        compInput = input("""\nFinally, please enter 1 to generate a single graph from a random comment tree, and
enter 2 if you wish to generate graphs for all of the comment trees: """)
        if compInput == '1':
            plotObesityGraph(posts_with_comments[random.randint(0, len(posts_with_comments))], layout)
        elif compInput == '2':
            for p in posts_with_comments:
                plotObesityGraph(p, layout)
        else:
            print('Please follow the directions and enter a viable value')
    # generate for r/Fatlogic
    elif uInput == '2':
        layout = input("""\nNow, please choose the layout format for your image(s).\n
Enter 1 to choose the Kamada_Kawai layout\nEnter 2 to choose the shell layout
Enter 3 to choose the spring layout\nEnter 4 to choose the spiral layout
Enter 5 to choose the planar layout\n\nChoose a layout: """)
        compInput = input("""\nFinally, please enter 1 to generate a single graph from a random comment tree, and
enter 2 if you wish to generate graphs for all of the comment trees: """)
        if compInput == '1':
            plotFatGraph(fl_data[random.randint(0, len(posts_with_comments))], layout)
        elif compInput == '2':
            for p in fl_data:
                plotFatGraph(p, layout)
        else:
            print('Please follow the directions and enter a viable value')
    else:
        print('Please follow the directions and enter a viable value')


def buildCommentTree(comments):
    '''takes a list of dictionaries containing reddit comment data and nests them so that they form a tree
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
with open("json_data/top_comment_data.json", "r", encoding="UTF-8") as file:
    o_data = json.load(file)

# Load JSON data from file (fatlogic)
with open("json_data/fat_logic_comment_data.json", "r", encoding="UTF-8") as file:
    fl_data = json.load(file)

# replace the 'comments' part of the data with organized trees for both 
for post in o_data:
    post['comments'] = buildCommentTree(post['comments'])
for post in fl_data:
    post['comments'] = buildCommentTree(post['comments'])

# eliminate posts with no comments and retain those with 1 or more comments
# specifically for data from r/OBESITY because there are top posts with no comments
posts_with_comments = [post for post in o_data if 'comments' in post and post['comments']]

def convert_timestamp(timestamp):
    '''converts unix datetime value to yyyy-mm-dd (optional in project)
    '''
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

def splitTitle(title, max_width=75):
    '''breaks up post titles that are too long by setting the width limit to 75 characters
    
    '''
    # Use textwrap to wrap the title at spaces
    wrapped_title = textwrap.fill(title, width=max_width)
    return wrapped_title

def addNodesObesity(G, comment):
    # Recursively add nodes and edges for comments and their replies
    for reply in comment.get("comments", []):
        # set other node colors to cadetblue
        G.add_node(reply["comment_id"], label=convert_timestamp(reply["timestamp"]), color="cadetblue")  
        G.add_edge(comment["comment_id"], reply["comment_id"])
        addNodesObesity(G, reply)

def addNodesFat(G, comment):
    # Recursively add nodes and edges for comments and their replies
    for reply in comment.get("comments", []):
        # set other nodes color to delft blue
        G.add_node(reply["comment_id"], label=convert_timestamp(reply["timestamp"]), color="#29335C")  
        G.add_edge(comment["comment_id"], reply["comment_id"])
        addNodesFat(G, reply)

def plotObesityGraph(post_data, layout=1):
    '''plot a graph based on a comment tree for a post in r/obesity
    '''
    G = nx.DiGraph()
    # add root node for the post
    root_id = post_data["submission_id"]
    G.add_node(root_id, label=root_id, color="palevioletred")  # set root node color to red
    # add edges from the post to top-level comments
    for comment in post_data.get("comments", []):
        # set color for nodes surrounding root node
        G.add_node(comment["comment_id"], label=convert_timestamp(comment["timestamp"]), color="cadetblue")
        G.add_edge(root_id, comment["comment_id"])
        addNodesObesity(G, comment)
    # plot graph, ADJUST LAYOUT HERE
    pos = pickLayout(G, layout)
    # get node colors based on 'color' attribute
    node_colors = [G.nodes[node]["color"] for node in G.nodes]
    # get node labels based on 'label' attribute
    node_labels = {node: G.nodes[node]["label"] for node in G.nodes}
    nx.draw(
        G,
        pos,
        labels=node_labels,
        with_labels=True,
        font_size=8,
        node_size=700,
        font_color="black",
        node_color=node_colors,
        edge_color="gray",
        font_weight="bold",
    )
    # save the plot with the post title (optional, can change basis for saving)
    plt.title(splitTitle(post_data["title"]))
    folder_path = "plot_graphs"
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = os.path.join(folder_path, f"{post_data['submission_id']}_graph.png")
    # print(file_path)
    # plt.savefig(file_path)
    plt.show()

def plotFatGraph(post_data, layout=1):
    '''plot a graph based on a comment tree for a post in r/fatlogic
    '''
    G = nx.DiGraph()
    root_id = post_data["submission_id"]
    G.add_node(root_id, label=root_id, color="#E4572E")
    for comment in post_data.get("comments", []):
        # set color for nodes surrounding root node
        G.add_node(comment["comment_id"], color="#29335C")
        G.add_edge(root_id, comment["comment_id"])
        addNodesFat(G, comment)
    # plot graph, ADJUST LAYOUT HERE
    pos = pickLayout(G, layout)
    node_colors = [G.nodes[node]["color"] for node in G.nodes]
    # make root node and child nodes different sizes
    node_sizes = [300 if node == root_id else 30 for node in G.nodes]
    # only label root node w unique post ID
    node_labels = {node: G.nodes[node]["label"] if node == root_id else "" for node in G.nodes}
    nx.draw(
        G,
        pos,
        labels=node_labels,
        with_labels=True,
        font_size=8,
        font_color="black",
        node_color=node_colors,
        node_size=node_sizes,
        edge_color="gray",
        font_weight="bold",
    )

    # save the plot with the post title (optional, can change basis for saving)
    plt.title(splitTitle(post_data["title"]))
    folder_path = "plot_graphs"
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    file_path = os.path.join(folder_path, f"{post_data['submission_id']}_graph.png")
    # print(file_path)
    # plt.savefig(file_path)
    plt.show()

def pickLayout(graph, layout):
    '''returns the chosen graph layout for drawing
    '''
    if layout == '1':
        return nx.kamada_kawai_layout(graph)
    elif layout == '2':
        return nx.shell_layout(graph)
    elif layout == '3':
        return nx.spring_layout(graph)
    elif layout == '4':
        return nx.spiral_layout(graph)
    else:
        # default layout
        return nx.planar_layout(graph)


# line to test code
# plotFatGraph(fl_data[0])

# actually run main
if __name__ == '__main__':
    main()