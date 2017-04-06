from tkinter import *
from yahoo_finance import Share
import time
import statistics
import MySQLdb
import feedparser

class portfolio:
	def __init__(self,sqlHost,sqlUser,passwd,dab):	
		db = MySQLdb.connect(host=sqlHost,user=sqlUser,passwd=passwd,db=dab)  
		cur = db.cursor()	
		self.contents = []

		cur.execute("SELECT * FROM portfolio")
		for row in cur.fetchall():
			sqlsymbol = row[0]
			sqlpriceBought = row[2]
			sqlcountBought = row[3]
			sqldateBought = row[1]
			name = stock(sqlsymbol,sqlpriceBought,sqlcountBought,sqldateBought)
			self.contents.append(name);
		db.close()
		self.number = len(self.contents)

class stock:
    def __init__(self, symbol, priceBought, countBought, dateBought):
        self.symbol = symbol
        self.priceBought =  priceBought
        self.countBought = countBought
        self.dateBought = dateBought
        yhoEntity = Share(self.symbol)
       	self.currPrice =  float(yhoEntity.get_price())
	
			
    def setThresh(self,inputBox):
    	self.threshold = inputBox    
#end of stock class

class subSetScreen:
	def __init__(self,freeH,freeW):
		self.freeH = freeH
		self.freeW = freeW
#end of screen object

class chart:
	def __init__(self,symbol,subSetScreen):
		self.symbol = symbol
		self.width = subSetScreen.freeW
		self.height = subSetScreen.freeH

	def drawChart(self):
		#setup data stream
		label = self.symbol
		now = (time.strftime("%Y-%m-%d"))
		yahooObject = Share(self.symbol)
		dataStream = yahooObject.get_historical(str('2015-01-01'),str(now))
		currPrice = yahooObject.get_price()
		fullName = yahooObject.get_name()
		
		#setup graphics
		x_interval = (self.width/len(dataStream))
		
		#start a lof of data operations to normalize the data points
		chartData = normalizeData(dataStream,self.height)

		#declare canvas 1/2 of width
		w = Canvas(root, width=(self.width), height=self.height,bg = "black",bd = 2)

		startX = 0
		startY=chartData[0]

		for value in chartData:
			endY = value
			endX = startX + x_interval
			if (startY>endY):
				color = "green"
			else: 
				color = "red"
			w.create_line(startX, startY, endX, endY, fill=color,  smooth="true", width = 3)
			startX = endX
			startY = endY
		
		avg = float(sum(chartData))/len(chartData)
		w.create_text(self.width/3, avg,  text=fullName + " " + currPrice, font = "Helvetica", fill = "white")
		w.grid(column=0)

#end of chart class

class currPriceColumn:
	def __init__(self,portfolio,subSetScreen):
		self.portfolio = portfolio
		self.width = subSetScreen.freeW
		self.height = subSetScreen.freeH
	

	def drawColumn(self):	
		for name in self.portfolio.contents:	
			color = "RED"
			if	(name.currPrice>name.threshold):
				color = "GREEN"
			if (thresh == 0):
				color = "GREY"	

	
	




def normalizeData(revDataStream,maxh):

	targetList = []
	for x in range(len(revDataStream)-1,-1,-1):
		targetList.append(float(revDataStream[x]["Close"]))
	
	diff = float(max(targetList)) - float(min(targetList))

	normChartData = []

	for x in targetList:
		normChartData.append(float((float(x)-float(min(targetList)))/diff))

	for x in range(0,len(targetList),1):
		targetList[x]=maxh - (normChartData[x] * maxh )
	return targetList


#eof

root = Tk()
root.title('Mariposa - stock keeping')


my_portfolio = portfolio("localhost","root","wasabi1212","aurora")

myscreen = subSetScreen((root.winfo_screenheight()/(my_portfolio.number))*.8,root.winfo_screenwidth()/3	)

for stock in my_portfolio.contents:
	smallchart = chart(stock.symbol,myscreen)
	smallchart.drawChart()
#

col1 = currPriceColumn(my_portfolio,myscreen)
root.mainloop()

