var tipuesearch = {"pages":[{"url":"http://ddss-40323123.rhcloud.com/static/blog/40323123-cdw18-qi-mo-bao-gao.html","title":"40323123 cdw18 期末報告","text":"前言: 在設定上的問題會以及Onshape的設定會有許多問題，要一一仔細的檢查，不然就無法讓齒輪旋轉。 利用2D軟體進行輔助，進行圖解，讓我們可以算出他的切線的角度，以及該連接的角度 建立github協同倉儲以及增加協同帳號 修改readme.md檔 2D鏈輪設計 先用圖解法算出切線和圓心大小，以利程式設計 程式碼: def realcircle(x, y): # 20 為鏈條兩圓距 # chain 所圍之圓圈半徑為 20/2/math.asin(degree*math.pi/180/2) # degree = math.asin(20/2/radius)*180/math.pi x = 50 y = 0 degree = 12 # 78, 66, 54, 42, 30, 18, 6度 #必須有某些 chain 算座標但是不 render first_degree = 90 - degree repeat = 360 / degree # 第1節也是 virtual chain outstring = ''' mychain = chain() x1, y1 = mychain.basic_rot('''+str(x)+\",\"+str(y)+\", \"+str(first_degree)+''', True) #x1, y1 = mychain.basic_rot('''+str(x)+\",\"+str(y)+\", \"+str(first_degree)+''') ''' # 這裡要上下各多留一節虛擬 chain, 以便最後進行連接 (x7, y7) 與 (x22, y22) for i in range(2, int(repeat)+1): #if i < 7 or i > 23: if i <= 3 or i >= 22: # virautl chain outstring += \"x\"+str(i)+\", y\"+str(i)+\"=mychain.basic_rot(x\"+str(i-1)+\", y\"+str(i-1)+\", 90-\"+str(i*degree)+\",True) \\n\" #outstring += \"x\"+str(i)+\", y\"+str(i)+\"=mychain.basic_rot(x\"+str(i-1)+\", y\"+str(i-1)+\", 90-\"+str(i*degree)+\") \\n\" else: outstring += \"x\"+str(i)+\", y\"+str(i)+\"=mychain.basic_rot(x\"+str(i-1)+\", y\"+str(i-1)+\", 90-\"+str(i*degree)+\") \\n\" p = -150 k = 0 degree = 20 # 70, 50, 30, 10 # 從 i=5 開始, 就是 virautl chain first_degree = 90 - degree repeat = 360 / degree # 第1節不是 virtual chain outstring += ''' #mychain = chain() p1, k1 = mychain.basic_rot('''+str(p)+\",\"+str(k)+\", \"+str(first_degree)+''') ''' for i in range(2, int(repeat)+1): if i >= 7 and i <= 15: # virautl chain outstring += \"p\"+str(i)+\", k\"+str(i)+\"=mychain.basic_rot(p\"+str(i-1)+\", k\"+str(i-1)+\", 90-\"+str(i*degree)+\", True) \\n\" #outstring += \"p\"+str(i)+\", k\"+str(i)+\"=mychain.basic_rot(p\"+str(i-1)+\", k\"+str(i-1)+\", 90-\"+str(i*degree)+\") \\n\" else: outstring += \"p\"+str(i)+\", k\"+str(i)+\"=mychain.basic_rot(p\"+str(i-1)+\", k\"+str(i-1)+\", 90-\"+str(i*degree)+\") \\n\" s = -97 t = 124.5 degree = 12 # 70, 50, 30, 10 # 從 i=5 開始, 就是 virautl chain first_degree = 90 - degree repeat = 360 / degree # 第1節不是 virtual chain outstring += ''' #mychain = chain() s1, t1 = mychain.basic_rot('''+str(s)+\",\"+str(t)+\", \"+str(first_degree)+''',True) #x1, y1 = mychain.basic_rot('''+str(x)+\",\"+str(y)+\", \"+str(first_degree)+''') ''' for i in range(2, int(repeat)+1): if i <= 18 or i >= 26: # virautl chain outstring += \"s\"+str(i)+\", t\"+str(i)+\"=mychain.basic_rot(s\"+str(i-1)+\", t\"+str(i-1)+\", 90-\"+str(i*degree)+\",True) \\n\" else: outstring += \"s\"+str(i)+\", t\"+str(i)+\"=mychain.basic_rot(s\"+str(i-1)+\", t\"+str(i-1)+\", 90-\"+str(i*degree)+\") \\n\" a = -180 b = 101 degree = 5 # 70, 50, 30, 10 # 從 i=5 開始, 就是 virautl chain first_degree = 90 - degree repeat = 360 / degree # 第1節不是 virtual chain outstring += ''' #mychain = chain() a1, b1 = mychain.basic_rot('''+str(a)+\",\"+str(b)+\", \"+str(first_degree)+''',True) ''' for i in range(2, int(repeat)+1): if i <= 47 or i >= 65: # virautl chain outstring += \"a\"+str(i)+\", b\"+str(i)+\"=mychain.basic_rot(a\"+str(i-1)+\", b\"+str(i-1)+\", 90-\"+str(i*degree)+\",True) \\n\" #outstring += \"x\"+str(i)+\", y\"+str(i)+\"=mychain.basic_rot(x\"+str(i-1)+\", y\"+str(i-1)+\", 90-\"+str(i*degree)+\") \\n\" else: outstring += \"a\"+str(i)+\", b\"+str(i)+\"=mychain.basic_rot(a\"+str(i-1)+\", b\"+str(i-1)+\", 90-\"+str(i*degree)+\") \\n\" return outstring 實際狀況 Onshape 3D 齒輪協同設計 先導入齒輪的Feacture script 然後定義兩個齒輪 ※注意模數和齒輪圓的大小，以及偏移的角度 設計一個齒輪座 最後進行組裝和模擬轉動 心得: 今天算是期末測驗，因為可以考驗大家平時的努力和成果，是否都是抄襲或者複製，這樣可以保障想要拿高分的人，的分數，在時間的壓力下，才發現協同的重要性，大家同時間平行運算，才可以平行運算，當作電腦，一樣可以，很快的表達出答案和設計的結果。","tags":"ag8"},{"url":"http://ddss-40323123.rhcloud.com/static/blog/xie-tong-chan-pin-she-ji-shi-xi-qi-mo-kao-zhou-zhuan-an-bao-gao.html","title":"協同產品設計實習期末考週專案報告","text":"為了能夠更客觀進行各組與各學員的期末自評, 特別以組為單位, 各組員為內容建構成員, 利用四堂課程的時間, 在各組新建的 Github 倉儲中完成此一專案報告. 基本專案建置流程: 請各組推派代表, 在其 Github 帳號下, 建立一個分組期末專案倉儲, 倉儲名稱定為 2016springcd_aG1, 其中的 aG1 代表 a 班的第 1 組 (以下將以 2016springcd_xGx 代表各組建立的倉儲名稱), 請各組自行配合改為各自的組別代號, 而且請各組特別注意, 此一倉儲的建立時間, 必須是在各班期末考週的第1堂課程時間之後建立, 才納入計分. 倉儲建立之後的第1階段提交推送資料, 必須是修改 README.md, 而且必須透過協調, 由各組員依序 git clone 各組在代表組員帳號下所建立的 2016springcd_xGx 倉儲後, 分別由各組員自行用學號登錄的 github 帳號以協同提交推送的過程, 各自修改 README.md 檔案, 將自己的學號與個人對應的 Github Page 網頁, 放入 REAEME.md 檔案中. 第2項的評分依據為各組員必須自行用自己在 Github 登錄的帳號, 取得各組的 2016springcd_xGx 倉儲協同權限後, 再進行 RADEME.md 的協同修改, 之後各組員完成提交推送的紀錄, 必須可以在 commits 呈現各自的學號與提交推送內容及時間, 才納入計分. 各組以協同流程完成 README.md 的編修後, 接著請取用 https://github.com/2015fallhw/2016springcd_final 倉儲中的架構, 在各組的代表成員的 2016springcd_xGx 倉儲中運作, 並設法將其中的 pelican 網誌內容, 呈現在 2016springcd_xGx 倉儲的 gh-pages 分支中, 完成後, 請各組員在此一 gh-pages 倉儲中各自建立一個能夠呈現自我期末報告的網誌, 並且將此一在 2016springcd_xGx 倉儲的 gh-pages 分支中的連結, 放入 2016springcd_xGx 倉儲 master 分支的 README.md 最前方. 接著, 請利用協同產品設計實習課程所學到的 2D 網際繪圖內容, 以分組組員各自繪製一簡單幾何零件圖形的方式, 將 2016springcd_xGx 倉儲資料中的 wsgi 程式, 送到各組代表成員的 OpenShift 網站中呈現, 並將 2D 繪圖程式連結, 放到 2016springcd_xGx 倉儲 master 分支的 README.md 資料中, 並且放在分組 gh-pages 連結之後. 最後, 請各組以協同方式在 Onshape 雲端電腦輔助設計軟體中, 建立一個名稱為 2016springcd_xGx 的公開協同 Document, 然後將各組組員納入作為可以 edit 與 view 的協同者, 以每一位組員利用 Onshape 官方所釋出的 SG (正齒輪) FeatureScript, 分別依照學號排序, 從齒數 17 開始, 以每位學員遞增 2 齒的方式, 各自在 Part Studio 建立一個正齒輪零件, 並以學號命名零件後, 完成後, 以最簡單的方式在以組別 xGx 命名的組立件中完成囓合組立 (例如, 該組有 6 位成員, 則各自提供一個正齒輪零件, 齒數分別為 17, 19, 21, 23, 25, 27 等, 最後則完成6個齒輪的囓合組立), 完成後, 請將各組的囓合正齒輪組立件以 share 功能, 設定成網路公開組立件, 並將此一 Onshape 的組立件連結, 放到 2016springcd_xGx 倉儲 master 分支的 README.md 資料中, 放在分組 wsgi 2D 繪圖連結之後. 最最後, 請各組依序完成上述工作任務後, 將各組與各學員所完成的網站連結放入 https://github.com/2015fallhw/cdw11/wiki 各組員的對應資料區中, 以作為期末成績評分參考. 祝大家 2016 Summer 假期愉快!","tags":"ag100"}]};