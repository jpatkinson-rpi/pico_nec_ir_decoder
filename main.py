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

from machine import Pin
from machine import Timer, Pin
from time import sleep
import time
import array

NEC_DATA_BITS = 32
NEC_DATA_BYTES = 4

# Start of Frame 13.5ms pulse
NEC_START_TIME_LOW  = 13500-500  
NEC_START_TIME_HIGH = 13500+500

# '0' 1.25ms pulse
NEC_ZERO_TIME_LOW  = 1125-125  
NEC_ZERO_TIME_HIGH = 1125+125

# '1' 2.25ms pulse
NEC_ONE_TIME_LOW  = 2250-125
NEC_ONE_TIME_HIGH = 2250+125

nec_ir_bits = [ 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80 ] 

nec_byte_values = array.array('i', (0 for _ in range(NEC_DATA_BYTES)))

nec_data_bit = 0   # Data bit counter
nec_data_byte = 0  # Data byte counter

last_timer_count = 0 # previous event time

# flags to indicate start/end of NEC IR sequence
nec_ir_seq_start = False
nec_ir_seq_end = False

# Uses GPIO 15 for IR sensor input
gpio_irq = Pin(15, mode=Pin.IN, pull=Pin.PULL_UP)


######################################################################
# interrupt routine for IR input
######################################################################
def irq_triggered(pin):
   global nec_data_bit, nec_data_byte
   global last_timer_count
   global nec_ir_seq_start, nec_ir_seq_end

   flags = pin.irq().flags()
   timer_count = time.ticks_us()
   timer_diff = timer_count - last_timer_count
   
   if nec_ir_seq_end == False:  
      if nec_ir_seq_start == False:
         if timer_diff > NEC_START_TIME_LOW and timer_diff < NEC_START_TIME_HIGH:
            nec_ir_seq_start = True
            nec_ir_seq_end = False
            nec_data_bit = 0
            nec_data_byte = 0
            for i in range(NEC_DATA_BYTES):
               nec_byte_values[i] = 0      
 
      else:
         if nec_data_bit < NEC_DATA_BITS:
            if timer_diff > NEC_ZERO_TIME_LOW and timer_diff < NEC_ZERO_TIME_HIGH:
               nec_byte_values[ nec_data_byte ] += 0
            elif timer_diff > NEC_ONE_TIME_LOW and timer_diff < NEC_ONE_TIME_HIGH:
               nec_byte_values[ nec_data_byte ] += nec_ir_bits[ nec_data_bit % 8 ]
            else:
               nec_ir_seq_start = False
               nec_data_bit = 0

            nec_data_bit += 1
            if nec_data_bit % 8 == 0:
               nec_data_byte += 1
            if nec_data_bit == NEC_DATA_BITS:
               nec_ir_seq_end = True
               nec_ir_seq_start = False
            
   last_timer_count=timer_count


######################################################################
# main program body
######################################################################
if __name__ == "__main__":

   gpio_irq.irq(handler=irq_triggered, trigger=Pin.IRQ_FALLING)

   while True:
      if nec_ir_seq_end == True:
         print("0x{:02x} 0x{:02x} 0x{:02x} 0x{:02x}".format(nec_byte_values[0], nec_byte_values[1], nec_byte_values[2], nec_byte_values[3]))
         sleep(0.2)
         nec_ir_seq_end = False


