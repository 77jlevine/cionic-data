# CIONIC Data Tools


This is a modified repository from CIONIC for the Summer School on Neurorehabilitation 2025. These are the requirements: 

* numpy==1.23.4
* requests==2.32.3
* pandas==1.5.1
* scipy==1.9.3
* matplotlib==3.7.1


The three days of the workshop will use this python repository as well as the web interface. You can access the web interface by going to www.cionic.com/a. Type in the email that you provided for the conference and press enter. You should receive an email with a link from CIONIC, which will transfer you to the CIONIC dashboard, where you should see SSNR 2025. Click open. Then click open under SSNR 2025 Workshop. There should be 4 tabs on the lefthand side: 

* Collections: where your recordings will be stored.
* Upload: this tab will be used to upload recordings from the control units.
* Protocols: this tab will be used to create custom protocols.
* Participants: on the app, you will create a participant profile so that you can identify in the collections which data is yours. You can view individual participant data in this tab.


**WOKRSHOP DAY 1:**
On day 1, you will be recording EMG and IMU data during walking using the Cionic Neural Sleeve. 
1. Open the Cionic app on the iPad. 
2. Select SSNR 2025-SSNR 2025 Workshop at the top to select/create a subject.
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
13. Select Start. This will initiate calibration. You will be asked to stand with feet shoulder width apart for 3 seconds. Then you will be asked to sit with your leg (wearing the sleeve) extended for 3 seconds. After that recording will start immediately. You can press stop to end the recording and delete the file. Restart once you are ready by selecting start.
14. When completed, you can save the file with a unique identifier to help you find it.
15. After all recording are complete, navitgate to the **Upload** page on the Cionic web interface. Plug in the control unit to your computer via the USB cable provided. You will have to unplug and replug to establish the connection.
16. Once your control unit is identified by your computer. Select **Choose Files** and navigate to the files you would like to upload. The unique identifiers will not be present so you should select the files with the date of the collection. Then there will be two panels of recordings. Refer to the top one and look for the unique identifiers you named the recordings. Make sure there is a check mark only next to those. Then select upload. It will take some time depending on the size of your file and number of files to upload to the server. 

**WORKSHOP DAY 2:**
On day 2, you will be processing the EMG data you recorded on Day 1. To do this, you will need to download the data files from the Cionic web interface.
1. Navigate to www.cionic.com/a and log in. You may already be logged in.
2. Navigate to the **Participants** tab and select the participant data you would like to download.
3. For each recording, you will have to download separately. Select the recording you would like to download. Under attachments, scroll until you see **streams.npz**. Click on this file and download it. You will not need any other files. Please ensure that you saved your npz files in a directory **OUTSIDE** of this repository.  
4. Once downloaded, you will need to use this git repository. Please ensure you have all requirements listed above. There is also a requirements.txt file in the scripts folder. 
5. Open the file **SSNR_EMG_Extraction.py**. This scripts takes the npz file downloaded from the Cionic web interface and exports a csv file of EMG.
6. You must change two lines in the script for it to run. Set the **file_path** and **file_name** appropriately to accesss the npz files from which you wish to extract EMG.
7. Run the python script. This should create a csv file in the same directory as it was originally stored. Repeat this for as many recordings as you would like to download.

**WORKSHOP DAY 3:**
On day 3, you will be developing custom stimulation profiles for each muscle. After developing these profiles, you will need to convert them into code that the Cionic web interface will understand.
1. A this point, you have developed stimulation profiles for all of the muscles.
2. This should be saved in a csv file with the following format:
     * Headers to each column: lhl, lhm, lvl, lrf, lgl, lgm, lta
     * Underneath each header, there should be 101 data points corresponding to 0-100% of the gait cycle. The script will not run if the file is not exactly 101 data points long.
     * The values should range from 0 to 1.
     * This file should be saved in a directory **OUTSIDE** of this repository. 
4. Once you have developed this csv file, open the python file **SSNR_StimProtocol_Generator.py**.
5. You must change two lines in the script for it to run. Set the **file_path** and **file_name** appropriately to accesss the csv file from which you wish to code into stimulation for the Cionic device.
6. Run the python script. This sould create a json file in the same directory as it was originally stored. 
7. Navigate to www.cionic.com/a and log in. You may already be logged in.
8. Navigate to the **Protocols** tab and select New Protocol.
9. Name the new protocol with a unique identifier. You will be able to see everyone's stimulation protocols at the Workshop, so name it appropriately. 
10. Select the Text tab. You should see the code underlying the stimulation. Delete this
11. Open the recently created json file. Copy the contents and paste it in the Text tab under Protocols.
12. Select Save as New Version. It will not automatically save.
13. On the Cionic home screen, refresh by dragging the screen down. The new protocol should be present.
14. You can repeat this for as many protocols as you would like and you can update protocols by pasting new code in the text. You will have to end stimulation, refresh, and start again to enable the new stimulation protocol.
15. Another option for creating stimulation protocols is through the web interface. You can set when and how much you would like to stimulate. We will not be instructing on how to use this interface, but feel free to try it out. 



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





