import os
import urllib.error
import urllib.parse
import urllib.request
import time
from PIL import Image, ImageDraw

year = 2024

def exists(day):
    """ Check if the data file for the given day (or sample file) exists """
    if isinstance(day, int):
        filename = f'./data/{day:02}.txt'
    else:
        filename = f'./data/{day}.txt'
    return os.path.exists(filename)

def load_data(day):
    """ Load the data file for the given day (or sample file). If the file does not exist,
      fetch it from the server. """
    if isinstance(day, int):
        filename = f'./data/{day:02}.txt'
    else:
        filename = f'./data/{day}.txt'

    print ("Loading data from", filename)

    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        if not isinstance(day, int) or day < 1 or day > 25:
            print ("File not found")
            return None
        
        print ("File not found, fetching from server")
        response = request(day)

        if response:
            with open(filename, 'w') as f:
                f.write(response)
            return response
        
def request(day):
    """ Fetch the data for the given day from the server """
    url = f'https://adventofcode.com/2024/day/{day}/input'
    headers = {
        'cookie': 'session=' + open('.session').read().strip()
    }

    httprequest = urllib.request.Request(url, headers=headers, method='GET')

    try:
        with urllib.request.urlopen(httprequest) as response:
            if (response.status == 200):
                return response.read().decode('utf-8')
            
            raise Exception("Error fetching data:", response.status, response.reason)
        
    except urllib.error.HTTPError as e:
        print ("Error fetching data:", e)
        return None
    
def timeit(func):
    """ Decorator to time a function """
    def wrapper(*args, **kwargs):
        tstart = time.perf_counter()
        result = func(*args, **kwargs)
        tend = time.perf_counter()
        print(f"{func.__name__} time: {(tend - tstart) * 1000:10,.1f} ms", end='\t')
        return result
    return wrapper

def drawMap(maze, nodeLists=[], scale=10):
    """
    Draw the map with the robot, boxes, and walls
    """
              
    # Create a new image with a white background
    img = Image.new('RGB', (len(maze[0]) * scale, len(maze)* scale), color='white')

    draw = ImageDraw.Draw(img)

    def point(p, color=(255, 0, 0)):
        c = p[1]
        r = p[0]
        draw.rectangle((c * scale, r * scale, c * scale + scale, r * scale + scale), fill=color)
    
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == '#':
                point((r, c), (0, 0, 0))

    if nodeLists:
        for nodes in nodeLists:
            if len(nodes) == 2:
                color = nodes[1]
            else:
                color = (255, 0, 0)
            for node in nodes[0]:
                point(node, color)

    return img


if __name__ == "__main__":
    print ("Running helper. You didn't want to do that.")