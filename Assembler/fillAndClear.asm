ldi r1 0
loop:   ldi r7 63
        stm r1
        inc r1 r1
        biz next
        jmp loop
next:   ldi r1 0
loop2:  ldi r7 62
        stm r1
        inc r1 r1
        biz end
        jmp loop2
end: hlt