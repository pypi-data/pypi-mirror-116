#!/bin/bash
CC=avr-gcc CXX=c++ LINK="-mmcu=atmega128 -Wl,-gc-sections" COMP="-O2 -ggdb -Wa,-mmcu=atmega128 -mmcu=atmega128 -ffunction-sections -fdata-sections" cmake -DARCH=AVR -DWSIZE=8 -DOPSYS= -DSEED=LIBC -DSHLIB=OFF -DSTBIN=ON -DTIMER= -DWITH="DV;MD;BN;FP;FPX;EP;EC;PP;PC" -DBENCH=20 -DTESTS=20 -DCHECK=off -DVERBS=off -DSTRIP=on -DQUIET=on -DARITH=avr-asm-158 -DFP_PRIME=158 -DBN_METHD="COMBA;COMBA;MONTY;BASIC;STEIN;BASIC" -DFP_QNRES=off -DFP_METHD="INTEG;COMBA;COMBA;MONTY;MONTY;SLIDE" -DBN_PRECI=160 -DBN_MAGNI=DOUBLE -DEP_PRECO=off -DEP_METHD="PROJC;LWNAF;LWNAF;BASIC" -DEP_ENDOM=on -DEP_PLAIN=on -DEC_METHD="PRIME" -DFPX_METHD="INTEG;INTEG;BASIC" -DPP_METHD="BASIC;OATEP" -DRAND=FIPS -DSEED=LIBC -DMD_METHD=SHONE $1
