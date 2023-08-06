from hyc.num import *

# 分数类
class fraction:
    def __init__(self,denominator: int, numerator: int, num: int=0):
        self.fraction = [denominator, numerator+num*denominator]

    # 分数化整数（保留到个位）
    def __int__(self):
        if self.fraction[1] > self.fraction[0]:
            num = self.fraction[1]//self.fraction[0]
        else:
            num = 0
        return num

    # 读作
    def __str__(self):
        self.red_fr()
        if int(self)<1 or float(self)%1==0:
            string = '{}分之{}'.format(self.fraction[0], self.fraction[1])
        else:
           string = '{}又{}分之{}'.format(int(self), self.fraction[0], self.fraction[1]%self.fraction[0])
        return string

    # 分数化小数（自动四舍五入到百分位）
    def __float__(self):
        decimal = self.fraction[1]/self.fraction[0]
        decimal = round(decimal, 2)
        return decimal

    # 约分
    def red_fr(self):
        if self.simp_fr():
            return self
        else:
            _, common_div = hcf(self.fraction)
            for i in range(2):
                self.fraction[i] = self.fraction[i]//common_div
            return self

    # 最简分数
    def simp_fr(self):
        if coprime(self.fraction):
            return True
        else:
            return False

    # 倒数
    def opposide(self):
        fraction_opposide = fraction(self.fraction[1], self.fraction[0])
        return fraction_opposide

    # 分数运算-加法
    def __add__(self, other):
        result = 0
        fraction_list = den_di([self,other])
        for i in fraction_list:
            result += i.fraction[1]
        fraction_sum = fraction(fraction_list[0].fraction[0], result)
        return fraction_sum.red_fr()


    # 分数运算-减法
    def __sub__(self, other):
        minuend, subtracted = den_di([self, other])
        minuend.fraction[1]-=subtracted.fraction[1]
        return minuend.red_fr()

    # 分数运算-乘法
    def __mul__(self, other):
        deno = 1
        mole = 1
        for i in [self.fraction, other.fraction]:
            deno*=i[0]
            mole*=i[1]
        result = fraction(deno,mole)
        return result.red_fr()

    # 分数运算-除法
    def __truediv__(self, other):
        result = self*other.opposide()
        return result.red_fr()

    # 分数运算-平方
    def __pow__(self, power, modulo=None):
        result = covert(1)
        for i in range(power):
            result *= self
        return result

# 通分
def den_di(fraction_list: list[fraction]):
    all_deno = []
    for i in fraction_list:
        all_deno.append(i.fraction[0])
    common_deno = lcm(all_deno)
    new_fraction_list = []
    for i in fraction_list:
        common_mul = int(common_deno/i.fraction[0])
        i = fraction(i.fraction[0]*common_mul, i.fraction[1]*common_mul)
        new_fraction_list.append(i)
    return new_fraction_list

# 小数化分数
def covert(covert_num: float):
    covert_num = float(covert_num)
    num, decimal = str(covert_num).split('.')
    if covert_num<1:
        frac = fraction(10**len(decimal), int(decimal))
    else:
        frac = fraction(10**len(decimal), int(decimal)+int(num)*10**len(decimal))
    return frac.red_fr()