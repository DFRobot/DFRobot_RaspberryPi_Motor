# DFRobot DC Motor Driver HAT

This RaspberryPi motor-driving board can communicate with RaspberryPi via IIC. <br>
It can control the motor to rotate forward and reserve, and rotation speed. <br>
The control command is IIC command and the drive command is PWM signal. <br>
The single-channel maximum operate current is 1.2A. The input port is compatible with GPIO port. <br>
With 2 independent output channels and 2 encoder ports, it can control 2 DC-motors or 2 motors with encoder. <br>
Application: RaspberryPi smart car, DIY tank, DIY micro-fish... <br>

## DFRobot DC Motor Driver HAT Library for RaspberryPi

Provide a Raspberry Pi library for the DC Motor Driver HAT modules.

## Table of Contents

* [Summary](#summary)
* [Feature](#feature)
* [Installation](#installation)
* [Methods](#methods)
* [Credits](#credits)

## Summary

DC Motors driver.

## Feature

1. Two DC motors with encoder control or normal DC motors. <br>
2. Get motors speed form encoder. <br>
3. PWM frequency set. <br>
4. PWM duty set. <br>

## Installation

This Sensor should work with DFRobot_RaspberryPi_DC_Motor on RaspberryPi. <br>
Run the program:

```
$> python2 DC_Motor_Demo.py
```

## Methods

```py

class DFRobot_DC_Motor:

  ''' Enum motor ID '''
  M1 = 0x01
  M2 = 0x02
  
  ''' Board status '''
  STA_OK = 0x00
  STA_ERR = 0x01
  STA_ERR_DEVICE_NOT_DETECTED = 0x02
  STA_ERR_SOFT_VERSION = 0x03
  STA_ERR_PARAMETER = 0x04

  ''' last operate status, users can use this variable to determine the result of a function call. '''
  last_operate_status = STA_OK

  ''' Orientation and global variables '''
  CW = 0x01     # clockwise
  CCW = 0x02    # countclockwise
  STOP = 0x05
  ALL = 0xffffffff

  def begin(self):
    '''
      @brief    Board begin
      @return   Board status
    '''

  def set_addr(self, addr):
    '''
      @brief    Set board controler address, reboot module to make it effective
      @param address: int    Address to set, range in 1 to 127
    '''

  def set_encoder_enable(self, id):
    '''
      @brief    Set dc motor encoder enable
      @param id: list   Encoder list, items in range 1 to 2, or id = self.ALL
    '''
  
  def set_encoder_disable(self, id):
    '''
      @brief    Set dc motor encoder disable

      @param id: list   Encoder list, items in range 1 to 2, or id = self.ALL
    '''

  def set_encoder_reduction_ratio(self, id, reduction_ratio):
    '''
      @brief    Set dc motor encoder reduction ratio
      @param id: list                 Encoder list, items in range 1 to 2, or id = self.ALL
      @param reduction_ratio: int     Set dc motor encoder reduction ratio, range in 1 to 2000, (pulse per circle) = 16 * reduction_ratio * 2
    '''

  def get_encoder_speed(self, id):
    '''
      @brief    Get dc motor encoder speed, unit rpm
      @param id: list   Encoder list, items in range 1 to 2, or id = self.ALL
      @return :list     List of encoders speed
    '''

  def set_moter_pwm_frequency(self, frequency):
    '''
      @brief    Set dc motor pwm frequency
      @param frequency: int    Frequency to set, in range 100HZ to 12750HZ, otherwise no effective (actual frequency) = frequency - (frequency % 50)
    '''

  def motor_movement(self, id, orientation, speed):
    '''
      @brief    Motor movement
      @param id: list             Motor list, items in range 1 to 2, or id = self.ALL
      @param orientation: int     Motor orientation, self.CW (clockwise) or self.CCW (counterclockwise)
      @param speed: float         Motor pwm duty cycle, in range 0 to 100, otherwise no effective
    '''

  def motor_stop(self, id):
    '''
      @brief    Motor stop
      @param id: list   Motor list, items in range 1 to 2, or id = self.ALL
    '''

  def detecte(self):
    '''
      @brief    If you forget address you had set, use this to detecte them, must have class instance
      @return   Board list conformed
    '''

class DFRobot_DC_Motor_IIC(DFRobot_DC_Motor):

  def __init__(self, bus_id, addr):
    '''
      @param bus_id: int   Which bus to operate
      @oaram addr: int     Board controler address
    '''

```

## Credits

·author [Frank jiehan.guo@dfrobot.com]
