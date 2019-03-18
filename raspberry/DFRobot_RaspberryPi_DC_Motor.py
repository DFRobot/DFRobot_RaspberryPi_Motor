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

class DFRobot_DC_Motor:

  _stepper_count = 1
  _motor_count = 2

  _reg_slave_addr = 0x00
  _reg_pid = 0x01
  _reg_vid = 0x02
  _reg_control_mode = 0x03
  _reg_encoder1_enable = 0x04
  _reg_encoder1_speed = 0x05
  _reg_encoder1_reduction_ratio = 0x07
  _reg_encoder2_enable = 0x09
  _reg_encoder2_speed = 0x0a
  _reg_encoder2_reduction_ratio = 0x0c
  _reg_motor_pwm = 0x0e
  _reg_motor1_orientation = 0x0f
  _reg_motor1_speed = 0x10
  _reg_motor2_orientation = 0x12
  _reg_motor2_speed = 0x13

  _reg_def_pid = 0xdf
  _reg_def_vid = 0x01

  ''' Board status '''
  sta_ok = 0x00
  sta_err = 0x01
  sta_err_device_not_detected = 0x02
  sta_err_soft_verion = 0x03
  sta_err_parameter = 0x04

  ''' last operate status '''
  last_operate_status = sta_ok

  ''' Board control mode '''
  _control_mode_dc_motor = 0x00
  _control_mode_stepper = 0x01

  ''' Orientation '''
  cw = 0x01
  ccw = 0x02
  stop = 0x04
  all = 0xff

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
    pid = self._read_bytes(self._reg_pid, 1)
    vid = self._read_bytes(self._reg_vid, 1)
    if self.last_operate_status == self.sta_ok:
      if pid[0] != self._reg_def_pid:
        self.last_operate_status = self.sta_err_device_not_detected
      elif vid[0] != self._reg_def_vid:
        self.last_operate_status = self.sta_err_soft_verion
      else:
        self._set_control_mode(self._control_mode_dc_motor)
        self.motor_stop(self.all)
    return self.last_operate_status

  def set_addr(self, addr):
    '''
      @brief    Set board controler address

      @param address    Address to set, range in 1 to 127
    '''
    if addr < 1 or addr > 127:
      self.last_operate_status = self.sta_err_parameter
      return
    self._write_bytes(self._reg_slave_addr, [addr])
    if self.last_operate_status == self.sta_ok:
      self._addr = addr

  def _set_control_mode(self, mode):
    self._write_bytes(self._reg_control_mode, [mode])

  def set_encoder_enable(self, id):
    '''
      @brief    Set dc motor encoder enable

      @param id: int    Encoder id, in range 1 to 2
    '''
    id = int(id)
    if id < 0 or id > self._motor_count:
      self.last_operate_status = self.sta_err_parameter
      return
    self._write_bytes(self._reg_encoder1_enable + 5 * (id - 1), [0x01])
  
  def set_encoder_disable(self, id):
    '''
      @brief    Set dc motor encoder disable

      @param id: int   Encoder id, in range 1 to 2
    '''
    id = int(id)
    if id < 0 or id > self._motor_count:
      self.last_operate_status = self.sta_err_parameter
      return
    self._write_bytes(self._reg_encoder1_enable + 5 * (id - 1), [0x00])

  def set_encoder_reduction_ratio(self, id, reduction_ratio):
    '''
      @brief    Set dc motor encoder reduction ratio

      @param id: int                 Encoder id, in range 1 to 2
      @param reduction_ratio: int    Set dc motor encoder reduction ratio, range in 1 to 2000, (pulse per circle) = 16 * reduction_ratio * 2
    '''
    id = int(id)
    if id < 0 or id > self._motor_count:
      self.last_operate_status = self.sta_err_parameter
      return
    reduction_ratio = int(reduction_ratio)
    if reduction_ratio < 1 or reduction_ratio > 2000:
      self.last_operate_status = self.sta_err_parameter
      return
    self._write_bytes(self._reg_encoder1_reduction_ratio + 5 * (id - 1), [reduction_ratio >> 8, reduction_ratio & 0xff])

  def get_encoder_speed(self, id):
    '''
      @brief    Get dc motor encoder speed, unit rpm

      @param id: int   Encoder id, in range 1 to 2
    '''
    if id < 0 or id > self._motor_count:
      self.last_operate_status = self.sta_err_parameter
      return 0
    rslt = self._read_bytes(self._reg_encoder1_speed + 5 * (id - 1), 2)
    if rslt[0] & 0x80:
      return - (((rslt[0] & 0x7f) << 8) | rslt[1])
    else:
      return (((rslt[0] & 0x7f) << 8) | rslt[1])

  def set_moter_pwm_frequency(self, frequency):
    '''
      @brief    Set dc motor pwm frequency

      @param frequency: int    Frequency to set, in range 50HZ to 12750HZ, (actual frequency) = frequency - (frequency % 50)
    '''
    if frequency < 50 or frequency > 12750:
      self.last_operate_status = self.sta_err_parameter
      return
    frequency = int(frequency / 50)
    self._write_bytes(self._reg_motor_pwm, [frequency])

  def motor_movement(self, id, orientation, speed):
    '''
      @brief    Motor movement

      @param id: int             Motor id to move
      @param orientation: int    Motor orientation, this.cw (clockwise) or this.ccw (counterclockwise)
      @param speed: float        Motor pwm duty cycle, in range 1.1 to 99.9
    '''
    if id < 1 or id > self._motor_count:
      self.last_operate_status = self.sta_err_parameter
      return
    if orientation != self.cw and orientation != self.ccw:
      self.last_operate_status = self.sta_err_parameter
      return
    if speed > 99.9 or speed < 1.1:
      self.last_operate_status = self.sta_err_parameter
      return
    reg = self._reg_motor1_orientation + (id - 1) * 3
    self._write_bytes(reg, [0x00])
    self._write_bytes(reg, [orientation])
    self._write_bytes(reg + 1, [int(speed), int((speed * 10) % 10)])

  def motor_stop(self, id):
    '''
      @brief    Motor stop

      @param int    Motor id to stop, use this.all to stop all motors
    '''
    if id < 1 or id > self._motor_count:
      if id != self.all:
        self.last_operate_status = self.sta_err_parameter
        return
    if id == self.all:
      for i in range(1, self._motor_count + 1):
        self.motor_stop(i)
    else:
      self._write_bytes(self._reg_motor1_orientation + 3 * (id - 1), [self.stop])

  def detecte(self):
    '''
      @brief    If you forget address you had set, use this to detecte them, must have class instance

      @return   Board list conformed
    '''
    l = []
    back = self._addr
    for i in range(1, 127):
      self._addr = i
      if self.begin() == self.sta_ok:
        l.append(i)
    for i in range(0, len(l)):
      l[i] = hex(l[i])
    self._addr = back
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
    self.last_operate_status = self.sta_err_device_not_detected
    # print("write byte: ", hex(reg), buf)
    try:
      self._bus.write_i2c_block_data(self._addr, reg, buf)
      self.last_operate_status = self.sta_ok
    except:
      pass

  def _read_bytes(self, reg, len):
    self.last_operate_status = self.sta_err_device_not_detected
    try:
      rslt = self._bus.read_i2c_block_data(self._addr, reg, len)
      self.last_operate_status = self.sta_ok
      return rslt
    except:
      pass
