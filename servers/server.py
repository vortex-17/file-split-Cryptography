from flask import Flask, request
import requests
import os
import glob

app = Flask(__name__)

# os.chdir("/storage")

peer_nodes = {
    "Bob" : "http://0.0.0.0:901",
    "Charlie" : "http://0.0.0.0:902",
    "David" : "http://0.0.0.0:903"
}

NAME = "Alice"
datalist= []

def find_file(filename):
    file_list = list(glob.glob("*.txt"))
    if filename in file_list:
        return True
    else:
        return False

@app.route('/')
def hello():
    return "Greetings! This is Alice."

@app.route('/send_file', methods = ["POST"])
def save_file():
    data = request.get_json(force = True)
    filename = data["filename"]
    content = data["content"]
    f = open(filename, "w")
    f.write("content")
    f.close()


@app.route("/fetch_file", methods = ["POST"])
def fetch_and_send():
    data = request.get_json(force = True)
    filename = data["filename"]
    to = peer_nodes[data["from"]]
    found = find_file(filename)
    if found == True:
        f = open(filename, "r")
        content = f.read()
        f.close()
        data_sent = {
            "from" : NAME,
            "filename" : filename,
            "content" : content,
            "found" : True
        }
        #send the data
        requests.post(url = to, data = data_sent)

    else:
        #send that the file is not received.
        data_sent = {
            "from" : NAME,
            "filename" : filename,
            "content" : "",
            "found" : False
        }

        requests.post(url = to, data = data_sent)
        
@app.route("/receive", methods = ["POST"])
def receive():
    data = request.get_json(force = True)
    datalist.append(data)
    print("Datalist : ",datalist)
    return "Thanks"
    # filename = data["filename"]
    # if data["found"] == False:
    #     print("File not found on ", data["from"] + "Machine")
    # else:
    #     content = data["content"]



if __name__ == "__main__":
    print("This is Alice")
    app.run(host='0.0.0.0', port=900,debug=True)