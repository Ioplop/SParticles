# SParticles

A simple 2d particle simulation made using mainly the pygame library in python.


# Requirements:

Python 3.10.0 or greater

# Installation

## Windows

1. Create an empty folder to hold your files  
2. Put the files on that folder  
    1. Using git:  
        - Open a command line and navigate to the folder  
        - Clone the repo with the following command:  
            > git clone https://github.com/Ioplop/SParticles.git .  
    2. Without git:  
        - Download this repo and extract it on the folder  
3. Open a command line and navigate to the project folder  
4. Create a python venv using the following command:  
    > python -m venv venv  
5. Activate the venv using the following command:  
    > venv\Scripts\Activate  
6. Install the required libraries on that venv using the following command:  
    > pip install -r requirements.txt  

## Linux

1. Create an empty folder to hold your files  
2. Put the files on that folder  
    1. Using git:  
        - Open a command line and navigate to the folder  
        - Clone the repo with the following command:  
            > git clone https://github.com/Ioplop/SParticles.git .  
    2. Without git:  
        - Download this repo and extract it on the folder  
3. Open a command line and navigate to the project folder  
4. Create a python venv using the following command:  
    > python3 -m venv venv  
5. Activate the venv using the following command:  
    > source venv/bin/activate  
6. Install the required libraries on that venv using the following command:  
    > pip install -r requirements.txt  

# Starting the simulation

To start the simulation, you have to activate your venv and run the main.py script.

## Windows

1. Open a command line and navigate to the project folder  
2. Activate your venv with the following command:  
    > venv\Scripts\Activate  
3. Run the main.py script with the following command:  
    > python main.py  

## Linux

1. Open a command line and navigate to the project folder  
2. Activate your venv with the following command:  
    > source venv/bin/activate  
3. Run the main.py script with the following command:  
    > python main.py  

# Controls

While the simulation is running, you can press ESC to quit the simulation.  

Press SPACE BAR to pause the simulation  
While paused:  
- Press "," (Comma) to advance one frame.  
- Hold "." (Colon) to continue the simulation.  
- Press SPACE BAR to unpause.  