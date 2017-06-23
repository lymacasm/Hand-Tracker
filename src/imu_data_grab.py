import sys
import csv
from imu import IMU

def main(argv):
    imu = IMU()
    imu.setAccelRangeG(8)
    imu.setGyroRangeDps(1000)

    data = []
    classes = []
    
    while True:
        orientation = raw_input("Enter orientation (q to quit): ")
        
        # Check if user wants to quit
        if orientation == "q":
            # Prompt user to save data to file
            answer = ""
            while answer not in ["n", "y", "yes", "no"]:
                answer = raw_input("Save to data to file? (y/n): ")
                # Save to file if user entered yes
                if answer in ["y", "yes"]:
                    # Prompt user for filename
                    file_name = raw_input("Enter file name (q to cancel): ")
                    if file_name is not "q":
                        print "Saving data to %s" % file_name
                        with open(file_name, 'w') as csvfile:
                            data_writter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            first_row = ["AccelX","AccelY", "AccelZ", "GyroX", "GyroY", "GyroZ", "Class"]
                            first_row = first_row + [("%s=%s" % (classes.index(x), x)) for x in classes]
                            data_writter.writerow(first_row)
                            for row in data:
                                data_writter.writerow(row)                            
            # Exit program
            break
        
        if orientation not in classes:
            classes = classes + [orientation]
        this_class = classes.index(orientation)

        data_count = input("Enter number of data points: ")
        for i in range(0,data_count):
            data.append([imu.getAccelX(), imu.getAccelY(), imu.getAccelZ(), imu.getGyroX(), imu.getGyroY(), imu.getGyroZ(), this_class])
            

if __name__ == "__main__":
    main(sys.argv)
