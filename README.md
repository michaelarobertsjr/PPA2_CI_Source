# PPA2_CI_Source
Source code for use in Continuous Integration server set up in PPA2

To run this application, please follow these steps

Run the following command...

docker run --name=ppa2_database -p 3306:3306 -d -e MYSQL_ROOT_PASSWORD=roots mysql:latest

...to set up the mysql container to save the entries to a database

Download python 3.7.4 from the following link on your local machine:

https://www.python.org/downloads/release/python-374/

Next, open command prompt on your local machine and enter the following commands to set up the necessary python libraries needed for the project:

python -m pip install --upgrade pip
pip install pytest
pip install sqlalchemy
pip install mypysql
pip install flask

Finally, clone this repository to your local device, navigate to its directory, and execute the program using the following command:

python ppa2src.py

You can interact with the functions included either in the command line interface or by using the associated web-enabled interface by navigating to any of the following:

1.  localhost:5000/bmi to see all bmi entries
2.  localhost:5000/distance to see all distance entries
3.  localhost:5000/bmi/ht/wt to run the bmi function, replacing ht with your combined term height (511 for 5 foot 11 inches) with no space and replacing wt with your weight
4.  localhost:5000/distance/x1/y1/x2/y2 to run the distance function, replacing the xs and ys with your values

Additionally:

To test the application on your local machine, navigate to the applications local directory and run ...

pytest ppa2_test.py 

