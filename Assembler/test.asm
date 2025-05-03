ldi r1 0
ldi r2 0
ldi r4 12
fibo: add r3 r1 r2 ; r3 <- r1 + r2
add r1 r2 r0 ; move data from r2 to r1
add r2 r3 r0 ; move data from r3 to r2
dec r4 r4    ; iterate number of rounds
bin stop
jmp fibo
stop: hlt