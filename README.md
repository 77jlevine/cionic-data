# CIONIC Data Tools


This is a modified repository from CIONIC for the Summer School on Neurorehabilitation 2025. These are the requirements: 

numpy==1.23.4
requests==2.32.3
pandas==1.5.1
scipy==1.9.3
matplotlib==3.7.1


The three days of the workshop will use this repository as well as the web interface. You can access the web interface by going to www.cionic.com/a. Type in the email that you provided for the conference and press enter. You should receive an email with a link from CIONIC, which will transfer you to the CIONIC dashboard, where you should see SSNR 2025. Click open. Then click open under SSNR 2025 Workshop. There should be 4 tabs on the lefthand side: 

* Collections: where your recordings will be stored.
* Upload: this tab will be used to upload recordings from the control units.
* Protocols: this tab will be used to create custom protocols.
* Participants: on the app, you will create a participant profile so that you can identify in the collections which data is yours. You can view individual participant data in this tab.


WOKRSHOP DAY 1:
On day 1, you will be recording EMG and IMU data during walking using the Cionic Neural Sleeve. 
1. Open the Cionic app on the iPad. 
2. Select SSNR 2025-SSNR 2025 Workshop at the top to select/create a subject
3. Select SSNR 2025 Workshop under ssnr2025 study. 
4. Either select the participant or select Add Participant. 
5. Type in any identifer for first and last name that you would like and type in any email. You do not need to add anything else. Select Submit when you are finished.
6. Put on the Cionic Neural Sleeve as instructed in the workshop. 
7. Connect the control unit to the iPad by pressing the power button and selecting on the iPad the control unit icon in the upper right. 
8. If the control unit is already connected, it should be visible under Connected. If not, it should be under available. Select the number that matches the number on the control unit. 
9. Slide the control unit into the sleeve pocket and then connect it to the sleeve. 
10. Restart the control unit on the app.
11. After restarting, it should say Left- before the control unit. 
12. On the main page, select Freeform. This is the EMG recording mode. 
13. Select Start. This will initiate calibration. You will be asked to stand with feet shoulder width apart for 5 seconds. Then you will be asked to sit with your leg (wearing the sleeve) extended for 5 seconds. After that recording will start immediately. You can press stop to end the recording and delete the file. Restart once you are ready by selecting start. When completed, you can save the file with a unique identifier to help you find it. 


There are two files that you will be using: 

* SSNR_EMG_Extraction.py - Workshop Day 2: Extracts EMG data from npz file downloaded from CIONIC. See workshop_sample_data\EMG Input for sample npz files and workshop_sample_data\EMG Output for the structure of the outputted EMG. It will include time, EMG signals for each muscle, and sagittal shank IMU data. 

* SSNR_StimProtocol_Generator.py - Workshop Day 3: Takes in a stimulation profile for each muscle and codes it to a stimulation protocol written in .json. Once created, copy the .json file into a new protocol under the text tab. See workshop_sample_data\Stimulation Input for structure of these files and workshop_sample_data\Stimulation Output for sample .json files. 


This repository provides tools for fetching and manipulating cionic collection data.

There are currently two supported libraries: command line scripts, and jupyter notebooks.  
Both methods make use of shared python code in the [cionic](cionic) directory 

* [scripts](scripts/README.md)  
  command line scripts for syncing collection data from the cionic servers
* [jupyter](jupyter/README.md)  
  jupyter notebooks (via docker) for running data analysis

Additional documentation:

* [npz](npz.md)  
  outlines the format of cionic npz files





