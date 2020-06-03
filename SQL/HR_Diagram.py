import sqlite3
from matplotlib import pyplot as plt

connection = sqlite3.connect("hipparcos.db")
cursor = connection.cursor()
# Created the cursor object to connect the database.
# Commands.
sql_command = '\
    SELECT "B-V", VAbsMag FROM photometry \
    JOIN data ON data.HIP = photometry.HIP \
    WHERE e_Dist < 10 and e_Dist != 0 and "B-V" != 0 \
    ORDER BY "B-V";'
cursor.execute(sql_command)
# Put all the data into a container:
# put B-V and VabsMag into different lists
results = cursor.fetchall()
BV = [item[0] for item in results]
VabsMag = [item[1] for item in results]
# Do the same query again with two more conditions
# to filter out the white dwarf stars

sql_command_wd = '\
    SELECT "B-V", VAbsMag FROM photometry \
    JOIN data ON data.HIP = photometry.HIP \
    WHERE e_Dist < 10 and e_Dist != 0 and "B-V" != 0 \
    and "B-V" < 0.7 and VAbsMag > 10 \
    ORDER BY "B-V";'
cursor.execute(sql_command_wd)
results_wd = cursor.fetchall()
BV_wd = [item[0] for item in results_wd]
VabsMag_wd = [item[1] for item in results_wd]
# Now let's draw some pictures!
fig, ax = plt.subplots(1, 1)
ax.plot(BV, VabsMag, "x", label='All the Data')
ax.plot(BV_wd, VabsMag_wd, "+", label='White Dwarf Stars Data')
ax.invert_yaxis()
ax.set_xlabel('Color')  # Add an x-label to the axes.
ax.set_ylabel('Absolute V mag')
ax.set_title("HR Diagram - Color Magnitude Diagram")
plt.legend(numpoints=1, loc='best')
plt.show()
