#include <stdio.h>
#include <stdint.h>

/* Syntax:
        InputArr         : Input compression data.
        K_array          : Setting K value of compression array.
        numDeCompbits    : Number of bit per sample.
        numSamplesPerBlock : Number of total data per block.
        CompressionRatio : Compression ratio.*/
void EGE_Decompression_16bit (uint16_t *InputArr, uint32_t InputArrSize, int16_t *OutputArr, uint8_t *K_array, uint8_t numSamplesPerBlock, uint16_t* bit) {
    uint8_t K_Value = 0;
    uint8_t ScaleFactorBW = 0;
    
    uint16_t idx = 0;
    uint8_t RawBit;
    uint8_t K_idx = 0;
    uint8_t Startbit = 7;
    uint8_t PollingIdx;
    uint16_t chkbit = 1;
    uint8_t n_extra = 0;
    uint8_t numSearchBit = 0;
    uint8_t Lock = 0;
    uint8_t bitVal = 0;
    uint16_t SampleCnt = 0;
    int16_t TempVal;
    /* Define K value in this block */
    RawBit = InputArr[0] & 0b111;
    K_idx |= (RawBit & 0x1) << 2;
    K_idx |= (RawBit & 0x4) >> 2;
    K_Value = K_array[K_idx];

    /* Define scale factor bit width in this block */
    RawBit = (InputArr[0] & 0b1111000) >> 3;
    ScaleFactorBW |= (RawBit & 0x1) << 3;
    ScaleFactorBW |= (RawBit & 0x2) << 1;
    ScaleFactorBW |= (RawBit & 0x4) >> 1;
    ScaleFactorBW |= (RawBit & 0x8) >> 3;
    uint8_t t =0;
    TempVal = 0;
    for ( idx = 0; idx < InputArrSize; idx++ ) {
        for (PollingIdx = Startbit; PollingIdx < 16; PollingIdx++){
            chkbit = 1 << PollingIdx;
            bitVal = (InputArr[idx] & chkbit) == chkbit;
            
            /* Searching stage */
            if (Lock == 0){
                if (bitVal == 1){ /* bit value is 1 */
                    Lock = 2;
                    numSearchBit = n_extra + K_Value - ScaleFactorBW + 1;
                }
                else{ /* bit value is 0 */
                    n_extra++;
                }
            }
            /* Accumlation stage */
            if (Lock > 0){
                if (numSearchBit>0){
                    numSearchBit--;
                    
                    TempVal = (TempVal<<1) + bitVal;
                    if (Lock == 2)
                        Lock--;
                }
                else{ /* Save decompression value */
                    OutputArr[SampleCnt] = (TempVal<<ScaleFactorBW) - (1<<K_Value);
                    if(bitVal == 1){
                        OutputArr[SampleCnt] = OutputArr[SampleCnt] * (-1);
                    }
                    Lock--;
                    SampleCnt++;
                    if (SampleCnt == numSamplesPerBlock)
                        return;
                    TempVal = 0;
                    n_extra = 0;
                }
            }
        }
        chkbit = 1;
        Startbit = 0;
    }
}

