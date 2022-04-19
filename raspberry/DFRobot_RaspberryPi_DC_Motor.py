# -*- coding:utf-8 -*-

'''
 MIT License

 Copyright (C) <2019> <@DFRobot Frank>

　Permission is hereby granted, free of charge, to any person obtaining a copy of this
　software and associated documentation files (the "Software"), to deal in the Software
　without restriction, including without limitation the rights to use, copy, modify,
　merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
　permit persons to whom the Software is furnished to do so.

　The above copyright notice and this permission notice shall be included in all copies or
　substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
 FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import time

class DFRobot_DC_Motor:

  _STEPPER_COUNT = 1
  _MOTOR_COUNT = 2

  _REG_SLAVE_ADDR = 0x00
  _REG_PID = 0x01
  _REG_PVD = 0x02
  _REG_CTRL_MODE = 0x03
  _REG_ENCODER1_EN = 0x04
  _REG_ENCODER1_SPPED = 0x05
  _REG_ENCODER1_REDUCTION_RATIO = 0x07
  _REG_ENCODER2_EN = 0x09
  _REG_ENCODER2_SPEED = 0x0a
  _REG_ENCODER2_REDUCTION_RATIO = 0x0c
  _REG_MOTOR_PWM = 0x0e
  _REG_MOTOR1_ORIENTATION = 0x0f
  _REG_MOTOR1_SPEED = 0x10
  _REG_MOTOR2_ORIENTATION = 0x12
  _REG_MOTOR2_SPEED = 0x13

  _REG_DEF_PID = 0xdf
  _REG_DEF_VID = 0x10

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

  ''' Board control mode '''
  _control_mode_dc_motor = 0x00
  _control_mode_stepper = 0x01

  ''' Orientation and global variables '''
  CW = 0x01     # clockwise
  CCW = 0x02    # countclockwise
  STOP = 0x05
  ALL = 0xffffffff
  
  def _write_bytes(self, reg, buf):
    pass
  
  def _read_bytes(self, reg, len):
    pass

  def __init__(self, addr):
    self._addr = addr

  def begin(self):
    '''
      @brief    Board begin
      @return   Board status
    '''
    pid = self._read_bytes(self._REG_PID, 1)
    vid = self._read_bytes(self._REG_PVD, 1)
    if self.last_operate_status == self.STA_OK:
      if pid[0] != self._REG_DEF_PID:
        self.last_operate_status = self.STA_ERR_DEVICE_NOT_DETECTED
      else:
        self._set_control_mode(self._control_mode_dc_motor)
        self.motor_stop(self.ALL)
        self.set_encoder_disable(self.ALL)
    return self.last_operate_status

  def set_addr(self, addr):
    '''
      @brief    Set board controler address, reboot module to make it effective
      @param address: int    Address to set, range in 1 to 127
    '''
    if addr < 1 or addr > 127:
      self.last_operate_status = self.STA_ERR_PARAMETER
      return
    self._write_bytes(self._REG_SLAVE_ADDR, [addr])

  def _set_control_mode(self, mode):
    self._write_bytes(self._REG_CTRL_MODE, [mode])

  def _parse_id(self, id):
    if id == self.ALL:
      return range(1, self._MOTOR_COUNT + 1)
    for i in id:
      if i < 1 or i > self._MOTOR_COUNT:
        self.last_operate_status = self.STA_ERR_PARAMETER
        return []
    return id

  def set_encoder_enable(self, id):
    '''
      @brief    Set dc motor encoder enable
      @param id: list   Encoder list, items in range 1 to 2, or id = self.ALL
    '''
    for i in self._parse_id(id):
      self._write_bytes(self._REG_ENCODER1_EN + 5 * (i - 1), [0x01])
  
  def set_encoder_disable(self, id):
    '''
      @brief    Set dc motor encoder disable

      @param id: list   Encoder list, items in range 1 to 2, or id = self.ALL
    '''
    for i in self._parse_id(id):
      self._write_bytes(self._REG_ENCODER1_EN + 5 * (i - 1), [0x00])

  def set_encoder_reduction_ratio(self, id, reduction_ratio):
    '''
      @brief    Set dc motor encoder reduction ratio
      @param id: list                 Encoder list, items in range 1 to 2, or id = self.ALL
      @param reduction_ratio: int     Set dc motor encoder reduction ratio, range in 1 to 2000, (pulse per circle) = 16 * reduction_ratio * 2
    '''
    reduction_ratio = int(reduction_ratio)
    if reduction_ratio < 1 or reduction_ratio > 2000:
      self.last_operate_status = self.STA_ERR_PARAMETER
      return
    for i in self._parse_id(id):
      self._write_bytes(self._REG_ENCODER1_REDUCTION_RATIO + 5 * (i - 1), [reduction_ratio >> 8, reduction_ratio & 0xff])

  def get_encoder_speed(self, id):
    '''
      @brief    Get dc motor encoder speed, unit rpm
      @param id: list   Encoder list, items in range 1 to 2, or id = self.ALL
      @return :list     List of encoders speed
    '''
    l = []
    for i in self._parse_id(id):
      rslt = self._read_bytes(self._REG_ENCODER1_SPPED + 5 * (i - 1), 2)
      s = (rslt[0] << 8) | rslt[1]
      if s & 0x8000:
        s = - (0x10000 - s)
      l.append(s)
    return l

  def set_moter_pwm_frequency(self, frequency):
    '''
      @brief    Set dc motor pwm frequency
      @param frequency: int    Frequency to set, in range 100HZ to 12750HZ, otherwise no effective (actual frequency) = frequency - (frequency % 50)
    '''
    if frequency < 100 or frequency > 12750:
      self.last_operate_status = self.STA_ERR_PARAMETER
      return
    frequency = int(frequency / 50)
    self._write_bytes(self._REG_MOTOR_PWM, [frequency])
    time.sleep(0.1)

  def motor_movement(self, id, orientation, speed):
    '''
      @brief    Motor movement
      @param id: list             Motor list, items in range 1 to 2, or id = self.ALL
      @param orientation: int     Motor orientation, self.CW (clockwise) or self.CCW (counterclockwise)
      @param speed: float         Motor pwm duty cycle, in range 0 to 100, otherwise no effective
    '''
    if orientation != self.CW and orientation != self.CCW:
      self.last_operate_status = self.STA_ERR_PARAMETER
      return
    if speed > 100.0 or speed < 0.0:
      self.last_operate_status = self.STA_ERR_PARAMETER
      return
    for i in self._parse_id(id):
      reg = self._REG_MOTOR1_ORIENTATION + (i - 1) * 3
      self._write_bytes(reg, [orientation])
      self._write_bytes(reg + 1, [int(speed), int((speed * 10) % 10)])

  def motor_stop(self, id):
    '''
      @brief    Motor stop
      @param id: list   Motor list, items in range 1 to 2, or id = self.ALL
    '''
    for i in self._parse_id(id):
      self._write_bytes(self._REG_MOTOR1_ORIENTATION + 3 * (i - 1), [self.STOP])

  def detecte(self):
    '''
      @brief    If you forget address you had set, use this to detecte them, must have class instance
      @return   Board list conformed
    '''
    l = []
    back = self._addr
    for i in range(1, 127):
      self._addr = i
      if self.begin() == self.STA_OK:
        l.append(i)
    for i in range(0, len(l)):
      l[i] = hex(l[i])
    self._addr = back
    self.last_operate_status = self.STA_OK
    return l

import smbus

class DFRobot_DC_Motor_IIC(DFRobot_DC_Motor):

  def __init__(self, bus_id, addr):
    '''
      @param bus_id: int   Which bus to operate
      @oaram addr: int     Board controler address
    '''
    self._bus = smbus.SMBus(bus_id)
    DFRobot_DC_Motor.__init__(self, addr)

  def _write_bytes(self, reg, buf):
    self.last_operate_status = self.STA_ERR_DEVICE_NOT_DETECTED
    # print("write byte: ", hex(reg), buf)
    try:
      self._bus.write_i2c_block_data(self._addr, reg, buf)
      self.last_operate_status = self.STA_OK
    except:
      pass

  def _read_bytes(self, reg, len):
    self.last_operate_status = self.STA_ERR_DEVICE_NOT_DETECTED
    try:
      rslt = self._bus.read_i2c_block_data(self._addr, reg, len)
      self.last_operate_status = self.STA_OK
      return rslt
    except:
      return [0] * len
