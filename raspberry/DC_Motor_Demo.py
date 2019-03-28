# -*- coding:utf-8 -*-

'''
  # DC_Motor_Demo.py
  #
  # Connect board with raspberryPi.
  # Make board power and motor connection correct.
  # Run this demo.
  #
  # Motor on connector 1 will move slow to fast, then fast to stop. loop in few seconds.
  # Motor speed will print on terminal
  #
  # test motor: https://www.dfrobot.com/product-634.html
  #
  # Copyright   [DFRobot](http://www.dfrobot.com), 2016
  # Copyright   GNU Lesser General Public License
  #
  # version  V1.0
  # date  2019-3-26
'''

import time

from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board

board = Board(1, 0x10)    # Select bus 1, set address to 0x10

def board_detect():
  l = board.detecte()
  print("Board list conform:")
  print(l)

''' print last operate status, users can use this variable to determine the result of a function call. '''
def print_board_status():
  if board.last_operate_status == board.STA_OK:
    print("board status: everything ok")
  elif board.last_operate_status == board.STA_ERR:
    print("board status: unexpected error")
  elif board.last_operate_status == board.STA_ERR_DEVICE_NOT_DETECTED:
    print("board status: device not detected")
  elif board.last_operate_status == board.STA_ERR_PARAMETER:
    print("board status: parameter error, last operate no effective")
  elif board.last_operate_status == board.STA_ERR_SOFT_VERSION:
    print("board status: unsupport board framware version")

if __name__ == "__main__":

  board_detect()    # If you forget address you had set, use this to detected them, must have class instance

  # Set board controler address, use it carefully, reboot module to make it effective
  '''
  board.set_addr(0x10)
  if board.last_operate_status != board.STA_OK:
    print("set board address faild")
  else:
    print("set board address success")
  '''

  while board.begin() != board.STA_OK:    # Board begin and check board status
    print_board_status()
    print("board begin faild")
    time.sleep(2)
  print("board begin success")

  board.set_encoder_enable(board.ALL)                 # Set selected DC motor encoder enable
  # board.set_encoder_disable(board.ALL)              # Set selected DC motor encoder disable
  board.set_encoder_reduction_ratio(board.ALL, 43)    # Set selected DC motor encoder reduction ratio, test motor reduction ratio is 43.8

  board.set_moter_pwm_frequency(500)    # Set DC motor pwm frequency to 500H

  while True:
    for i in range(5, 95, 10):   # slow to fast
      board.motor_movement(board.ALL, board.CW, i)    # DC motor 1 movement, orientation clockwise, pwm duty i
      time.sleep(1)
      speed = board.get_encoder_speed(board.ALL)      # Use boadrd.all to get all encoders speed
      print("duty: %d, motor 1 encoder speed: %d rpm, motor 2 encoder speed %d rpm" %(i, speed[0], speed[1]))

    for i in range(95, 5, -10):    # fast to slow
      board.motor_movement([1, 2], board.CW, i)       # DC motor 1 movement, orientation clockwise, pwm duty i
      time.sleep(1)
      speed = board.get_encoder_speed([1, 2])         # Use list to get all encoders speed
      print("duty: %d, motor 1 encoder speed: %d rpm, motor 2 encoder speed %d rpm" %(i, speed[0], speed[1]))

    print("stop all motor")
    board.motor_stop(board.ALL)   # stop all DC motor
    print_board_status()
    time.sleep(4)
