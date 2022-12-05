# CAN_27930_Decode
To decode the message log file between the EV Charger and BMS with GB/T 27930-2015 standard. The source file here is logged and exported via the CANalyzer 12.0 in .asc format.

While using CANalyer I find the Database file is not well written and some of the info is missing. Then I started to learn the communication protocal GB/T 27930-2015 and prepare the this simple script to help to decode the important information during charging.

Basically you just need to export your asc file from CANalyer and run with the main.py following information will be exported:
Time,U_Req,I_Req,U_CCS,I_CCS,U_BCS,I_BCS,Max_T[C],SOC,Time_Charged[min]
