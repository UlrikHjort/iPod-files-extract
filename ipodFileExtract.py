########################################################################
#                                                                           
#                                                                    
#                          Ipod file extract                                                            
#                          ipodFileExtract.py                                      
#                                                                           
#                                MAIN                                      
#                                                                           
#                 Copyright (C) 2020 Ulrik Hoerlyk Hjort                   
#                                                                        
#  Ipod file extract is free software;  you can  redistribute it                          
#  and/or modify it under terms of the  GNU General Public License          
#  as published  by the Free Software  Foundation;  either version 2,       
#  or (at your option) any later version.                                   
#  Ipod file extract is distributed in the hope that it will be                           
#  useful, but WITHOUT ANY WARRANTY;  without even the  implied warranty    
#  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  
#  See the GNU General Public License for  more details.                    
#  You should have  received  a copy of the GNU General                     
#  Public License  distributed with Yolk.  If not, write  to  the  Free     
#  Software Foundation,  51  Franklin  Street,  Fifth  Floor, Boston,       
#  MA 02110 - 1301, USA.                                                    
########################################################################        
import subprocess
import glob
import pathlib
from shutil import copyfile

SOURCE_DIR="./Music/" # Top dir of ipod music (usually iPod_Control/Music/)
EXTENSION="*.mp3"     # Source file extensions
DEST_DIR="./dest/"    # Destination dir for the extracted music files

pathlib.Path(DEST_DIR).mkdir(parents=True, exist_ok=True)

filelist = glob.glob(SOURCE_DIR+"/*/"+EXTENSION)

files = {}
for f in filelist:    
    result = subprocess.run(['mediainfo', f], stdout=subprocess.PIPE) # Build with MediaInfoLib - v19.09 (Other versions may work as well)
    info = result.stdout.decode("utf-8").split('\n')
    tags = ['Album', 'Track name', 'Track name/Position', 'Performer']

    track = {}
    for e in info:
        es = e.split(":")
        if es[0].strip() in tags:            
            track[es[0].strip()] = es[1].strip()
    files[f]=track

for ipod_file, track in files.items():
    performer=track.get('Performer','PERFORMER-NULL')
    album=track.get('Album',"ALBUM-NULL")
    PATH = DEST_DIR+performer+"/"+album
    pathlib.Path(PATH).mkdir(parents=True, exist_ok=True)
    position = ("{:02d}".format(int(track.get('Track name/Position','0')))) # Add leading zero
    trackname=track.get('Track name','TRACK-NULL').replace('/', '-') # replace "/" in track name
    new_file = PATH +"/" + position + "-" + trackname + ".mp3" 
    copyfile(ipod_file, new_file)
    
    
