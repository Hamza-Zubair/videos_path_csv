#### For making video qc excel

##### Option1
1. Make sure Python is installed. if not installed, download and install Python and Whilst installing make sure the check box is ON for install pip
2. Download requirements.txt file and python videos_path_csv.py to your directory
3. Open cmd
4. Run the following command 
    pip install -r Path_to_file\requirements.txt
4. Afterwards, run the following script: python videos_path_csv.py
5. Give Path to the directory where your vid files are and click submit
6. Output CSV will be generated in the Users/username folder (or the cwd) (depends if run from idle or cmd)

##### Option2
1. Install anaconda which comes with jupyter lab (or pip install jupyter lab)
2. Download requirements.txt file and python videos_path_csv.ipynb to your directory
3. Open jupyter notebook and load python videos_path_csv.ipynb file
4. Change the **input_dir** variable in the **main()** function to the directory path where your vid files are
5. Run all cells
6. Output CSV will be generated in the script folder


  For terminal
  anaconda terminal: jupyter lab --notebook-dir E:
  cmd: python -m jupyterlab --notebook-dir E: 
  change the directory according to urs
