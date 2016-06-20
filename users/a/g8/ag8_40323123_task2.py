from flask import Blueprint, request
 
ag8_test = Blueprint('ag8_test', __name__, url_prefix='/ag8_test', template_folder='templates')
 
head_str = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 2D 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
<script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango-8v03.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="http://cptocadp-2015fallhw.rhcloud.com/static/CangoAxes-1v33.js"></script>
 
</head>
<body>
 
<script>
window.onload=function(){
brython(1);
}
</script>
 
<canvas id="plotarea" width="800" height="800"></canvas>
'''
 
tail_str = '''
</script>
</body>
</html>
'''
 
chain_str = '''
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window
import math
 
cango = JSConstructor(window.Cango)
cobj = JSConstructor(window.Cobj)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
 
cgo.setWorldCoords(-250, -250, 500, 500) 
 
# 畫軸線
cgo.drawAxes(0, 240, 0, 240, {
    "strokeColor":"#aaaaaa",
    "fillColor": "#aaaaaa",
    "xTickInterval": 20,
    "xLabelInterval": 20,
    "yTickInterval": 20,
    "yLabelInterval": 20})
 
deg = math.pi/180  
 
# 將繪製鏈條輪廓的內容寫成 class 物件
class chain():
    # 輪廓的外型設為 class variable
    chamber = "M -6.8397, -1.4894 \
            A 7, 7, 0, 1, 0, 6.8397, -1.4894 \
            A 40, 40, 0, 0, 1, 6.8397, -18.511 \
            A 7, 7, 0, 1, 0, -6.8397, -18.511 \
            A 40, 40, 0, 0, 1, -6.8397, -1.4894 z"
    #chamber = "M 0, 0 L 0, -20 z"
    cgoChamber = window.svgToCgoSVG(chamber)
 
    def __init__(self, fillcolor="green", border=True, strokecolor= "tan", linewidth=2, scale=1):
        self.fillcolor = fillcolor
        self.border = border
        self.strokecolor = strokecolor
        self.linewidth = linewidth
        self.scale = scale
 
    # 利用鏈條起點與終點定義繪圖
    def basic(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # 注意, cgo.Chamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(math.atan2(y2-y1, x2-x1)/deg+90)
 
        # 放大 scale 倍
        cgo.render(basic1, x1, y1, self.scale, 0)
 
    # 利用鏈條起點與旋轉角度定義繪圖, 使用內定的 color, border 與 linewidth 變數
    def basic_rot(self, x1, y1, rot, v=False):
        # 若 v 為 True 則為虛擬 chain, 不 render
        self.x1 = x1
        self.y1 = y1
        self.rot = rot
        self.v = v
        # 注意, cgoChamber 為成員變數
        cmbr = cobj(self.cgoChamber, "SHAPE", {
                "fillColor": self.fillcolor,
                "border": self.border,
                "strokeColor": self.strokecolor,
                "lineWidth": self.linewidth })
 
        # hole0 為原點位置
        hole = cobj(shapedefs.circle(4*self.scale), "PATH")
        cmbr.appendPath(hole)
        # 根據旋轉角度, 計算 x2 與 y2
        x2 = x1 + 20*math.cos(rot*deg)*self.scale
        y2 = y1 + 20*math.sin(rot*deg)*self.scale
 
        # 複製 cmbr, 然後命名為 basic1
        basic1 = cmbr.dup()
        # 因為鏈條的角度由原點向下垂直, 所以必須轉 90 度, 再考量 atan2 的轉角
        basic1.rotate(rot+90)
 
        # 放大 scale 倍
        if v == False:
            cgo.render(basic1, x1, y1, self.scale, 0)
 
        return x2, y2
'''
 
# 傳繪 A 函式內容
def a(x, y, scale=1, color="green"):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain(scale='''+str(scale)+''', fillcolor="'''+str(color)+'''")
 
# 畫 A
# 左邊兩個垂直單元
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
# 左斜邊兩個單元
x3, y3 = mychain.basic_rot(x2, y2, 80)
x4, y4 = mychain.basic_rot(x3, y3, 71)
# 最上方水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜邊兩個單元
x6, y6 = mychain.basic_rot(x5, y5, -71)
x7, y7 = mychain.basic_rot(x6, y6, -80)
# 右邊兩個垂直單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
x9, y9 = mychain.basic_rot(x8, y8, -90)
# 中間兩個水平單元
x10, y10 = mychain.basic_rot(x8, y8, -180)
mychain.basic(x10, y10, x1, y1)
'''
 
    return outstring
 
 
# 傳繪 B 函式內容
def b(x, y):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 畫 B
# 左邊四個垂直單元
# 每一個字元間隔為 65 pixels
#x1, y1 = mychain.basic_rot(0+ 65, 0, 90)
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
x3, y3 = mychain.basic_rot(x2, y2, 90)
x4, y4 = mychain.basic_rot(x3, y3, 90)
# 上方一個水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜 -30 度
x6, y6 = mychain.basic_rot(x5, y5, -30)
# 右上垂直向下單元
x7, y7 = mychain.basic_rot(x6, y6, -90)
# 右斜 240 度
x8, y8 = mychain.basic_rot(x7, y7, 210)
# 中間水平
mychain.basic(x8, y8, x2, y2)
# 右下斜 -30 度
x10, y10 = mychain.basic_rot(x8, y8, -30)
# 右下垂直向下單元
x11, y11 = mychain.basic_rot(x10, y10, -90)
# 右下斜 240 度
x12, y12 = mychain.basic_rot(x11, y11, 210)
# 水平接回起點
mychain.basic(x12,y12, '''+str(x)+","+str(y)+''')
'''
 
    return outstring
 
# 傳繪 C 函式內容
def c(x, y):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 上半部
# 左邊中間垂直起點, 圓心位於線段中央, y 方向再向上平移兩個鏈條圓心距單位
#x1, y1 = mychain.basic_rot(0+65*2, -10+10+20*math.sin(80*deg)+20*math.sin(30*deg), 90)
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+'''-10+10+20*math.sin(80*deg)+20*math.sin(30*deg), 90)
# 上方轉 80 度
x2, y2 = mychain.basic_rot(x1, y1, 80)
# 上方轉 30 度
x3, y3 = mychain.basic_rot(x2, y2, 30)
# 上方水平
x4, y4 = mychain.basic_rot(x3, y3, 0)
# 下半部, 從起點開始 -80 度
#x5, y5 = mychain.basic_rot(0+65*2, -10+10+20*math.sin(80*deg)+20*math.sin(30*deg), -80)
x5, y5 = mychain.basic_rot('''+str(x)+","+str(y)+'''-10+10+20*math.sin(80*deg)+20*math.sin(30*deg), -80)
# 下斜 -30 度
x6, y6 = mychain.basic_rot(x5, y5, -30)
# 下方水平單元
x7, y7 = mychain.basic_rot(x6, y6, -0)
'''
 
    return outstring
 
 
# 傳繪 D 函式內容
def d(x, y):
    outstring = '''
# 利用 chain class 建立案例, 對應到 mychain 變數
mychain = chain()
 
# 左邊四個垂直單元
#x1, y1 = mychain.basic_rot(0+65*3, 0, 90)
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 90)
x2, y2 = mychain.basic_rot(x1, y1, 90)
x3, y3 = mychain.basic_rot(x2, y2, 90)
x4, y4 = mychain.basic_rot(x3, y3, 90)
# 上方一個水平單元
x5, y5 = mychain.basic_rot(x4, y4, 0)
# 右斜 -40 度
x6, y6 = mychain.basic_rot(x5, y5, -40)
x7, y7 = mychain.basic_rot(x6, y6, -60)
# 右中垂直向下單元
x8, y8 = mychain.basic_rot(x7, y7, -90)
# -120 度
x9, y9 = mychain.basic_rot(x8, y8, -120)
# -140
x10, y10 = mychain.basic_rot(x9, y9, -140)
# 水平接回原點
#mychain.basic(x10, y10, 0+65*3, 0, color="red")
mychain.basic(x10, y10, '''+str(x)+","+str(y)+''')
'''
 
    return outstring
 
def circle(x, y):
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+''', 50)
'''
    for i in range(2, 10):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*40)+") \n"
    return outstring
 
def circle1(x, y, degree=10):
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    #degree = 10
    first_degree = 90 - degree
    repeat = 360 / degree
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
    return outstring
 
 
def circle2(x, y, degree=10):
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    #degree = 10
    first_degree = 90 - degree
    repeat = 360 / degree
 
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
    return outstring
 
 
def twocircle(x, y):
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    x = 50
    y = 0
    degree = 12
    # 78, 66, 54, 42, 30, 18, 6度
    #必須有某些 chain 算座標但是不 render
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節也是 virtual chain
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''', True)
#x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    # 這裡要上下各多留一節虛擬 chain, 以便最後進行連接 (x7, y7) 與 (x22, y22)
    for i in range(2, int(repeat)+1):
        #if i < 7 or i > 23:        
        if i <= 7 or i >= 23:
            # virautl chain
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+", True) \n"
            #outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
 
    p = -150
    k = 0
    degree = 20
    # 70, 50, 30, 10
    # 從 i=5 開始, 就是 virautl chain
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
p1, k1 = mychain.basic_rot('''+str(p)+","+str(k)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        if i >= 5 and i <= 13:
            # virautl chain
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+", True) \n"
            #outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+") \n"
 
    # 上段連接直線
    # 從 p5, k5 作為起點
    first_degree = 10
    repeat = 11
    outstring += '''
m1, n1 = mychain.basic_rot(p4, k4, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "m"+str(i)+", n"+str(i)+"=mychain.basic_rot(m"+str(i-1)+", n"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 下段連接直線
    # 從 p12, k12 作為起點
    first_degree = -10
    repeat = 11
    outstring += '''
r1, s1 = mychain.basic_rot(p13, k13, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "r"+str(i)+", s"+str(i)+"=mychain.basic_rot(r"+str(i-1)+", s"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 上段右方接點為 x7, y7, 左側則為 m11, n11
    outstring += "mychain.basic(x7, y7, m11, n11)\n"
    # 下段右方接點為 x22, y22, 左側則為 r11, s11
    outstring += "mychain.basic(x22, y22, r11, s11)\n"
 
    return outstring
def realcircle(x, y):
    
     # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    x = 50
    y = 0
    degree = 12
    # 78, 66, 54, 42, 30, 18, 6度
    #必須有某些 chain 算座標但是不 render
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節也是 virtual chain
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''', True)
#x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    # 這裡要上下各多留一節虛擬 chain, 以便最後進行連接 (x7, y7) 與 (x22, y22)
    for i in range(2, int(repeat)+1):
        #if i < 7 or i > 23:        
        if i <= 3 or i >= 22:
            # virautl chain
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+",True) \n"
            #outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
 
    p = -150
    k = 0
    degree = 20
    # 70, 50, 30, 10
    # 從 i=5 開始, 就是 virautl chain
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
p1, k1 = mychain.basic_rot('''+str(p)+","+str(k)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        if i >= 7 and i <= 15:
            # virautl chain
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+", True) \n"
            #outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+", 90-"+str(i*degree)+") \n"

    s = -97
    t = 124.5
    degree = 12
    # 70, 50, 30, 10
    # 從 i=5 開始, 就是 virautl chain
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
s1, t1 = mychain.basic_rot('''+str(s)+","+str(t)+", "+str(first_degree)+''',True)
#x1, y1 = mychain.basic_rot('''+str(x)+","+str(y)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):

        if i <= 18 or i >= 26:
            # virautl chain
            outstring += "s"+str(i)+", t"+str(i)+"=mychain.basic_rot(s"+str(i-1)+", t"+str(i-1)+", 90-"+str(i*degree)+",True) \n"
        else:
            outstring += "s"+str(i)+", t"+str(i)+"=mychain.basic_rot(s"+str(i-1)+", t"+str(i-1)+", 90-"+str(i*degree)+") \n"
 
 
    a = -180
    b = 101
    degree = 5
    # 70, 50, 30, 10
    # 從 i=5 開始, 就是 virautl chain
    first_degree = 90 - degree
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
a1, b1 = mychain.basic_rot('''+str(a)+","+str(b)+", "+str(first_degree)+''',True)
'''
    for i in range(2, int(repeat)+1):


       
        if i <= 47 or i >= 65:
            # virautl chain
            outstring += "a"+str(i)+", b"+str(i)+"=mychain.basic_rot(a"+str(i-1)+", b"+str(i-1)+", 90-"+str(i*degree)+",True) \n"
            #outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+", 90-"+str(i*degree)+") \n"
        else:
            outstring += "a"+str(i)+", b"+str(i)+"=mychain.basic_rot(a"+str(i-1)+", b"+str(i-1)+", 90-"+str(i*degree)+") \n"




 
    return outstring

def eighteenthirty(x, y):
    '''
從圖解法與符號式解法得到的兩條外切線座標點
(-203.592946177111, 0.0), (0.0, 0.0), (-214.364148466539, 56.5714145924675), (-17.8936874260919, 93.9794075692901)
(-203.592946177111, 0.0), (0.0, 0.0), (-214.364148466539, -56.5714145924675), (-17.8936874260919, -93.9794075692901)
左邊關鍵鍊條起點 (-233.06, 49.48), 角度 20.78, 圓心 (-203.593, 0.0)
右邊關鍵鍊條起點 (-17.89, 93.9), 角度 4.78, 圓心 (0, 0)
    '''
    # 20 為鏈條兩圓距
    # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2)
    # degree = math.asin(20/2/radius)*180/math.pi
    x = 50
    y = 0
    degree = 20
    first_degree = 20.78
    startx = -233.06+100
    starty = 49.48
    repeat = 360 / degree
    # 先畫出左邊第一關鍵節
    outstring = '''
mychain = chain()
 
x1, y1 = mychain.basic_rot('''+str(startx)+","+str(starty)+", "+str(first_degree)+''')
 
'''
    # 接著繪製左邊的非虛擬鍊條
    for i in range(2, int(repeat)+1):
        if i >=2 and i <=11:
            # virautl chain
            #outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+", True) \n"
        else:
            outstring += "x"+str(i)+", y"+str(i)+"=mychain.basic_rot(x"+str(i-1)+", y"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
 
    # 接著處理右邊的非虛擬鍊條
    # 先畫出右邊第一關鍵節
 
    p = -17.89+100
    k = 93.98
    degree = 12
    first_degree = 4.78
    repeat = 360 / degree
    # 第1節不是 virtual chain
    outstring += '''
#mychain = chain()
 
p1, k1 = mychain.basic_rot('''+str(p)+","+str(k)+", "+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        if i >=18:
            # virautl chain
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+", True) \n"
            #outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
        else:
            outstring += "p"+str(i)+", k"+str(i)+"=mychain.basic_rot(p"+str(i-1)+", k"+str(i-1)+","+str(first_degree+degree-i*degree)+") \n"
 
    # 上段連接直線
    # 從 x1, y1 作為起點
    first_degree = 10.78
    repeat = 10
    outstring += '''
m1, n1 = mychain.basic_rot(x1, y1, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "m"+str(i)+", n"+str(i)+"=mychain.basic_rot(m"+str(i-1)+", n"+str(i-1)+", "+str(first_degree)+")\n"
 
    # 下段連接直線
    # 從 x11, y11 作為起點
    first_degree = -10.78
    repeat = 10
    outstring += '''
r1, s1 = mychain.basic_rot(x11, y11, '''+str(first_degree)+''')
'''
    for i in range(2, int(repeat)+1):
        outstring += "r"+str(i)+", s"+str(i)+"=mychain.basic_rot(r"+str(i-1)+", s"+str(i-1)+", "+str(first_degree)+")\n"
 
    return outstring
 
 
@ag8_test.route('/a')
def draw_a():
    return head_str + chain_str + a(0, 0) + tail_str
 
 
@ag8_test.route('/b')
def draw_b():
   # 每個橫向字元距離為 65 pixels, 上下字距則為 110 pixels
    return head_str + chain_str + b(0+65, 0) + tail_str
 
 
@ag8_test.route('/c')
def draw_c():
    # 每個橫向字元距離為 65 pixels
    return head_str + chain_str + c(0+65*2, 0) + tail_str
 
 
@ag8_test.route('/d')
def draw_d():
    return head_str + chain_str + d(0+65*3, 0) + tail_str
 
 
@ag8_test.route('/ab')
def draw_ab():
    #return head_str + chain_str + a(0, 0) + b(0+65, 0) + tail_str
    return head_str + chain_str + a(0, 0) + b(0, 0-110) + tail_str
 
 
@ag8_test.route('/ac')
def draw_ac():
    return head_str + chain_str + a(0, 0) + c(0+65, 0) + tail_str
 
 
@ag8_test.route('/bc')
def draw_bc():
    return head_str + chain_str + b(0, 0) + c(0+65, 0) + tail_str
 
 
@ag8_test.route('/abc')
def draw_abc():
    return head_str + chain_str + a(0, 0) + b(0+65, 0) + c(0+65*2, 0) + tail_str
 
 
@ag8_test.route('/aaaa')
def draw_aaaa():
    outstring = head_str + chain_str
    scale = 2
    for i in range(15):
        scale = scale*0.9
        outstring +=  a(0+10*i, 0, scale=scale)
    return outstring + tail_str
    #return head_str + chain_str + a(0, 0, scale=1) + a(0+65, 0, scale=0.8, color="red") + a(0+65*2, 0, scale=0.6) + a(0+65*3, 0, scale=0.4, color="red") + tail_str
 
 
@ag8_test.route('/badc')
def draw_badc():
    return head_str + chain_str + b(0, 0) + a(0+65, 0) + d(0+65*2, 0) + c(0+65*3, 0) + tail_str
 
 
@ag8_test.route('/abcd')
def draw_abcd():
    #return head_str + chain_str + a(0, 0) + b(0+65, 0) + c(0+65*2, 0) + d(0+65*3, 0) + tail_str
    return head_str + chain_str + a(0, 110) + b(0, 110-110) + c(0, 110-110*2) + d(0, 110-110*3) + tail_str
 
 
@ag8_test.route('/circle')
def drawcircle():
    return head_str + chain_str + circle(0, 0) + tail_str
 
 
@ag8_test.route('/circle1/<degree>', defaults={'x': 0, 'y': 0})
@ag8_test.route('/circle1/<x>/<degree>', defaults={'y': 0})
@ag8_test.route('/circle1/<x>/<y>/<degree>')
#@ag100.route('/circle1/<int:x>/<int:y>/<int:degree>')
def drawcircle1(x,y,degree):
    return head_str + chain_str + circle1(int(x), int(y), int(degree)) + tail_str
 
 
@ag8_test.route('/circle2/<degree>', defaults={'x': 0, 'y': 0})
@ag8_test.route('/circle2/<x>/<degree>', defaults={'y': 0})
@ag8_test.route('/circle2/<x>/<y>/<degree>')
#@ag100.route('/circle2/<int:x>/<int:y>/<int:degree>')
def drawcircle2(x,y,degree):
    return head_str + chain_str + circle2(int(x), int(y), int(degree)) + tail_str
 
 
@ag8_test.route('/twocircle/<x>/<y>')
@ag8_test.route('/twocircle', defaults={'x':0, 'y':0})
def drawtwocircle(x,y):
    return head_str + chain_str + twocircle(int(x), int(y)) + tail_str
 
 
@ag8_test.route('/realcircle/<x>/<y>')
@ag8_test.route('/realcircle', defaults={'x':0, 'y':0})
def drawrealcircle(x,y):
    return head_str + chain_str + realcircle(int(x), int(y)) + tail_str
@ag8_test.route('/eighteenthirty/<x>/<y>')
@ag8_test.route('/eighteenthirty', defaults={'x':0, 'y':0})
def draweithteenthirdy(x,y):
    return head_str + chain_str + eighteenthirty(int(x), int(y)) + tail_str
 
 
@ag8_test.route('/snap')
# http://svg.dabbles.info/snaptut-base
def snap():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>
    <script type="text/javascript" src="/static/snap.svg-min.js"></script>
 
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>
 
<svg width="800" height="800" viewBox="0 0 800 800" id="svgout"></svg>
 
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window, document
 
# 透過 window 與 JSConstructor 從 Brython 物件 snap 擷取 Snap 物件的內容
snap = JSConstructor(window.Snap)
 
s = snap("#svgout")
# 建立物件時, 同時設定 id 名稱
r = s.rect(10,10,100,100).attr({'id': 'rect'})
c = s.circle(100,100,50).attr({'id': 'circle'})
r.attr('fill', 'red')
c.attr({ 'fill': 'blue', 'stroke': 'black', 'strokeWidth': 10 })
r.attr({ 'stroke': '#123456', 'strokeWidth': 20 })
s.text(180,100, '點按一下圖形').attr({'fill' : 'blue',  'stroke': 'blue', 'stroke-width': 0.2 })
 
g = s.group().attr({'id': 'tux'})
 
def hoverover(ev):
    g.animate({'transform': 's1.5r45,t180,20'}, 1000, window.mina.bounce)
 
def hoverout(ev):
    g.animate({'transform': 's1r0,t180,20'}, 1000, window.mina.bounce) 
 
# callback 函式
def onSVGLoaded(data):
    #s.append(data)
    g.append(data)
    #g.hover(hoverover, hoverout )
    g.text(300,100, '拿滑鼠指向我')
 
# 利用 window.Snap.load 載入 svg 檔案
tux = window.Snap.load("/static/Dreaming_tux.svg", onSVGLoaded)
g.transform('t180,20')
 
# 與視窗事件對應的函式
def rtoyellow(ev):
    r.attr('fill', 'yellow')
 
def ctogreen(ev):
    c.attr('fill', 'green')
 
# 根據物件 id 綁定滑鼠事件執行對應函式
document['rect'].bind('click', rtoyellow)
document['circle'].bind('click', ctogreen)
document['tux'].bind('mouseover', hoverover)
document['tux'].bind('mouseleave', hoverout)
</script>
</body>
</html>
'''
    return outstring
 
 
@ag8_test.route('/snap_link')
# http://svg.dabbles.info/
def snap_link():
    outstring = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>網際 snap 繪圖</title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">


    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/CangoAxes-1v33.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/flintlockPartDefs-02.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/CangoAnimation-4v01.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>

 
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>
 
<svg width="800" height="800" viewBox="0 0 800 800" id="svgout"></svg>
 
<script type="text/python">
from javascript import JSConstructor
from browser import alert
from browser import window, document
 
# 透過 window 與 JSConstructor 從 Brython 物件 snap 擷取 Snap 物件的內容
snap = JSConstructor(window.Snap)
 
# 使用 id 為 "svgout" 的 svg 標註進行繪圖
s = snap("#svgout")
 
offsetY = 50
 
# 是否標訂出繪圖範圍
#borderRect = s.rect(0,0,800,640,10,10).attr({ 'stroke': "silver", 'fill': "silver", 'strokeWidth': "3" })
 
g = s.group().transform('t250,120')
r0 = s.rect(150,150,100,100,20,20).attr({ 'fill': "orange", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c0 = s.circle(225,225,10).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "4"  }).attr({ 'id': 'c0' })
g0 = s.group( r0,c0 ).attr({ 'id': 'g0' })
#g0.animate({ 'transform' : 't250,120r360,225,225' },4000)
g0.appendTo( g )
g0.animate({ 'transform' : 'r360,225,225' },4000)
# 讓 g0 可以拖動
g0.drag()
 
r1 = s.rect(100,100,100,100,20,20).attr({ 'fill': "red", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c1 = s.circle(175,175,10).attr({ 'fill': "silver", 'stroke': "black" , 'strokeWidth': "4"}).attr({ 'id': 'c1' })
g1 = s.group( r1,c1 ).attr({ 'id': 'g1' })
g1.appendTo( g0 ).attr({ 'id': 'g1' })
g1.animate({ 'transform' : 'r360,175,175' },4000)
 
r2 = s.rect(50,50,100,100,20,20).attr({ 'fill': "blue", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c2 = s.circle(125,125,10).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "4" }).attr({ 'id': 'c2' })
g2 = s.group(r2,c2).attr({ 'id': 'g2' })
 
g2.appendTo( g1 );
g2.animate( { 'transform' : 'r360,125,125' },4000);
 
r3 = s.rect(0,0,100,100,20,20).attr({ 'fill': "yellow", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c3 = s.circle(75,75,10).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "4" }).attr({ 'id': 'c3' })
g3 = s.group(r3,c3).attr({ 'id': 'g3' })
 
g3.appendTo( g2 )
g3.animate( { 'transform' : 'r360,75,75' },4000)
 
r4 = s.rect(-50,-50,100,100,20,20).attr({ 'fill': "green", 'opacity': "0.8", 'stroke': "black", 'strokeWidth': "2" })
c4 = s.circle(25,25,10).attr({ 'fill': "silver", 'stroke': "black", 'strokeWidth': "4" }).attr({ 'id': 'c4' })
g4 = s.group(r4,c4).attr({ 'id': 'g4' });
g4.appendTo( g3 )
g4.animate( { 'transform' : 'r360,25,25' },4000)
</script>
</body>
</html>
'''
    return outstring
 
 
@ag8_test.route('/snap_gear')
def snap_gear():
    outstring = '''
    
    <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title> snap </title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/CangoAxes-1v33.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/flintlockPartDefs-02.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/CangoAnimation-4v01.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>
        
<canvas id='gear1' width='800' height='750'></canvas>
 
<script type="text/python">
# 將 導入的 document 設為 doc 主要原因在於與舊程式碼相容
from browser import document as doc
# 由於 Python3 與 Javascript 程式碼已經不再混用, 因此來自 Javascript 的變數, 必須居中透過 window 物件轉換
from browser import window
# 針對 Javascript 既有的物件, 則必須透過 JSConstructor 轉換
from javascript import JSConstructor
import math
 
# 主要用來取得畫布大小
canvas = doc["gear1"]
# 此程式採用 Cango Javascript 程式庫繪圖, 因此無需 ctx
#ctx = canvas.getContext("2d")
# 針對類別的轉換, 將 Cango.js 中的 Cango 物件轉為 Python cango 物件
cango = JSConstructor(window.Cango)
# 針對變數的轉換, shapeDefs 在 Cango 中資料型別為變數, 可以透過 window 轉換
shapedefs = window.shapeDefs
# 目前 Cango 結合 Animation 在 Brython 尚無法運作, 此刻只能繪製靜態圖形
# in CangoAnimation.js
#interpolate1 = window.interpolate
# Cobi 與 createGearTooth 都是 Cango Javascript 程式庫中的物件
cobj = JSConstructor(window.Cobj)
creategeartooth = JSConstructor(window.createGearTooth)
 
# 經由 Cango 轉換成 Brython 的 cango, 指定將圖畫在 id="plotarea" 的 canvas 上
cgo = cango("gear1")
 
######################################
# 畫正齒輪輪廓
#####################################
def spur(cx,cy,m,n,pa):

    # m 為模數, 根據畫布的寬度, 計算適合的模數大小
    # Module = mm of pitch diameter per tooth

    # pr 為節圓半徑
    pr = n*m/2 # gear Pitch radius
    # generate gear
    data = creategeartooth(m, n, pa)
    # Brython 程式中的 print 會將資料印在 Browser 的 console 區
    #print(data)
    gearTooth = cobj(data, "SHAPE", {
            "fillColor":"#ddd0dd",
            "border": True,
            "strokeColor": "#606060" })
    gearTooth.rotate(180/n) # rotate gear 1/2 tooth to mesh
    # 單齒的齒形資料經過旋轉後, 將資料複製到 gear 物件中
    gear = gearTooth.dup()
    # gear 為單一齒的輪廓資料
    #cgo.render(gearTooth)
     
    # 利用單齒輪廓旋轉, 產生整個正齒輪外形
    for i in range(1, n):
        # 將 gearTooth 中的資料複製到 newTooth
        newTooth = gearTooth.dup()
        # 配合迴圈, newTooth 的齒形資料進行旋轉, 然後利用 appendPath 方法, 將資料併入 gear
        newTooth.rotate(360*i/n)
        # appendPath 為 Cango 程式庫中的方法, 第二個變數為 True, 表示要刪除最前頭的 Move to SVG Path 標註符號
        gear.appendPath(newTooth, True) # trim move command = True
     
    # 建立軸孔
    # add axle hole, hr 為 hole radius
    hr = 0.6*pr # diameter of gear shaft
    shaft = cobj(shapedefs.circle(hr), "PATH")
    shaft.revWinding()
    gear.appendPath(shaft) # retain the 'moveTo' command for shaft sub path

    gear.translate(cx, cy)
    # render 繪出靜態正齒輪輪廓
    cgo.render(gear)
    deg = math.pi/180
    Line = cobj(['M',cx,cy,'L',
	cx+pr*math.cos(180/n*deg),
	cy+pr*math.sin(180/n*deg)],"PATH",{
	'strockColor':'blue','lineWidth':4})
    cgo.render(Line)

cx = canvas.width/2
cy = canvas.height/2
# n 為齒數
n = 25
# pa 為壓力角
pa = 25
m = 0.8*canvas.width/n/5
spur(cx,cy,10,15,pa)
spur(cx-150,cy,10,15,pa)
spur(cx+150,cy,10,15,pa)


</script>
</body>
</html>
'''
    return outstring
@ag8_test.route('/snap_twogear')
def snap_twogear():
    outstring = '''
    
    <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title> snap </title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/CangoAxes-1v33.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/flintlockPartDefs-02.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/CangoAnimation-4v01.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>
        
<canvas id='gear2' width='800' height='700'></canvas>
 
<script type="text/python3">
# 導入 browser 模組中的 document, 並設為 doc 變數
from browser import document as doc
import math
# deg 為角度轉為徑度的轉換因子
deg = math.pi/180.
# 定義 Spur 類別
class Spur(object):
    def __init__(self, ctx):
        self.ctx = ctx
 
    def create_line(self, x1, y1, x2, y2, width=3, fill="red"):
        self.ctx.beginPath()
        self.ctx.lineWidth = width
        self.ctx.moveTo(x1, y1)
        self.ctx.lineTo(x2, y2)
        self.ctx.strokeStyle = fill
        self.ctx.stroke()
    #
    # 定義一個繪正齒輪的繪圖函式
    # midx 為齒輪圓心 x 座標
    # midy 為齒輪圓心 y 座標
    # rp 為節圓半徑, n 為齒數
    # pa 為壓力角 (deg)
    # rot 為旋轉角 (deg)
    # 已經針對 n 大於等於 52 齒時的繪圖錯誤修正, 因為 base circle 與齒根圓大小必須進行判斷
    def Gear(self, midx, midy, rp, n=20, pa=20, color="black"):
        # 齒輪漸開線分成 15 線段繪製
        imax = 15
        # 在輸入的畫布上繪製直線, 由圓心到節圓 y 軸頂點畫一直線
        self.create_line(midx, midy, midx, midy-rp)
        # 畫出 rp 圓, 畫圓函式尚未定義
        #create_oval(midx-rp, midy-rp, midx+rp, midy+rp, width=2)
        # a 為模數 (代表公制中齒的大小), 模數為節圓直徑(稱為節徑)除以齒數
        # 模數也就是齒冠大小
        a=2*rp/n
        # d 為齒根大小, 為模數的 1.157 或 1.25倍, 這裡採 1.25 倍
        d=2.5*rp/n
        # ra 為齒輪的外圍半徑
        ra=rp+a
        # 畫出 ra 圓, 畫圓函式尚未定義
        #create_oval(midx-ra, midy-ra, midx+ra, midy+ra, width=1)
        # rb 則為齒輪的基圓半徑
        # 基圓為漸開線長齒之基準圓
        rb=rp*math.cos(pa*deg)
        # 畫出 rb 圓 (基圓), 畫圓函式尚未定義
        #create_oval(midx-rb, midy-rb, midx+rb, midy+rb, width=1)
        # rd 為齒根圓半徑
        rd=rp-d
        # 當 rd 大於 rb 時, 漸開線並非畫至 rb, 而是 rd
        # 畫出 rd 圓 (齒根圓), 畫圓函式尚未定義
        #create_oval(midx-rd, midy-rd, midx+rd, midy+rd, width=1)
        # dr 則為基圓到齒頂圓半徑分成 imax 段後的每段半徑增量大小
        # 將圓弧分成 imax 段來繪製漸開線
        # 當 rd 大於 rb 時, 漸開線並非畫至 rb, 而是 rd
        if rd>rb:
            dr = (ra-rd)/imax
        else:
            dr=(ra-rb)/imax
        # tan(pa*deg)-pa*deg 為漸開線函數
        sigma=math.pi/(2*n)+math.tan(pa*deg)-pa*deg
        for j in range(n):
            ang=-2.*j*math.pi/n+sigma
            ang2=2.*j*math.pi/n+sigma
            lxd=midx+rd*math.sin(ang2-2.*math.pi/n)
            lyd=midy-rd*math.cos(ang2-2.*math.pi/n)
            for i in range(imax+1):
                # 當 rd 大於 rb 時, 漸開線並非畫至 rb, 而是 rd
                if rd>rb:
                    r=rd+i*dr
                else:
                    r=rb+i*dr
                theta=math.sqrt((r*r)/(rb*rb)-1.)
                alpha=theta-math.atan(theta)
                xpt=r*math.sin(alpha-ang)
                ypt=r*math.cos(alpha-ang)
                xd=rd*math.sin(-ang)
                yd=rd*math.cos(-ang)
                # i=0 時, 繪線起點由齒根圓上的點, 作為起點
                if(i==0):
                    last_x = midx+xd
                    last_y = midy-yd
                # 由左側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
                self.create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=color)
                # 最後一點, 則為齒頂圓
                if(i==imax):
                    lfx=midx+xpt
                    lfy=midy-ypt
                last_x = midx+xpt
                last_y = midy-ypt
            # the line from last end of dedendum point to the recent
            # end of dedendum point
            # lxd 為齒根圓上的左側 x 座標, lyd 則為 y 座標
            # 下列為齒根圓上用來近似圓弧的直線
            self.create_line((lxd),(lyd),(midx+xd),(midy-yd),fill=color)
            for i in range(imax+1):
                # 當 rd 大於 rb 時, 漸開線並非畫至 rb, 而是 rd
                if rd>rb:
                    r=rd+i*dr
                else:
                    r=rb+i*dr
                theta=math.sqrt((r*r)/(rb*rb)-1.)
                alpha=theta-math.atan(theta)
                xpt=r*math.sin(ang2-alpha)
                ypt=r*math.cos(ang2-alpha)
                xd=rd*math.sin(ang2)
                yd=rd*math.cos(ang2)
                # i=0 時, 繪線起點由齒根圓上的點, 作為起點
                if(i==0):
                    last_x = midx+xd
                    last_y = midy-yd
                # 由右側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
                self.create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=color)
                # 最後一點, 則為齒頂圓
                if(i==imax):
                    rfx=midx+xpt
                    rfy=midy-ypt
                last_x = midx+xpt
                last_y = midy-ypt
            # lfx 為齒頂圓上的左側 x 座標, lfy 則為 y 座標
            # 下列為齒頂圓上用來近似圓弧的直線
            self.create_line(lfx,lfy,rfx,rfy,fill=color)
 
# 準備在 id="gear2" 的 canvas 中繪圖
canvas = doc["gear2"]
ctx = canvas.getContext("2d")
x = (canvas.width)/2
y = (canvas.height)/2
r = 0.8*(canvas.width/2)
# 齒數
n = 53
# 壓力角
pa = 20
Spur(ctx).Gear(x, y, r, n, pa, "blue")
Spur(ctx).Gear(x-100, y-100, r, n, pa, "blue")
</script>
</body>
</html>
'''
    return outstring
@ag8_test.route('/snap_threeg')
def snap_threeg():
    outstring = '''
    
    <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title> snap </title>
    <!-- IE 9: display inline SVG -->
    <meta http-equiv="X-UA-Compatible" content="IE=9">
    <script type="text/javascript" src="http://brython.info/src/brython_dist.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango-8v03.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/Cango2D-7v01-min.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/CangoAxes-1v33.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/flintlockPartDefs-02.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/CangoAnimation-4v01.js"></script>

    <script type="text/javascript" src="http://2015fallhw.github.io/cptocadp/static/gearUtils-05.js"></script>
    <script>
    window.onload=function(){
    brython(1);
    }
    </script>
</head>
<body>


<canvas id='gear3' width='800' height='400'></canvas>
 
<script type="text/python3">
# 導入 browser 模組中的 document, 並設為 doc 變數
from browser import document as doc
import math
# deg 為角度轉為徑度的轉換因子
deg = math.pi/180.
# 定義 Spur 類別
class Spur(object):
    def __init__(self, ctx):
        self.ctx = ctx
 
    def create_line(self, x1, y1, x2, y2, width=3, fill="red"):
        self.ctx.beginPath()
        self.ctx.lineWidth = width
        self.ctx.moveTo(x1, y1)
        self.ctx.lineTo(x2, y2)
        self.ctx.strokeStyle = fill
        self.ctx.stroke()
    #
    # 定義一個繪正齒輪的繪圖函式
    # midx 為齒輪圓心 x 座標
    # midy 為齒輪圓心 y 座標
    # rp 為節圓半徑, n 為齒數
    # pa 為壓力角 (deg)
    # rot 為旋轉角 (deg)
    # 已經針對 n 大於等於 52 齒時的繪圖錯誤修正, 因為 base circle 與齒根圓大小必須進行判斷
    def Gear(self, midx, midy, rp, n=20, pa=20, color="black"):
        # 齒輪漸開線分成 15 線段繪製
        imax = 15
        # 在輸入的畫布上繪製直線, 由圓心到節圓 y 軸頂點畫一直線
        self.create_line(midx, midy, midx, midy-rp)
        # 畫出 rp 圓, 畫圓函式尚未定義
        #create_oval(midx-rp, midy-rp, midx+rp, midy+rp, width=2)
        # a 為模數 (代表公制中齒的大小), 模數為節圓直徑(稱為節徑)除以齒數
        # 模數也就是齒冠大小
        a=2*rp/n
        # d 為齒根大小, 為模數的 1.157 或 1.25倍, 這裡採 1.25 倍
        d=2.5*rp/n
        # ra 為齒輪的外圍半徑
        ra=rp+a
        # 畫出 ra 圓, 畫圓函式尚未定義
        #create_oval(midx-ra, midy-ra, midx+ra, midy+ra, width=1)
        # rb 則為齒輪的基圓半徑
        # 基圓為漸開線長齒之基準圓
        rb=rp*math.cos(pa*deg)
        # 畫出 rb 圓 (基圓), 畫圓函式尚未定義
        #create_oval(midx-rb, midy-rb, midx+rb, midy+rb, width=1)
        # rd 為齒根圓半徑
        rd=rp-d
        # 當 rd 大於 rb 時, 漸開線並非畫至 rb, 而是 rd
        # 畫出 rd 圓 (齒根圓), 畫圓函式尚未定義
        #create_oval(midx-rd, midy-rd, midx+rd, midy+rd, width=1)
        # dr 則為基圓到齒頂圓半徑分成 imax 段後的每段半徑增量大小
        # 將圓弧分成 imax 段來繪製漸開線
        # 當 rd 大於 rb 時, 漸開線並非畫至 rb, 而是 rd
        if rd>rb:
            dr = (ra-rd)/imax
        else:
            dr=(ra-rb)/imax
        # tan(pa*deg)-pa*deg 為漸開線函數
        sigma=math.pi/(2*n)+math.tan(pa*deg)-pa*deg
        for j in range(n):
            ang=-2.*j*math.pi/n+sigma
            ang2=2.*j*math.pi/n+sigma
            lxd=midx+rd*math.sin(ang2-2.*math.pi/n)
            lyd=midy-rd*math.cos(ang2-2.*math.pi/n)
            for i in range(imax+1):
                # 當 rd 大於 rb 時, 漸開線並非畫至 rb, 而是 rd
                if rd>rb:
                    r=rd+i*dr
                else:
                    r=rb+i*dr
                theta=math.sqrt((r*r)/(rb*rb)-1.)
                alpha=theta-math.atan(theta)
                xpt=r*math.sin(alpha-ang)
                ypt=r*math.cos(alpha-ang)
                xd=rd*math.sin(-ang)
 
                yd=rd*math.cos(-ang)
                # i=0 時, 繪線起點由齒根圓上的點, 作為起點
                if(i==0):
                    last_x = midx+xd
                    last_y = midy-yd
                # 由左側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
                self.create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=color)
                # 最後一點, 則為齒頂圓
                if(i==imax):
                    lfx=midx+xpt
                    lfy=midy-ypt
                last_x = midx+xpt
                last_y = midy-ypt
            # the line from last end of dedendum point to the recent
            # end of dedendum point
            # lxd 為齒根圓上的左側 x 座標, lyd 則為 y 座標
            # 下列為齒根圓上用來近似圓弧的直線
            self.create_line((lxd),(lyd),(midx+xd),(midy-yd),fill=color)
            for i in range(imax+1):
                # 當 rd 大於 rb 時, 漸開線並非畫至 rb, 而是 rd
                if rd>rb:
                    r=rd+i*dr
                else:
                    r=rb+i*dr
                theta=math.sqrt((r*r)/(rb*rb)-1.)
                alpha=theta-math.atan(theta)
                xpt=r*math.sin(ang2-alpha)
                ypt=r*math.cos(ang2-alpha)
                xd=rd*math.sin(ang2)
                yd=rd*math.cos(ang2)
                # i=0 時, 繪線起點由齒根圓上的點, 作為起點
                if(i==0):
                    last_x = midx+xd
                    last_y = midy-yd
                # 由右側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
                self.create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=color)
                # 最後一點, 則為齒頂圓
                if(i==imax):
                    rfx=midx+xpt
                    rfy=midy-ypt
                last_x = midx+xpt
                last_y = midy-ypt
            # lfx 為齒頂圓上的左側 x 座標, lfy 則為 y 座標
            # 下列為齒頂圓上用來近似圓弧的直線
            self.create_line(lfx,lfy,rfx,rfy,fill=color)
 
# 準備在 id="gear3" 的 canvas 中繪圖
canvas = doc["gear3"]
ctx = canvas.getContext("2d")
 
# 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
# 壓力角 pa 單位為角度
pa = 20
# 第1齒輪齒數
n_g1 = 17
# 第2齒輪齒數
n_g2 = 11
# 第3齒輪齒數
n_g3 = 13
# m 為模數, 根據畫布的寬度, 計算適合的模數大小
m = (0.8*canvas.width)/(n_g1+n_g2+n_g3)
# 根據模數 m, 計算各齒輪的節圓半徑
rp_g1 = m*n_g1/2
rp_g2 = m*n_g2/2
rp_g3 = m*n_g3/2
#單一正齒輪繪圖呼叫格式 Spur(ctx).Gear(x, y, r, n, pa, "blue")
# 開始繪製囓合齒輪輪廓
# 繪圖第1齒輪的圓心座標, 因為希望繪圖佔去 canvas.width 的 80%, 所以兩邊各預留 10% 距離
x_g1 = canvas.width*0.1+rp_g1
# y 方向繪圖區域上方預留 canvas.height 的 20%
y_g1 = canvas.height*0.2+rp_g1
# 第2齒輪的圓心座標, 假設排列成水平, 表示各齒輪圓心 y 座標相同
x_g2 = x_g1 + rp_g1 + rp_g2
y_g2 = y_g1
# 第3齒輪的圓心座標
x_g3 = x_g1 + rp_g1 + 2*rp_g2 + rp_g3
y_g3 = y_g1
 
# 將第1齒輪順時鐘轉 90 度, 也就是 math.pi/2
# 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
ctx.save()
# translate to the origin of second gear
ctx.translate(x_g1, y_g1)
# rotate to engage
ctx.rotate(math.pi/2)
# put it back
ctx.translate(-x_g1, -y_g1)
# 繪製第一個齒輪輪廓
Spur(ctx).Gear(x_g1, y_g1, rp_g1, n_g1, pa, "blue")
ctx.restore()
 
# 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
ctx.save()
# translate to the origin of second gear
ctx.translate(x_g2, y_g2)
# rotate to engage
ctx.rotate(-math.pi/2-math.pi/n_g2)
# put it back
ctx.translate(-x_g2, -y_g2)
Spur(ctx).Gear(x_g2, y_g2, rp_g2, n_g2, pa, "black")
ctx.restore()
 
# 將第3齒輪逆時鐘轉 90 度之後, 再往回轉第2齒輪定位帶動轉角, 然後再逆時鐘多轉一齒, 以便與第2齒輪進行囓合
ctx.save()
# translate to the origin of second gear
ctx.translate(x_g3, y_g3)
# rotate to engage
# math.pi+math.pi/n_g2 為第2齒輪從順時鐘轉 90 度之後, 必須配合目前的標記線所作的齒輪 2 轉動角度, 要轉換到齒輪3 的轉動角度
# 必須乘上兩齒輪齒數的比例, 若齒輪2 大, 則齒輪3 會轉動較快
# 第1個 -math.pi/2 為將原先垂直的第3齒輪定位線逆時鐘旋轉 90 度
# -math.pi/n_g3 則是第3齒與第2齒定位線重合後, 必須再逆時鐘多轉一齒的轉角, 以便進行囓合
# (math.pi+math.pi/n_g2)*n_g2/n_g3 則是第2齒原定位線為順時鐘轉動 90 度, 
# 但是第2齒輪為了與第1齒輪囓合, 已經距離定位線, 多轉了 180 度, 再加上第2齒輪的一齒角度, 因為要帶動第3齒輪定位, 
# 這個修正角度必須要再配合第2齒與第3齒的轉速比加以轉換成第3齒輪的轉角, 因此乘上 n_g2/n_g3
ctx.rotate(-math.pi/2-math.pi/n_g3+(math.pi+math.pi/n_g2)*n_g2/n_g3)
# put it back
ctx.translate(-x_g3, -y_g3)
Spur(ctx).Gear(x_g3, y_g3, rp_g3, n_g3, pa, "red")
ctx.restore()
</script>
</body>
</html>
'''
    return outstring

