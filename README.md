# Spmerg Introduction
##design purpose:
One of my work as a geology technician is to write down the field geological phenomena on a notebook and then iput the words into the DGS(Digital Geological System) in every single file. It's *tedious* to click the mouse during the process. I think it should easy and straightforward to input the words in a sigle '.xml' file and spilt it into sigle files corresponding to each geopoint. So I did this work.
split xml files into sigle .txt file based on their tags and merge .txt files into .xml files. 
##how to use
###split *.xml* file
invoke the bash shell under linux and go the reposity directory.
input the command to split the *L1220.xml* file under the *demo* directory, and it will generated a folder named *note*.

`python3 spmergy.py s ./demo/L1220.xml`
###merge above spilt files into sigle *.xml* file 
merge the files under the *./note/L1220* directory into a sigle *.xml* file for overall edit

`python3 spmergy.py m ./note/L1220`

