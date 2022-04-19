# DFRobot_RaspberryPi_Motor
* [English Version](./README.md)

这个RaspberryPi电机驱动板可以通过IIC与RaspberryPi进行通信。 <br>
它可以控制电机向前旋转和备用，以及转速。 <br>
控制命令为IIC命令，驱动命令为PWM信号。 <br>
单通道最大工作电流为1.2A。 输入端口与GPIO端口兼容。 <br>
具有2个独立的输出通道和2个编码器端口，可控制2个直流电机或2个带编码器的电机。 <br>
应用:RaspberryPi智能汽车，DIY水箱，DIY微型鱼… <br> 

![产品实物图](./resources/images/DFR0592.png)

## 产品链接 (https://www.dfrobot.com.cn/goods-2013.html)
    SKU: DFR0592


## 目录

* [概述](#概述)
* [库安装](#库安装)
* [方法](#方法)
* [兼容性](#兼容性)
* [历史](#历史)
* [创作者](#创作者)

## 概述

为直流电机驱动模块提供一个树莓派库。  <br>
1.  两个带有编码器控制的直流电机或普通直流电机。<br> 
2.  获得电机速度形式编码器。 <br>
3. 脉宽调制频率设置。 <br>
4.  PWM责任。<br>

## 库安装

这个传感器应该与DFRobot_RaspberryPi_DC_Motor在RaspberryPi上工作。 <br>
运行程序:
```
python DC_Motor_Demo.py
```

## 方法

```python

  def begin(self):
    '''!
      @brief    主板初始化
      @return   主板初始化状态
    '''

  def set_addr(self, addr):
    '''!
      @brief 设置单板控制器地址，重启模块使其生效  
      @param address  要设置的地址范围为1 ~ 127
    '''

  def set_encoder_enable(self, id):
    '''!
      @brief 设置直流电机编码器使能
      @param id  编码器列表、范围为1到2的项或id = self.ALL
    '''
  
  def set_encoder_disable(self, id):
    '''!
      @brief 禁用直流电机编码器
      @param id  编码器列表、范围为1到2的项或id = self.ALL
    '''

  def set_encoder_reduction_ratio(self, id, reduction_ratio):
    '''!
      @brief 设置直流电机编码器减速比
      @param id  编码器列表、范围为1到2的项或id = self.ALL
      @param reduction_ratio  设置直流电机编码器的减速比，范围在1 - 2000 , (pulse per circle) = 16 * reduction_ratio * 2
    '''

  def get_encoder_speed(self, id):
    '''!
      @brief  得到直流电机编码器的速度，单位转速
      @param  id  编码器列表、范围为1到2的项或id = self.ALL
      @return  编码器速度列表
    '''

  def set_moter_pwm_frequency(self, frequency):
    '''!
      @brief 设置直流电机pwm频率
      @param frequency   频率设置，范围100HZ ~ 12750HZ，否则无效 (actual frequency) = frequency - (frequency % 50)
    '''

  def motor_movement(self, id, orientation, speed):
    '''!
      @brief 电机运动
      @param id           电机列表，1到2的项目，或id = self.ALL
      @param orientation  电机方向, self.CW (顺时针方向) or self.CCW (逆时针方向)
      @param speed        电机pwm占空比，范围为0 ~ 100，否则无效  
    '''

  def motor_stop(self, id):
    '''!
      @brief 电机停止
      @param id  电机列表，1到2的项目，或id = self.ALL
    '''

  def detecte(self):
    '''!
      @brief    如果您忘记了您已经设置的地址，使用此来检测它们，必须有类实例  
      @return   董事会名单确认
    '''

```

## 兼容性

* RaspberryPi 版本

| Board        | Work Well | Work Wrong | Untested | Remarks |
| ------------ | :-------: | :--------: | :------: | ------- |
| RaspberryPi2 |           |            |    √     |         |
| RaspberryPi3 |           |            |    √     |         |
| RaspberryPi4 |     √     |            |          |         |

* Python 版本

| Python  | Work Well | Work Wrong | Untested | Remarks |
| ------- | :-------: | :--------: | :------: | ------- |
| Python2 |     √     |            |          |         |
| Python3 |     √     |            |          |         |


## 历史

- 2019/03/16 - 1.0.0 版本
- 2022/04/19 - 1.0.1 版本


## 创作者

Written by tangjie(jie.tang@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))
