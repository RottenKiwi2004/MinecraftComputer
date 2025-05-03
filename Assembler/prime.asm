ldi r1 2        ; Current number
ldi r2 100      ; Last number
ldi r6 0x00     ; Pointer copy
ldi r7 0x00     ; Pointer
stm r1          ; Store 2 as first prime
ldi r7 61       ; Display address
stm r1          ; Display first prime
loop:       inc r1 r1       ; Increment to next number
            sub r5 r2 r1    ; Check if last number reached
            biz end         ; If yes, end program
            ldi r7 0x00     ; Set pointer to first prime
setup:      add r3 r1 r0    ; Copy r3 <- r1
            ldm r4          ; Get prime to check divisibility
divide:     sub r3 r3 r4    ; Subtract loop
            biz loop        ; If reaches zero, divisible (not prime)
            bin nextPrime   ; If turns negative,not divisible
            jmp divide      ; Otherwise, continue subtracting
nextPrime:  inc r7 r7       ; Move pointer
            sub r0 r6 r7    ; Check size of all prime before number
            bin isPrime     ; If negative, this number is prime
            jmp setup       ; Reset number for next division
isPrime:    stm r1          ; Store current number to prime list
            inc r6 r6       ; Increment size of prime list
            ldi r7 61       ; Display address
            stm r1          ; Display new prime
            jmp loop        ; Go to next number
end:        hlt