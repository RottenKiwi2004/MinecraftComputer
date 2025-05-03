ldi r1 0x5a     ; Initial position
ldi r2 0xf0     ; Velocity Y
ldi r3 0x0f     ; Velocity X
ldi r4 0xf0     ; Mask Y
loop:   and r5 r1 r4    ; Get Y coord
        xor r0 r5 r0    ; Test if Y == 0
        biz top         ; If hit top edge
        jmp c1          ; Else proceed to check bottom edge
top:    ldi r2 0x10     ; Change Velocity Y to 1
        jmp c2          ; Jump to move Y coord
c1:     xor r0 r5 r4    ; Test if Y == 15
        biz bottom      ; If xor with 0xf0 == 0, then bottom
        jmp c2          ; Jump to move Y coord
bottom: ldi r2 0xf0     ; Change Velocity Y to -1
c2:     add r5 r5 r2    ; Move Y coord
x:      ldi r4 0x0f     ; Mask X
        and r6 r1 r4    ; Get X coord
        xor r0 r6 r0    ; Test if X == 0
        biz left        ; If hit left edge
        jmp c3          ; Else proceed to check right edge
left:   ldi r3 0x01     ; Change Velocity X to 1
        jmp c4          ; Jump to move X coord
c3:     xor r0 r6 r4    ; Test if X == 15
        biz right       ; If hit right edge
        jmp c4          ; Jump to move X coord
right:  ldi r3 0x0f     ; Change Velocity X to -1
c4:     add r6 r6 r3    ; Move X coord
merge:  and r6 r6 r4    ; Get only X component
        ldi r4 0xf0     ; Mask Y
        and r5 r5 r4    ; Get only Y component
        or r5 r5 r6     ; Merge X and Y coord
        ldi r7 63       ; Set pixel address
        stm r5          ; Set new pixel
        ldi r7 62       ; Clear pixel address
        stm r1          ; Clear old pixel
        add r1 r5 r0    ; Move r1 <- r5
        jmp loop        ; Back to main loop
