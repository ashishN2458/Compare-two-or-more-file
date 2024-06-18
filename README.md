#  Compare two different sheet to find common data
Compare two or more files line by line in Python using some formula and display yes or no keywords for data match line and implement auto sent mail.

Important Note: 
1. Create folder(unite) in custom folder path. For e.g /projectName/unite(folderName)/
2. Create two or more csv file as per header cols
   1. first file columnName: FIRST_UNIQUE, FIRST_SDN, FIRST_AccountID, First_FILEDATE, FIRST_Status
   2. second file columnName: SECOND_UNIQUE, SECOND_SDN, SECOND_AccountID, SECOND_FILEDATE, SECOND_Status
   3. Third file columnName: Third_UNIQUE, THird_SDN, THird_AccountID, Third_FILEDATE, Third_Status
3. After the script is executed the final csv file will display the column names as belows: 
"FIRST_UNIQUE, FIRST_SDN, FIRST_AccountID, First_FILEDATE, FIRST_Status, UniqueStatusMatch, THIRD_UNIQUE_ID, THIRD_FIRST_SDN, THIRD_AC_ID, THIRD_FILEDATE, ThirduniqueIDMatch, ThirdfirstsdnMatch, ThirdFirstIdMatch, ThirdsecondFileDateMatch,"
