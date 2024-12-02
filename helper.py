import urllib.error
import urllib.parse
import urllib.request

year = 2024

def load_data(day):
    if isinstance(day, int):
        filename = f'./data/{day:02}.txt'
    else:
        filename = f'./data/{day}.txt'

    print ("Loading data from", filename)

    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        print ("File not found, fetching from server")
        response = request(day)

        if response:
            with open(filename, 'w') as f:
                f.write(response)
            return response
        
def request(day):
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
    
if __name__ == "__main__":
    print ("Running helper")
    print ("Year:", year)
    

