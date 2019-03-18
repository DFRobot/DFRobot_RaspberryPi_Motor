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
* [Compatibility](#compatibility)
* [Credits](#credits)

## Summary

DC Motors driver.

## Feature

1. Two DC motors with encoder control. <br>
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

  ''' Board status '''
  sta_ok = 0x00
  sta_err = 0x01
  sta_err_device_not_detected = 0x02
  sta_err_soft_verion = 0x03
  sta_err_parameter = 0x04

  ''' last operate status '''
  last_operate_status = sta_ok

  ''' Orientation '''
  cw = 0x01
  ccw = 0x02
  all = 0xff

  def begin(self):
    '''
      @brief    Board begin

      @return   Board status
    '''

  def set_addr(self, addr):
    '''
      @brief    Set board controler address

      @param address    Address to set, range in 1 to 127
    '''

  def set_encoder_enable(self, id):
    '''
      @brief    Set dc motor encoder enable

      @param id: int    Encoder id, in range 1 to 2
    '''
  
  def set_encoder_disable(self, id):
    '''
      @brief    Set dc motor encoder disable

      @param id: int   Encoder id, in range 1 to 2
    '''

  def set_encoder_reduction_ratio(self, id, reduction_ratio):
    '''
      @brief    Set dc motor encoder reduction ratio

      @param id: int                 Encoder id, in range 1 to 2
      @param reduction_ratio: int    Set dc motor encoder reduction ratio, range in 1 to 2000, (pulse per circle) = 16 * reduction_ratio * 2
    '''

  def get_encoder_speed(self, id):
    '''
      @brief    Get dc motor encoder speed, unit rpm

      @param id: int   Encoder id, in range 1 to 2
    '''

  def set_moter_pwm_frequency(self, frequency):
    '''
      @brief    Set dc motor pwm frequency

      @param frequency: int    Frequency to set, in range 50HZ to 12750HZ, (actual frequency) = frequency - (frequency % 50)
    '''

  def motor_movement(self, id, orientation, speed):
    '''
      @brief    Motor movement

      @param id: int             Motor id to move
      @param orientation: int    Motor orientation, this.cw (clockwise) or this.ccw (counterclockwise)
      @param speed: float        Motor pwm duty cycle, in range 1.1 to 99.9
    '''

  def motor_stop(self, id):
    '''
      @brief    Motor stop

      @param int    Motor id to stop, use this.all to stop all motors
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
