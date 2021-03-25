#연평균 성장률(연복리 수익률), 1년동안 얼마 만큼씩 증가??
def getCAGR(first:float,last:float,years:float)->float:
    return (last/first)**(1/years) - 1

# print("CAGR : {:.2%}".format(getCAGR(65300,2669000,20)))
from calendar import month
print(month(2020,1))
import this
