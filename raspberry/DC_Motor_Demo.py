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
  # Copyright   [DFRobot](http://www.dfrobot.com), 2016
  # Copyright   GNU Lesser General Public License
  #
  # version  V1.0
  # date  2017-10-9
'''

import time

from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board

board = Board(1, 0x10)    # Select bus 1, set address to 0x10

def board_detect():
  l = board.detecte()
  print("Board list conform:")
  print(l)

def print_board_status(status):
  if status == board.sta_ok:
    print("board status: everything ok")
  elif status == board.sta_err:
    print("board status: unexpected error")
  elif status == board.sta_err_device_not_detected:
    print("board status: device not detected")
  elif status == board.sta_err_parameter:
    print("board status: parameter error")
  elif status == board.sta_err_soft_verion:
    print("board status: unsupport board framware version")

if __name__ == "__main__":

  board_detect()    # If you forget address you had set, use this to detected them, must have class instance

  while board.begin() != board.sta_ok:    # Board begin and check board status
    print_board_status(board.last_operate_status)
    print("board begin faild")
    time.sleep(2)
  print("board begin success")

  # board.set_addr(0x20)    # Set board controler address, use it carefully

  board.set_encoder_enable(1)               # Set selected DC motor encoder enable
  # board.set_encoder_disable(1)            # Set selected DC motor encoder disable
  board.set_encoder_reduction_ratio(1, 1)   # Set selected DC motor encoder reduction ratio

  board.set_moter_pwm_frequency(500)    # Set DC motor pwm frequency to 500HZ

  time.sleep(0.1)   # wait for config done, avoid unexpect movement

  while True:
    for i in range(11, 99, 10):   # slow to fast
      board.motor_movement(1, board.cw, i)   # DC motor 1 movement, orientation clockwise, pwm duty i
      time.sleep(1)
      speed = board.get_encoder_speed(1)
      print("motor 1 encoder speed: %d rpm, duty: %d" %(speed, i))

    for i in range(99, 11, -10):    # fast to slow
      board.motor_movement(1, board.cw, i)   # DC motor 1 movement, orientation clockwise, pwm duty i
      time.sleep(1)
      speed = board.get_encoder_speed(1)
      print("motor 1 encoder speed: %d rpm, duty: %d" %(speed, i))

    print("stop all motor")
    board.motor_stop(board.all)   # stop all DC motor
    time.sleep(4)
