#To compile this script through command prompt- python connect_populate_db.py

import xlrd
import pymysql

# Open the workbook and define the worksheet

book = xlrd.open_workbook("image.xlsx")    #open the excel file which contains 4 rows- imageID, imagePath, imageFormat, imageDescription
sheet = book.sheet_by_name("image")      #name of the sheet

# Establish a MySQL connection
database = pymysql.connect (host="52.53.147.106", user = "geet", passwd = "image", db = "imagerec")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = """INSERT INTO imageDB (imageID,imagePath,imageFormat,imageDescription) VALUES (%s, %s, %s, %s)"""
#query = """SELECT * FROM imageDB"""


# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(0, sheet.nrows):
		imageID		= sheet.cell(r,0).value
		imagePath	= sheet.cell(r,1).value
		imageFormat	= sheet.cell(r,2).value
		imageDescription	= sheet.cell(r,3).value
 
		

		# Assign values from each row
		values = (imageID, imagePath, imageFormat, imageDescription)
		
# Get the number of rows in the resultset
numrows = cursor.rowcount

# Get and display one row at a time
for x in range(0, numrows):
	row = cursor.fetchone()
	print (row[0], "-->", row[1])

		# Execute sql Query
	cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()


# Close the database connection
database.close()

# Print results
print ("")
print ("All Done! Bye, for now.")
print ("")
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print ("I just imported " ,columns, " columns and ", rows, " rows to MySQL!")