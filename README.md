
# Advanced File Distribution System

##  Problem Statement 
Imagine an IT administrator tasked with distributing critical software updates, project documents, or training materials across hundreds of systems. This process is often time-consuming and resource-draining. Traditional methods like shared folders and email attachments are akin to sending each user a separate copy of a giant file, one packet at a time – it's slow, difficult to scale, and inefficiently utilizes network bandwidth. There must be a better way!

This project offers a solution to this problem by designing a path-breaking file-sharing system. The aim is to explore the intricacies of network programming and create a tool that is not only functional but also efficient, secure, and user-friendly.

##  Key Features 

###  File Distribution 
-  Initiate File Transfers : Administrators can initiate file transfers to a group of systems within the organization, streamlining the distribution process.
-  Efficient Network Usage : The tool ensures optimal use of the organization's network bandwidth, preventing unnecessary congestion.
-  Integrity Checks : The tool maintains the integrity of transferred files, ensuring that they reach their destination without corruption.

###  Group Management 
-  Create & Manage Groups : Administrators can create and manage user groups, making it easier to organize and control file distribution.
-  Real-time Monitoring : Real-time monitoring of transfer logs allows administrators to track the progress and status of ongoing file distributions.
-  User Discovery : Users can discover and join available groups, facilitating seamless integration into the system.

###  Security 
-  Controlled Distribution : Only administrators have the privilege to distribute files, ensuring that the process remains secure and controlled.
-  User Access Management : Administrators have the ability to control user access within groups, adding an additional layer of security.

##  Installation 

To get started with the Advanced File Distribution System, follow these steps:

1.  Clone the Repository   
   ```bash
   git clone https://github.com/RameshBabuAsh/FileTransferTally.git
   ```

2.  Create a Virtual Environment   
   Navigate to the cloned repository and create a virtual environment:
   ```bash
   cd repo-name
   python3 -m venv venv
   venv\Scripts\activate
   ```

3.  Install Dependencies   
   Install the required dependencies using the provided `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

4.  Run the Application   
   Navigate to the `src` directory and start the application:
   -  Start the Backend (Terminal 1): 

    ```bash
    cd src
    python app.py
    ```

   -  Note : Close the GUI that opens here.
   -  Start the GUI (Terminal 2): 

    ```bash
    python gui.py
    ```

##  Contributing 
Contributions are welcome! If you have suggestions or improvements, feel free to fork the repository and submit a pull request.


