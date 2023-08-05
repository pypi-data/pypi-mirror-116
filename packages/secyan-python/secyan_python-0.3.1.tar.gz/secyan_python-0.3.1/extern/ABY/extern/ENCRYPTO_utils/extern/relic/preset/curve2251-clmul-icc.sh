#!/bin/bash
cmake -DALIGN=16 -DARCH=X64 -DARITH=curve2251-sse -DCHECK=off -DFB_POLYN=251 -DFB_METHD="INTEG;INTEG;QUICK;QUICK;QUICK;QUICK;LOWER;SLIDE;QUICK" -DFB_PRECO=on -DFB_SQRTF=off -DEB_METHD="PROJC;LODAH;COMBS;INTER" -DEC_METHD="CHAR2" -DCOMP="-O3 -xSSE4.2 -unroll" -DTIMER=CYCLE -DWITH="MD;DV;BN;FB;EB;EC" -DWSIZE=64 $1
