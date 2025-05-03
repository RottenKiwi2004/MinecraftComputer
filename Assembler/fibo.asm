ldi r1 0
ldi r2 1
ldi r4 11               ; Number of iterations
ldi r7 61               ; Display address
loop:   add r3 r1 r2
        stm r3          ; Write to display
        add r1 r2 r0    ; Move r1 <- r2
        add r2 r3 r0    ; Move r2 <- r3
        dec r4 r4
        biz end         ; Number of iterations reached
        jmp loop
end:    hlt

; Fibo sequence
; 0 1 1 2 3 5 8 13 21 34 55 89 144 233