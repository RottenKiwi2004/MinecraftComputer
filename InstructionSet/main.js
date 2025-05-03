let instruction = 0;
let previousInstruction = 0;

document.querySelectorAll('th > button').forEach(e=>{
    e.addEventListener('click', function(){
        previousInstruction = instruction;
        console.log(e.id);
        let bit = parseInt(e.id.substring(3));
        instruction ^= (1 << bit);
        let num = e.textContent;
        num = 1 - parseInt(num);
        e.textContent = num;
        setTimeout(() => {
            e.style.animation = 'none';
        }, 1000);
        e.style.animation = 'flash 1s forwards';
        decodeInstruction();
    })
})

function getSignedNumFormat8Bit(num) {
    num &= 0xff;
    return num < 128 ? num : num - 256;
}

function getOpCode(instruction) {
    let opcode = (instruction & 0xf000) >> 12;
    return opcode;
}

function getRd() {
    let r = (instruction & 0x0e00) >> 9;
    return r;
}

function getRa() {
    let r = (instruction & 0x0038) >> 3;
    return r;
}

function getRb() {
    let r = (instruction & 0x0007);
    return r;
}

function get8bit() {
    let r = instruction & 0x00ff;
    return r;
}

const instSymbols = document.querySelector('#instructionsymbol');

function set3Bits() {
    for(let i=0; i<3; i++) {
        instruction |= 7;
        let el = document.querySelector(`#bit${i}`);
        el.textContent = 1;
    }
}

function clear3Bits() {
    for(let i=0; i<3; i++) {
        instruction &= ~7;
        let el = document.querySelector(`#bit${i}`);
        el.textContent = 0;
    }
}


function decodeInstruction() {
    let opcode = getOpCode(instruction);


    for(let i=0; i<16; i++){
        let el = document.querySelector(`#inst${i}`);
        if (opcode == i) {
            el.classList.add("active");
        }
        else {
            el.classList.remove("active");
        }
    }

    let instructionString = "";

    // Handle R7 of LDM, STM
    let previousOpcode = getOpCode(previousInstruction);
    if (previousOpcode != opcode && (previousOpcode == 0b0011 || previousOpcode == 0b0100) ) {
        clear3Bits();
    }
    
    switch (opcode) {
        case 0b0000: instructionString = "NOP (No Operation)";                      break;
        case 0b0001: instructionString = "HLT (Halt)";                              break;
        case 0b0010: instructionString = `R${getRd()} <- ${get8bit()}`;             break;
        case 0b0011: instructionString = `R${getRd()} <- M[R7]`; set3Bits();        break;
        case 0b0100: instructionString = `M[R7] <- R${getRa()}`; set3Bits();        break;
        case 0b0101: instructionString = `PC <- ${get8bit()}`;                      break;
        case 0b0110: instructionString = `PC <- ${get8bit()} if N = 1`;             break;
        case 0b0111: instructionString = `PC <- ${get8bit()} if Z = 1`;             break;
        case 0b1000: instructionString = `R${getRd()} <- R${getRa()} + R${getRb()}`;break;
        case 0b1001: instructionString = `R${getRd()} <- R${getRa()} - R${getRb()}`;break;
        case 0b1010: instructionString = `R${getRd()} <- R${getRa()} | R${getRb()}`;break;
        case 0b1011: instructionString = `R${getRd()} <- R${getRa()} & R${getRb()}`;break;
        case 0b1100: instructionString = `R${getRd()} <- R${getRa()} ^ R${getRb()}`;break;
        case 0b1101: instructionString = `R${getRd()} <- R${getRa()} + 1`;          break;
        case 0b1110: instructionString = `R${getRd()} <- R${getRa()} - 1`;          break;
        case 0b1111: instructionString = `R${getRd()} <- R${getRa()} >> 1`;         break;
    }
    instSymbols.textContent = instructionString;
}