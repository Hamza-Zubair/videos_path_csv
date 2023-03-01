#pip install -r requirements.txt
## DEPENDENCIES
from pathlib import Path
from datetime import datetime
from tkinter import *
import pandas as pd
import numpy as np
import cv2
import os


## FUNCTIONS
# FUNCTION TO GET VIDEO FILE NAMES AND ITS SIZES
def video_duration(input_dir):
    """ Input: takes absolute directory path and calculate duration of video files in it (checks for preview.mp4 files)
        Output: returns pandas dataframe
    """
    # convert raw directory to window Path
    directory = Path(input_dir)
    # empty lists to store the file name and duration
    file_name= []
    file_duration = []
    # loop through directory
    for folder in directory.glob('**'):
        for filename in folder.iterdir():
            # only look for those videos which end with preview
            if str(filename).endswith('preview.mp4'):
                # create video capture object
                data = cv2.VideoCapture(str(filename))
                # count the number of frames
                frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
                fps = data.get(cv2.CAP_PROP_FPS)
                # calculate duration of the video
                seconds = round(frames / fps)
                # append file name and duration to our lists
                file_name.append((str(filename)))
                file_duration.append(seconds)
    # zip the shit together        
    data_zipped = list(zip(file_name,file_duration))
    # create the data frame
    df = pd.DataFrame( data = data_zipped, columns = ['raw_name', 'duration(secs)'])
    # return the result
    return df



# FUNCTION TO GET FOLDER NAMES AND FOLDER SIZES IN DIRECTORY
def directory_size(input_dir):
    """ Input: takes absolute directory path and calculate all folder and sub folder's size in gb
        Output: returns pandas dataframe
    """
    # convert raw directory to window Path
    directory = Path(input_dir)
    # empty lists to store the file name and duration
    folder_name = []
    folder_size = []
    # loop through the folders, sub folders upto files
    for level_zero in directory.glob('**'):
        for level_end in level_zero.iterdir():
            # check for directories only not files
            if level_end.is_dir() == True:
                # calculate folder sizes
                size = sum(file.stat().st_size for file in level_end.iterdir())
                total_size = round(((size/1024)/1024)/1024, 2)
                # append the folder names and it sizes in gb
                folder_name.append(str(level_end))
                folder_size.append(total_size)
    # zip name and size together
    data_zipped = list(zip(folder_name,folder_size))
    # create the data frame
    df = pd.DataFrame( data = data_zipped, columns = ['folder_name', 'size(gb)'])
    # return the result
    return df



def main():
    ## setup a GUI window
    parent = Tk()
    parent.geometry('750x250')
    ## name the GUI window
    parent.title('Windows directory to CSV maker')

    ## create labels and inputs and buttons
    # LABELS
    Label(parent, text="Enter directory path").grid(row=0, column =0)


    # INPUTS
    directory_input = Entry(parent, width=80)
    directory_input.grid(row=0, column =1,sticky="W")

## tkinter event functions
    def submit_button():
        global a
        a = directory_input.get()
        parent.destroy()

    def clear_button():
        directory_input.delete(0, END)

    # BUTTONS
    submit = Button(parent, text = 'Submit', fg = 'green', command = submit_button).grid(row=3, column =0)
    clear = Button(parent, text = 'Clear', fg = 'red', command = clear_button).grid(row=3, column =1)
    # execute the loop
    parent.mainloop()


    # directory path
    input_dir = a
    
    dir_size = directory_size(input_dir)   # folder sizes
    vid_duration = video_duration(input_dir)   # video files duration
    
    # process and reshape video duration dataframe
    vid_duration['day'] = vid_duration['raw_name'].str.rsplit(pat="\\").str[-3]             # assumes that third element from right is always day
    vid_duration['file_name'] = vid_duration['raw_name'].str.rsplit(pat="\\").str[-2]       # assumes that second element from right is always file name
    vid_duration['quality (ok/not okay/in between)'] =np.NaN                            # add empty columns required  
    vid_duration['deleted'] =np.NaN                                                     # add empty columns required  
    vid_duration['comments'] =np.NaN                                                    # add empty columns required  
    vid_duration['is_snow(1/0)'] =np.NaN                                                # add empty columns required  
    vid_duration['folder_name'] = vid_duration['raw_name'].str.rsplit(pat="\\", n=1).str[0]   # folder name reshape to join with other df

    # merge video duration and folder size dataframes
    final_df = vid_duration.merge(dir_size, how='left', on = 'folder_name')

    # keep selected columns
    final_df = final_df.loc[:, final_df.columns.drop('folder_name')]

    # some more reshaping
    final_df['links to screenshots (if works)'] =np.NaN                                 # add empty columns required  
    
    #export csv
    cwd = os.getcwd()
    f_out_name = ('output_{}.csv'.format(datetime.now().strftime("%Y_%m_%d-%I-%M-%S%p")))
    final_df.to_csv(os.path.join(cwd, f_out_name), index=False)
    
    

# CONDITIONAL BLOCK
if __name__ == '__main__':
    main()


