### Graphical Comparisons between Reddit Post Comments from r/obesity and r/fatlogic

#### I. Project Description

The main goal of this project is to represent the hierarchical structure of subreddit posts and comments from (1) [r/obesity](https://www.reddit.com/r/Obesity/) and (2) [r/fatlogic](https://www.reddit.com/r/fatlogic/) with tree graphs. 
The main application ([```final_project.py```](https://github.com/AxueWithoutU/si507_final_project/blob/master/final_project.py)) that you can run via command line generates graphs from cached data from the aforementioned subreddits. You can choose from the 5 following layouts:

- Kamada-Kawai layout
- shell layout
- spring layout
- spiral layout
- planar layout

You will then choose to generate:
- a single graph from a random post's comment trees
- a combined graph of all posts' comment trees from a specific subreddit data sample

For singular random graphs only, the number on the root node indicates the maximum depths across all comment trees/threads under the post. The comment nodes of r/obesity graphs are labeled with their respective posting dates.  

#### II. Packages to Install before Running

- [networkx](https://networkx.org/)
    ```pip install networkx```

#### III. How to Use the Project

1. To use the program, the user should download [```final_project.py```](https://github.com/AxueWithoutU/si507_final_project/blob/master/final_project.py) and the [```json_data```](https://github.com/AxueWithoutU/si507_final_project/tree/master/json_data) folder, and put the both in the same location to ensure no errors occur. 
1. The user can run the python program (final_project.py) via command line or any other software that supports a compatible command line interface.
1. After starting the program, the user will be prompted to choose the following:
- The subreddit to sample data from for drawing the graph(s)
    - Enter 1 for r/obesity data
    - Enter 2 for r/fatlogic data
- The preferred layout for drawing the graph(s)
    - Enter 1 for the [Kamada-Kawai layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html)
    - Enter 2 for the [shell layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.shell_layout.html)
    - Enter 3 for the [spring layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html)
    - Enter 4 for the [spiral layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spiral_layout.html)
    - Enter 5 or anything else for the default [planar layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.planar_layout.html)
- Whether to draw (1) a single graph from a random post or (2) a combined figure with graphs of all posts
    - Enter 1 to generate a single graph
    - Enter 2 to generate a combined figure with all graphs
1. A pop-up window will show an image based on the user's input, and the program will terminate when the pop-up window is closed.