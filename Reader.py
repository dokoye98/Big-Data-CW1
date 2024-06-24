
def url_reader(filePath='video_url.txt'):
    vids = []
    with open(filePath,'r') as file:
        for line in file:
            #this is the clean the whitespace after each url
            vids.append(line.strip())
    return vids