#-------------------------------------------------------------------
# NEC format IR decoder for RPi PICO
#
# Uses GPIO 15 for IR sensor input
#
# NEC format:
#    start bit      - 13.5ms pulse
#    8-bit address  - 0 = 1.25ms pulse : 1 = 2.25ms pulse
#    8-bit ~address - 0 = 1.25ms pulse : 1 = 2.25ms pulse
#    8-bit data     - 0 = 1.25ms pulse : 1 = 2.25ms pulse
#    8-bit ~data    - 0 = 1.25ms pulse : 1 = 2.25ms pulse
#-------------------------------------------------------------------

![Alt text](https://github.com/jpatkinson-rpi/pico_nec_ir_decoder/blob/main/images/NEC_format_IR.png?raw=true "NEC format IR")
