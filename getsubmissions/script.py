from google_drive_downloader import GoogleDriveDownloader as gdd
import numpy

f = open('ass.tsv','r')
X = f.readlines()

rollToTeam = {}
rollToFile = {}

for x in X:
    x = x.strip().split('\t')[1:]
    rollToTeam[x[1]] = x[0]
    rollToFile[x[1]] = x[10][33:]


for i in rollToFile.keys():
    name = 'submi/'  + rollToTeam[i]+ i +'.py'
    print('Downloading',name)
    gdd.download_file_from_google_drive(file_id=rollToFile[i],dest_path=name)
    print('Downloaded',name)