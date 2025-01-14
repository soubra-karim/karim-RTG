# karim-RTG
study notes:https://giant-approach-db5.notion.site/SOC-Design-Study-Notes-17ae6f9f865880538b21cd7e19bab082

Course work and personal projects.


## RISC CPU (2024)–Verilog,Computer Architecture, RTL, Digital Systems,Vivado
- Implemented the RV32I instruction set using Verilog
- Utilized Harvard architecture to develop the pipelined CPU
- Developed the pipeline stages of fetch, decode, execute, memory, and write back
- Implemented stalls,forwarding and pipeline flushing to deal with pipelining hazards
- (work in progress, issue found in forwarding logic)
## 4x4 Network-On-Chip (NOC) (2024) –Systemc,Linux,SOC design,C/C++
- Connected sources and sinks in a 4x4 mesh topology using Systemc
- Utilized the Wormhole flow control technique to transfer flits throughout the network
- Implemented an XY routing algorithm to pass flits from source to destination
- Integrated components in the SC_MAIN function and tested the 4x4 NOC
## Image Edge Detection (2024) –Verilog, Vivado, RTL, Digital Systems
- Implemented buffers to store pixel data
- Implemented control data to keep track of which buffer to use
- Implemented 2D convolution (Multiply Accumulate) function for Sobel Edge detection
- Utilized Sobel Edge detection matrix to calculate edges
## MultiMedia System (2023) –C/C++, Embedded systems, Keil uVision
- Implemented an interactive media center using the MCB1700 board
- Utilized MMIO and GPIO pins on the board to accept user inputs through a joystick
- Implemented timers and interrupts to use the on board speaker
- Made us of Keil uVision built in debugger to trace code execution
- Applied scheduling techniques in order to switch between media system’s Features
## Job Recommender System Capstone (2023-2024) – Python, Machine learning,Django,Scikit-learn
- Designed and developed a hybrid recommender system using resume data
- Leverage Pandas for data cleaning, preprocessing, and cleaning
- Implemented a Django backend and React frontend.
- Utilized REST API design principles in order to employ modular API endpoints
- Utilized MYSQL DBMS to manage and store data
- Utilize Amazon AWS to host MYSQL database
## Custom PC (2024)  –  System integration, Assembly
- CPU: AMD Ryzen 5 7600 6-Core Processor
- GPU: AMD Radeon RX 7700 XT
- Motherboard: Asus TUF Gaming B650-PLUS WIFI
- RAM: 2x16 GB Corsair
- OS: Windows 11/ Linux
- Storage:  NVME WD Black SN850X 2TB, Sandisk SATA SSD 120 GB
- Heatsink: Bequiet Dark ROCK PRO 5
- Case: Corsair 4000D Airflow
- PSU:Corsair RM750 
## UVM testbench for ALU verification (2024)  –  UVM, Systemverilog
- Implemented a basic test bench using UVM 
- Implemented Sequencer, Sequence item and other test bench components and environments, as well as a top level testbench connecting everything together


## Banking project (2024) - java,encryption,networking
- Implemented a secure banking system
- uses RSA encryption in order to keep data secured
- Stores encrypted data locally and uses networking sockets to send data between bank and atm
- utilizes public/private key encryption methods

## P2P File sharing (2023) - C, networking
- utilizing TCP and UDP connections in order to facilitate file sharing between users
- P2P feature enables users to be both host and clients

