.ORIG x3000
AND R0, R0, #0
ADD R0, R0, #9
NOT R1, R0
ADD R1, R1, #1
START_LOOP
    ADD R1, R1, R0
    ADD R1, R1, R0
    ADD R0, R0, #-1
    BRp START_LOOP
HALT
.END