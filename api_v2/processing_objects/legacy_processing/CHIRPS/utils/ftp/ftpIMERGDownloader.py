'''

Created on March 2016
@author: Kris Stanton

Last Modified on June 2017
By Githika Tondapu
'''

import sys
import datetime
import os
import ftplib
import time
import CHIRPS.utils.configuration.parameters as params
import CHIRPS.dataclasses.IMERG_Data as IDC

# Tests 20160105 20160109
# startYYYYMMDD = "20160105"
# endYYYYMMDD = "20160109"
def download_IMERG(startYYYYMMDD, endYYYYMMDD):
    # Parse Start and End date ranges from strings
    #startYear = startYYYYMMDD[0:4]
    #startMonth = startYYYYMMDD[4:6]
    #startDay = startYYYYMMDD[6:8]
    
    #endYear = endYYYYMMDD[0:4]
    #endMonth = endYYYYMMDD[4:6]
    #endDay = endYYYYMMDD[6:8]
    
    # Set the Datatype number
    current_DataTypeNumber = 26  # Hardcoded until there are more IMERG types in here..
    
    # Instance of Imerg Data Classes
    IMERG_DataClass =  IDC.IMERG_Data()
    
    # Convert to dates
    dateFormat = "%Y%m%d"
    start_Date = datetime.datetime.strptime(startYYYYMMDD, dateFormat)
    end_Date = datetime.datetime.strptime(endYYYYMMDD, dateFormat)
    
    # Build expected string list
    #expected_FTP_FilePaths_TIF = []
    #expected_FTP_FilePaths_TFW = []
    expected_FTP_FilePaths = [] # "ftpPathTo_tif"  and "ftpPathTo_tfw
    # iterate through all dates
    delta = end_Date - start_Date
    for i in range(delta.days + 1):
        #print start_Date + datetime.timedelta(days=i)
        currentDate = start_Date + datetime.timedelta(days=i)
        print(currentDate)
        tifPath = IMERG_DataClass.get_Expected_FTP_FilePath_To_Tif(currentDate.year, currentDate.month, currentDate.day)
        tfwPath = IMERG_DataClass.get_Expected_FTP_FilePath_To_Tfw(currentDate.year, currentDate.month, currentDate.day)
        objToAdd = {
                    "ftpPathTo_tif":tifPath,
                    "ftpPathTo_tfw":tfwPath
                    }
        expected_FTP_FilePaths.append(objToAdd)
        #expected_FTP_FilePaths_TIF.append(tifPath)
        #expected_FTP_FilePaths_TFW.append(tfwPath)
        
    # Folder Stuff
        # Create the destination folder if it does not exist
    dataDestinationFolder = params.dataTypes[current_DataTypeNumber]['inputDataLocation']
    print("-Data Destination Folder (Downloading To) : " + str(dataDestinationFolder))
    testFolderPath = os.path.dirname(dataDestinationFolder)
    if not os.path.exists(testFolderPath):
        os.makedirs(testFolderPath)
        print("-Created a new folder at path: " + str(testFolderPath))
        
    
    
    # Connect to the FTP Server and download all of the files in the list.
    ftp_Connection = None
    try:
        print("Connecting to FTP.. : " + IMERG_DataClass.FTP_Host)
        ftp_Connection = ftplib.FTP(IMERG_DataClass.FTP_Host, IMERG_DataClass.FTP_UserName, IMERG_DataClass.FTP_UserPass)
        time.sleep(1)
    except:
        e = sys.exc_info()[0]
        print("-ERROR Connecting to FTP.. bailing out..., System Error Message: " + str(e))
        return
    
    print("-Downloading files... this may take a few minutes....")
    downloadCounter = 0
    # Iterate through all of our expected file paths
    for ftpFullFilePaths in expected_FTP_FilePaths: 
        
        isError = False
        errorLog = []
        
        # print progress
        if(downloadCounter % 10 == 0):
            print("-Downloaded: " + str(downloadCounter) + " rasters so far..")
        # Get the file names
        filenameOnly_Tif = ftpFullFilePaths['ftpPathTo_tif'].split('/')[-1]
        filenameOnly_Tfw = ftpFullFilePaths['ftpPathTo_tfw'].split('/')[-1]
        
        # Make local filenames
        local_FullFilePath_ToSave_Tif = os.path.join(dataDestinationFolder, filenameOnly_Tif)
        local_FullFilePath_ToSave_Twf = os.path.join(dataDestinationFolder, filenameOnly_Tfw)
        
        # Get directoryPath and Filename for FTP Server
        ftp_PathTo_TIF = IMERG_DataClass._get_FTP_FolderPath_From_FullFilePath(ftpFullFilePaths['ftpPathTo_tif'])
        ftp_PathTo_TWF= IMERG_DataClass._get_FTP_FolderPath_From_FullFilePath(ftpFullFilePaths['ftpPathTo_tfw'])
        print "*******************"
        print ftp_PathTo_TIF
        # Download the Tif
        try:
            fx= open(local_FullFilePath_ToSave_Tif, "wb")
            fx.close()
            os.chmod(local_FullFilePath_ToSave_Tif,0777)
        except:
            pass	
        try:
            with open(local_FullFilePath_ToSave_Tif, "wb") as f:
				ftp_Connection.retrbinary("RETR " + ftp_PathTo_TIF, f.write)  # "RETR %s" % ftp_PathTo_TIF	
        except:
            os.remove(local_FullFilePath_ToSave_Tif)  
            local_FullFilePath_ToSave_Tif = local_FullFilePath_ToSave_Tif.replace("03E", "04A")
            ftp_PathTo_TIF=ftp_PathTo_TIF.replace("03E", "04A")
            fx= open(local_FullFilePath_ToSave_Tif, "wb")
            fx.close()
            os.chmod(local_FullFilePath_ToSave_Tif,0777)
            try:
				with open(local_FullFilePath_ToSave_Tif, "wb") as f:
					ftp_Connection.retrbinary("RETR " + ftp_PathTo_TIF, f.write)  # "RETR %s" % ftp_PathTo_TIF	
            except:
				os.remove(local_FullFilePath_ToSave_Tif)  
				ftp_PathTo_TIF=ftp_PathTo_TIF.replace("04A", "04B")
				local_FullFilePath_ToSave_Tif = local_FullFilePath_ToSave_Tif.replace("04A", "04B")
				fx= open(local_FullFilePath_ToSave_Tif, "wb")
				fx.close()
				os.chmod(local_FullFilePath_ToSave_Tif,0777)
				try:
					with open(local_FullFilePath_ToSave_Tif, "wb") as f:
						ftp_Connection.retrbinary("RETR " + ftp_PathTo_TIF, f.write)  # "RETR %s" % ftp_PathTo_TIF	
				except:
					errorStr = "-ERROR Downloading  TIF file: " + ftp_PathTo_TIF
					print(errorStr)
					errorLog.append(errorStr)
					isError = True 
 		

        
        # Give the FTP Connection a short break (Server spam protection mitigation)
        time.sleep(3)
            
        # Download the Tfw
        fx= open(local_FullFilePath_ToSave_Twf, "wb")
        fx.close()
        os.chmod(local_FullFilePath_ToSave_Twf,0777)	
        try:
            with open(local_FullFilePath_ToSave_Twf, "wb") as f:
				ftp_Connection.retrbinary("RETR " + ftp_PathTo_TWF, f.write)  # "RETR %s" % ftp_PathTo_TIF	
        except:
            os.remove(local_FullFilePath_ToSave_Twf)  
            local_FullFilePath_ToSave_Twf = local_FullFilePath_ToSave_Twf.replace("03E", "04A")
            ftp_PathTo_TWF=ftp_PathTo_TWF.replace("03E", "04A")
            fx= open(local_FullFilePath_ToSave_Twf, "wb")
            fx.close()
            os.chmod(local_FullFilePath_ToSave_Twf,0777)
            try:
				with open(local_FullFilePath_ToSave_Twf, "wb") as f:
					ftp_Connection.retrbinary("RETR " + ftp_PathTo_TWF, f.write)  # "RETR %s" % ftp_PathTo_TIF	
            except:
				os.remove(local_FullFilePath_ToSave_Twf)  
				ftp_PathTo_TWF=ftp_PathTo_TWF.replace("04A", "04B")
				local_FullFilePath_ToSave_Twf = local_FullFilePath_ToSave_Twf.replace("04A", "04B")
				fx= open(local_FullFilePath_ToSave_Twf, "wb")
				fx.close()
				os.chmod(local_FullFilePath_ToSave_Twf,0777)
				try:
					with open(local_FullFilePath_ToSave_Twf, "wb") as f:
						ftp_Connection.retrbinary("RETR " + ftp_PathTo_TWF, f.write)  # "RETR %s" % ftp_PathTo_TIF	
				except:
					errorStr = "-ERROR Downloading  TWF file: " + ftp_PathTo_TWF
					print(errorStr)
					errorLog.append(errorStr)
					isError = True 

        
        # Give the FTP Connection a short break (Server spam protection mitigation)
        time.sleep(3)
        
        if isError == True:
            # try and remove the file??
            pass
        
        downloadCounter += 1
            
    #print "STOPPED RIGHT HERE!!! SHOULD ALREADY HAVE THE FILES... NOW NEED TO BETTER CATCH THE ERRORS AND REPORT THEM DOWN HERE... THATS ABOUT IT REALLY FOR THE DOWNLOADER....."
    
    # Pretty much done with the downloader for now..
    
    pass


# Expected input:
# - startDate (YYYYMMDD)
# - endDate (YYYYMMDD)
if __name__ == '__main__':
    print "Starting Downloading IMERG Data"
    args = len(sys.argv)
    if (args < 3):
        print "Usage: StartDate(YYYYMMDD) EndDate(YYYYMMDD)"
        sys.exit()
    else :
        print "IMERG_Downloader: Working on Date Range: ", sys.argv[1], " - ", sys.argv[2]
        download_IMERG(sys.argv[1], sys.argv[2])
        print "IMERG_Downloader: Done"
        

