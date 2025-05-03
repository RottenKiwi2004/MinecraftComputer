ldi r7 61
ldi r1 0
loop: inc r1 r1
biz end
stm r1
jmp loop
end: hlt