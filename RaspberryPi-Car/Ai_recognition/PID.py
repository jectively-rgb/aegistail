

#@Date: 2026-01-21 20:34:09 
#@LastEditors: jack jaehyung kim 


# PID 제어 1차 관성 시스템 테스트 프로그램
#*****************************************************************#
#                   증분형 PID 시스템                              #
#*****************************************************************#******************************************************#
class IncrementalPID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D
 
        self.PIDOutput = 0.0             #PID제어기 출력
        self.SystemOutput = 0.0          #시스템 출력값
        self.LastSystemOutput = 0.0      #이전 시스템 출력값
 
        self.Error = 0.0                 #목표값과 출력값의 오차
        self.LastError = 0.0             # 이전 오차
        self.LastLastError = 0.0         # 그 이전 오차 
 
    #PID 제어기 입력(스텝 신호) 설정
    def SetStepSignal(self,StepSignal):
        self.Error = StepSignal - self.SystemOutput
        IncrementValue = self.Kp * (self.Error - self.LastError) +\
        self.Ki * self.Error +\
        self.Kd * (self.Error - 2 * self.LastError + self.LastLastError)

        self.PIDOutput += IncrementValue
        self.LastLastError = self.LastError
        self.LastError = self.Error

   # 1차 관성 시스템 설정
    # InertiaTime : 관성 시간 상수
    def SetInertiaTime(self,InertiaTime,SampleTime):
        self.SystemOutput = (InertiaTime * self.LastSystemOutput + \
            SampleTime * self.PIDOutput) / (SampleTime + InertiaTime)

        self.LastSystemOutput = self.SystemOutput
 
 
# *****************************************************************#
#                      위치형 PID 시스템                             #
# *****************************************************************#
class PositionalPID:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D
 
        self.SystemOutput = 0.0         #시스템출력
        self.ResultValueBack = 0.0      # 이전 출력값
        self.PidOutput = 0.0            # PID 출력
        self.PIDErrADD = 0.0            # 오차 누적값 (적분 항)
        self.ErrBack = 0.0              # 이전 오차 
    
    # PID 제어기 입력(스텝 신호) 설정
    def SetStepSignal(self,StepSignal):
        Err = StepSignal - self.SystemOutput
        KpWork = self.Kp * Err
        KiWork = self.Ki * self.PIDErrADD
        KdWork = self.Kd * (Err - self.ErrBack)
        self.PidOutput = KpWork + KiWork + KdWork
        self.PIDErrADD += Err
        self.ErrBack = Err

    # 1차 관성 시스템 설정
    # InertiaTime : 관성 시간 상수
    def SetInertiaTime(self, InertiaTime,SampleTime):
       self.SystemOutput = (InertiaTime * self.ResultValueBack + \
           SampleTime * self.PidOutput) / (SampleTime + InertiaTime)
       self.ResultValueBack = self.SystemOutput
       