#글자로 그리는거 후에 py게임으로 만들어나 볼까 시간 충분하면 
#계급의 갯수는 작성하는걸로
#파일을 가져올때 파일을 직접 찾아올수있도록 변경해볼까?<-근데 궁금한게 다른 어플리케이션은 조금씩 파일 위치가 다를건데 어떻게 자기 파일위치를 잘아는거지?
#상대경로? 절대경로 
class grif:
  def __init__(self):
    self.reset("")
  
  def reset(self,data):
    if data=="":
      data="data.txt"
    self.data_file = open(data,"r")
    self.data=self.data_file.read()
    self.data_file.close()
    self.data=self.data.split(",")
    for i in range(len(self.data)):
      self.data[i]=int(self.data[i])
    self.data.sort()

    self.unit=1
    self.no_class=6 #int(input("양의정수 작성")),추후 수정필요

    self.buffer=(self.data[-1]-self.data[0])/self.no_class
    #divide=[round(self.self.data[len(self.self.data)-1]*i/no_class+self.self.data[0]*(no_class-i)/no_class) for i in range(no_class+1)] #round를 안에 넣을생각을 못했네
    self.divide=[round((self.data[0]-self.buffer)*(self.no_class+0.5-i)/(self.no_class+1)+(self.data[-1]+self.buffer)*(i+0.5)/(self.no_class+1)) for i in range(self.no_class+1)]#생각해보니 나 지금까지 왜 len(divide)를 쓴거지 그냥 -1넣으면되는데 
    self.Class_range=[f"{self.divide[i]}~{self.divide[i+1]-self.unit/10}" for i in range(len(self.divide)-1)]#왜 0.5씩 분배하는게 양쪽에 1씩 넣는것보다 결과값이 좋지? 적어도 지금의 나는 대답하기 어렵다.
    self.Class=[i+1 for i in range(len(self.Class_range))]
    self.Class_Mark=[f"{(self.divide[i]+self.divide[i+1]-self.unit/10)/2}" for i in range(len(self.divide)-1)]
    self.Frequency=[len([x for x in self.data if self.divide[i]<=x<self.divide[i+1]]) for i in range(len(self.divide)-1)]
    self.Relative_Frequency=[sum(self.Frequency[0:i+1]) for i in range(len(self.Frequency))]
    #이전의 거가 기록이되어야하고 저장이되어야하는데 그거를 동시에 진행하려면 저장이되고 기록이되어야함
    self.Cumulative_Frequency=[self.Frequency[i]/len(self.data) for i in range(len(self.Frequency))]
    self.Cumulative_Relative_Frequency=[sum(self.Cumulative_Frequency[0:i+1]) for i in range(len(self.Cumulative_Frequency))]
    self.full_data=[self.Class,self.Class_range,self.Frequency,self.Relative_Frequency,self.Cumulative_Frequency,self.Cumulative_Relative_Frequency,self.Class_Mark]
    #1.하나의 긴자를 원하는 등분으로 자를수있어야함->숫자가 걸치는 문제발생 1~19,19~27
    #2.그리고 그긴자를 자르기 시작하는 부분이 괴상한 숫자가 아닌 괜찮은 숫자여야함(5 10단위)
    #3.그러면 양옆에 한칸정도는 데이터가 거의없는 완충구역을 만들어두자
  def redata(self): #https://jjeongil.tistory.com/1590 이파트 참고한거(파일유무 참고)
    adress=str(input("파일 주소를 입력해 주세요.(공백일시 기본 데이터가 입력됨니다.)"))
    try: #여기 파트가 파일이 실존하는지 확인하는 파트인데 import os나 pathlib을 사용하는 방법이 존재하는데 import쓰지 말라고 하셨기때문에 없는 버전을 찾아서 가져옴
      if adress=="":
        self.reset(adress)
      else:
        f=open(adress)
        f.close()
        self.reset(adress)  
    except:
      print("File not accessible")
      self.redata()
    #기존에는 여기에 finally와 self.reset(adress)였었는데 재귀를 하니깐 이쪽에있으니 에러가 나서 위치 옮김

    
  
  def Frequency_Distribution_table(self):#이거는 도수분포표
    print(f"{'계급':<10}|{'계급간격':^10}|{'도수':^10}|{'누적도수':^10}|{'상대도수':^10}|{'누적상대도수':^10}|{'계급값':>10}")

    for name,clrange,frequency,relative_Frequency,cumulative_Frequency,cumulative_Relative_Frequency,clMark in zip(*self.full_data):
      print(f"{'제'+str(name)+'계급':<9}|{clrange:^14}|{frequency:^12}|{relative_Frequency:^14}|{cumulative_Frequency:^14.2f}|{cumulative_Relative_Frequency:^16.2f}|{clMark:>14}")
    return 1# https://ooyoung.tistory.com/87 기억이슈로 확인한거
  
  def histogram(self,R=None,):
    #포인터로 맨윗줄부터 내려가면서 하는거
    #이거는 상대도수 히스토그램
    if R==None:
      R=self.Relative_Frequency
    pointer=max(R)#근데 데이터만 잘 다듬어서 여기에 그냥 집어넣으면 되는거 아닌가? 아 "상대"도수구나 이건 그냥 누적도수고 이런! 그래도 일단 남겨는 놔야겠다
    while pointer>0:
      if pointer%5==0:
        print(f"{pointer:<4}",end="")
      else:
        print(f"    ",end="")

      for a in R:
        if a>=pointer:
          print(f" ⬜⬜",end="")
        else:
          if a+1==pointer:
            print(" ⬛⬜",end="")
          else:
            print(" ⬛⬛",end='')
      print("")

      pointer=pointer-2                      
    print("     ",end="")
    for i in self.Class_Mark:
      print(f"{float(i):<5.1f}",end="")
    print("")
    return 1

  def Cumulative_histogram(self,choice):
    #소수인데 어떻게 하지
    #지금보니 대략 20~30쯤이 그래프가 이쁘게 나오는것같아 일단 저 히스토그램만드는건 유지하고 추후 개선을 하고  저걸 함수로 변형하고 상대도수를 소수대에서 자연수로 바꾸고 그냥 그대로 넣어버리며 되겠다.
    af=[]
    if choice=='3':
      af=self.Cumulative_Frequency
    elif choice=='4':
      af=self.Cumulative_Relative_Frequency
    else:
      print("에헤이 조졌네이거")    
      return -1
    
    pointer=1
    while pointer>0:
      if pointer in [0.2,0.4,0.6,0.8,1.0]:
        print(f"{pointer:<4}",end="")
      else:
        print(f"    ",end="")

      for a in af:
        if a>=pointer:
          print(f" ⬜⬜",end="")
        else:
          if pointer-0.05<a<pointer:
            print(" 🟨🟨",end="")
          else:
            print(" ⬛⬛",end='')
      print("")

      pointer=pointer-0.1
    print("     ",end="")
    for i in self.Class_Mark:
      print(f"{float(i):<5.1f}",end="")
    print("")
    return 1


  def fun(self,susususupanoba):
    if susususupanoba=='1':
      self.Frequency_Distribution_table()
    elif susususupanoba=='2':
      self.histogram(None)
    elif susususupanoba=='3':
      self.Cumulative_histogram(susususupanoba)
    elif susususupanoba=='4':
      self.Cumulative_histogram(susususupanoba)
    elif susususupanoba=="5":
      self.redata()
    elif susususupanoba=="exit":
      return -1
    else:
      self.fun(str(input("1:도수분포표 \n2:누적도수 히스토그램 \n3:상대도수 히스토그램\n4:누적 상대도수 히스토그램\n5:데이터 변경\nexit:종료\n입력:")))

#가로면 칸을 ]]]] ||||||||같은걸로 표현하면 되는데 세로니깐 안돼서 조금 어렵다.

#근데 지금 문제점이 데이터의 양이 너무 적거나 너무 많아지면 지금 가진 형태로도 힘들거나 불가능 할 가능성이 있다는 사실
#이거는 pointer값이 50이하 될정도로 계속 절반정도로 깎고 다깎겼으면 2^깎인 횟수 만큼 가로를 늘리거나 다른 방도(1/2정도 칠해진 정사각형 이용하기)를 취하면 되고 그러면 코드 마지막에있는 pointer-2도 -1로 바꾸면 된다!
#근데 지금 당장하긴 좀그러니(다른과제들이 남음)다른 과제를 완료하고 시간남으면 하는걸로 
program=grif()
while True:
  end=program.fun(str(input("1:도수분포표 \n2:누적도수 히스토그램 \n3:상대도수 히스토그램\n4:누적 상대도수 히스토그램\n5:데이터 변경\nexit:종료\n입력:")))
  if end==-1:
    break

"⬛🟨⬜"
#9/15 거의다 만들었고 상대도수 히스토그램이랑 누적 상대도수 히스토그램 만들때 왼쪽에 단위가 30으로 나오는거랑(완벽하진않은데 어떻게든 고치긴함 9/16 AM 10:30)
#데이터 다른거들도 받을수있도록 변경하면 될듯 (9/16 AM 9:44 완료)
#이게 사실 버그수정이랑 패치말고는 할게 없어서 더안할 거긴한데 데이터를 바꿔가면서하는게 아니라 한쪽에 저장해두고 비교하는 방식으로 갔으면 조금더 좋지않았을까 하는 생각이있는데 
#program.append(grif(data))이런느낌으로 