
import os
import mysql.connector
import time
import wx
wildcard = "Reports (*.dat)|*.dat|" \
            "All files (*.*)|*.*"
class MyForm(wx.Frame):
 #----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, None, -1,"REPORT COMPARISON", size=(1000, 400))	                          
		panel = wx.Panel(self, wx.ID_ANY)
		self.currentDirectory = os.getcwd()
		self.Centre()

		self.compared = 'false'
 
       		# create the buttons and bindings
		self.browse1 = wx.Button(panel, label="Select report 1", pos=(295, 50), size=(400, 25))
		self.browse1.Bind(wx.EVT_BUTTON, self.get_report1)
		
		self.browse2 = wx.Button(panel, label="Select report 2", pos=(295, 100), size=(400, 25))
		self.browse2.Bind(wx.EVT_BUTTON, self.get_report2)

		self.compare = wx.Button(panel, label="COMPARE", pos=(295, 200), size=(400, 25))
		self.compare.Bind(wx.EVT_BUTTON, self.on_compare)

		self.diff = wx.Button(panel, label="DIFFERENCES", pos=(300, 250), size=(100, 25))
		self.diff.Bind(wx.EVT_BUTTON, self.on_diff)


		self.common = wx.Button(panel, label="SIMILARITIES", pos=(600, 250), size=(100, 25))
		self.common.Bind(wx.EVT_BUTTON, self.on_common)

		self.cls= wx.Button(panel, label="Close", pos=(450, 310), size=(100, 25))
		self.cls.Bind(wx.EVT_BUTTON, self.on_close)

		self.diff.Hide()
		self.common.Hide()		

		self.path1 = 'Report1 not chosen'
		self.path2 = 'Report2 not chosen'     




	def get_report1(self, event):
		dlg1 = wx.FileDialog(
            		self, message="Choose Report 1",
            		defaultDir=self.currentDirectory, 
            		defaultFile="",
            		wildcard=wildcard,
            		style=wx.FD_OPEN |wx.FD_FILE_MUST_EXIST
            		)
    
		if dlg1.ShowModal() == wx.ID_OK:
            			self.path1 = dlg1.GetPath()
		else :
			self.path1 = 'Report1 not chosen'
		dlg1.Destroy()
		self.browse1.SetLabel(self.path1) 

	def get_report2(self, event):
		dlg2 = wx.FileDialog(
            		self, message="Choose Report 2",
            		defaultDir=self.currentDirectory, 
            		defaultFile="",
            		wildcard=wildcard,
            		style=wx.FD_OPEN |wx.FD_FILE_MUST_EXIST
            		)
    
		if dlg2.ShowModal() == wx.ID_OK:
            			self.path2 = dlg2.GetPath()
		else :
              			self.path2 = 'Report2 not chosen'

		dlg2.Destroy()
		self.browse2.SetLabel(self.path2) 
	
	def on_compare(self, event):
		if self.path1 != 'Report1 not chosen' and self.path2 != 'Report2 not chosen' and self.path1 != self.path2 :
			wait = wx.BusyInfo("PLEASE WAIT. COMPARING THE REPORTS")
			time.sleep(1)
			del wait
			self.compared = 'true'
			fn11 = self.path1
			fn22 = self.path2
			print('Report 1 : '+fn11)
			print('Report 2 : '+fn22)
			d = "truncate table report1"
			db = mysql.connector.connect(user='root', password='aparsql', host='localhost', database='report_comparison')
			cur = db.cursor()
			cur.execute(d)
			with open(fn11) as f :
				for x in f :
					check = x[2:11]
					exte = x[len(x)-4:len(x)-1]
					rep = x[0:8]
					if rep == '* Report' :
						self.report1 = x[9:len(x)]
#						print('\nProcessing Report 1 : '+self.report1)
					if check == 'SW_Module' and exte == 'CRI':				
						y=x.find("=")
						key = x[2:y]
						value = x[y+1:len(x)]
						query = "insert into report1(id, name) values(%s, %s)"
						val = (key, value)
						cur.execute(query, val)
			f.close()
			db.commit()
			db.close()
	
		#FETCH MODULES AND STORE IN DETAILS 1
			print('Processing the reports')
			qn = "select name from report1"
			dd = "truncate table details1"
			db = mysql.connector.connect(user='root', password='aparsql', host='localhost', database='report_comparison')
			cur = db.cursor()
			cur.execute(dd)
			cur.execute(qn)
			data = cur.fetchall()
			for row in data:
				mod = row[0]
				mod = mod[0:len(mod)-1]
				location = 'Z:/img/'+mod
				n = t = o = s = d = v = r = h = m = 'NA\n'
				with open(location) as fd1 :
					for x in fd1 :
						y=x.find("=")
						check = x[0:y]
						valu = x[y+1:len(x)]
						if check == 'ModuleThis' :
							n = valu
						if check == 'ModuleSize' :
							s = valu
						if check == 'Description' :
							d = valu
						if check == 'OS' :
							o = valu
						if check == 'Type' :
							t = valu
						if check == 'Version' :
							v = valu	
						if check == 'RecoveryCD' :
							r = valu
						if check == 'HIITModule' :
							h = valu
						if check == 'MLPS' :
							m = valu
				

				query1 = "insert into details1(name, type, os, size, des, ver, rcd, hiit, mlps) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
				values1 = (n, t, o, s, d, v, r, h, m)
				cur.execute(query1, values1)
				fd1.close()
			db.commit()
			db.close()
			


		#DO FOLLOWING FOR VALID REPORT2

		#STORE INTO REPORT2 TABLE


			d1 = "truncate table report2"
			db1 = mysql.connector.connect(user='root', password='aparsql', host='localhost', database='report_comparison')
			cur1 = db1.cursor()
			cur1.execute(d1)
			with open(fn22) as f1 :
				for x in f1 :
					check = x[2:11]
					exte = x[len(x)-4:len(x)-1]
					rep2 = x[0:8]
					if rep2 == '* Report' :
						self.report2 = x[9:len(x)]
#						print('Processing Report 2 : '+self.report2)
					if check == 'SW_Module' and exte == 'CRI':
						y=x.find("=")
						key1 = x[2:y]
						value1 = x[y+1:len(x)]
						query1 = "insert into report2(id, name) values(%s, %s)"
						val1 = (key1, value1)
						cur1.execute(query1, val1)
			f1.close()
			db1.commit()
			db1.close()

		#FETCH MODULES AND STORE IN DETAILS 2
	
			qn = "select name from report2"
			dd = "truncate table details2"
			db = mysql.connector.connect(user='root', password='aparsql', host='localhost', database='report_comparison')
			cur = db.cursor()
			cur.execute(dd)
			cur.execute(qn)
			data = cur.fetchall()
			for row in data:
				mod = row[0]
				mod = mod[0:len(mod)-1]
				location = 'Z:/img/'+mod
				n = t = o = s = d = v = r = h = m = 'NA\n'
				with open(location) as fd1 :
					for x in fd1 :
						y=x.find("=")
						check = x[0:y]
						valu = x[y+1:len(x)]
						if check == 'ModuleThis' :
							n = valu
						if check == 'ModuleSize' :
							s = valu
						if check == 'Description' :
							d = valu
						if check == 'OS' :	
							o = valu
						if check == 'Type' :
							t = valu
						if check == 'Version' :
							v = valu	
						if check == 'RecoveryCD' :
							r = valu
						if check == 'HIITModule' :
							h = valu
						if check == 'MLPS' :
							m = valu
				

				query1 = "insert into details2(name, type, os, size, des, ver, rcd, hiit, mlps) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
				values1 = (n, t, o, s, d, v, r, h, m)
				cur.execute(query1, values1)
				fd1.close()
			db.commit()
			db.close()
			print('Comparison done Successfully')
			self.diff.Show()
			self.common.Show()

		else :
			no_input = wx.BusyInfo("PLEASE SELECT 2 DISTINCT REPORT FILES TO BE COMPARED")
			time.sleep(0.80)
			del no_input
		

	#	OUTPUT CHOICES


	def on_common(self, event) :
		if self.path1 != 'Report1 not chosen' and self.path2 != 'Report2 not chosen' and self.path1 != self.path2 and self.compared == 'true' :
			fout = open('Result.txt', 'w')
			fout.flush()
			fout.write("====COMMON MODULES===\n")
			com = 'select details1.id, details1.name, details1.type, details1.os, details1.size, details1.des, details1.ver, details1.rcd, details1.hiit, details1.mlps from details1 inner join details2 on details1.name = details2.name'
			db = mysql.connector.connect(user = 'root', password = 'aparsql', host = 'localhost', database = 'report_comparison')
			cur = db.cursor()
			cur.execute(com)
			count = 0
			for row in cur.fetchall() :
				count = count+1
				fout.write("\n"+str(count)+"\nModule : "+row[1]+"Type : "+row[2]+"OS : "+row[3]+"Size : "+row[4]+"Description : "+row[5]+"Version : "+row[6])	
	
			db.close()
			fout.close()
			os.startfile('Result.txt')
			
		else :
			no_input = wx.BusyInfo("PLEASE SELECT 2 DISTINCT REPORT FILES TO BE COMPARED")
			time.sleep(0.80)
			del no_input

		
			


			
	def on_diff(self, event) :
		if self.path1 != 'Report1 not chosen' and self.path2 != 'Report2 not chosen' and self.path1 != self.path2 and self.compared == 'true':
				
				fout = open('Result.txt', 'w')
				fout.flush()
				fout.write("====MODIFICATIONS====\n")
				fout.write('##########################\n\n'+self.report1[0:len(self.report1)-1]+'  >>>>  '+self.report2[0:len(self.report2)-1]+'\n###############################################################\n')
				com = 'select * from details1 inner join details2 on details1.name != details2.name and details1.des = details2.des'
				db = mysql.connector.connect(user = 'root', password = 'aparsql', host = 'localhost', database = 'report_comparison')
				cur = db.cursor()
				cur.execute(com)
				count = 0
				for row in cur.fetchall() :
					count = count+1
					fout.write('\n'+str(count)+'\nMODULE  ::::  '+row[1][0:len(row[1])-1]+' <=> '+row[11]+'TYPE  :   '+row[2][0:len(row[2])-1]+' <=> '+row[12]+'OS  :  '+row[3][0:len(row[3])-1]+' <=> '+row[13]+'Size  :  '+row[4][0:len(row[4])-1]+' <=> '+row[14]+'Description  :  '+row[5][0:len(row[5])-1]+'\nVersion  :  '+row[6][0:len(row[6])-1]+' <=> '+row[16])
				db.close()
				fout.write("\n\n====MODULES UNIQUE TO : "+self.report1[0:len(self.report1)-1]+" ====\n#####################################################################")
				com = 'select * from details1  where not exists (select * from details2 where details2.name = details1.name or details2.des = details1.des)'
				db = mysql.connector.connect(user = 'root', password = 'aparsql', host = 'localhost', database = 'report_comparison')
				cur = db.cursor()
				cur.execute(com)
				count = 0
				for row in cur.fetchall() :
					count = count+1
					fout.write('\n'+str(count)+'\nMODULE  :  : '+row[1]+'Type : '+row[2]+'OS : '+row[3]+'Size : '+row[4]+'Description : '+row[5]+'Version : '+row[6])	
				db.close()
				if str(count) == '0' :
					fout.write("\n===TOTAL NUMBER OF UNIQUE MODULES :  "+str(count)+"===\n")
				fout.write("\n\n====MODULES UNIQUE TO : "+self.report2[0:len(self.report2)-1]+" ====\n#####################################################################")
				com = 'select * from details2  where not exists (select * from details1 where details1.name = details2.name or details1.des = details2.des)'
				db = mysql.connector.connect(user = 'root', password = 'aparsql', host = 'localhost', database = 'report_comparison')
				cur = db.cursor()
				cur.execute(com)
				count = 0
				for row in cur.fetchall() :
					count = count+1
					fout.write('\n'+str(count)+'\nMODULE  : '+row[1]+'Type : '+row[2]+'OS : '+row[3]+'Size : '+row[4]+'Description : '+row[5]+'Version : '+row[6])	
				db.close()
				if str(count) == '0' :
					fout.write("\n===TOTAL NUMBER OF UNIQUE MODULES :  "+str(count)+"===\n")
				fout.close()

				os.startfile('Result.txt')
		else :
			no_input = wx.BusyInfo("PLEASE SELECT 2 DISTINCT REPORT FILES TO BE COMPARED")
			time.sleep(0.80)
			del no_input
			
	def on_close(self, event) :
		try : 
			os.remove('Result.txt')
		except :
#			print('no result file')
#			time.sleep(0.0000001)
			self.Close()

		finally :
			lastdel1 = "truncate table details1"
			lastdel2 = "truncate table details2"
			db = mysql.connector.connect(user='root', password='aparsql', host='localhost', database='report_comparison')
			cur = db.cursor()
			cur.execute(lastdel1)
			cur.execute(lastdel2)
			self.Close()



# Run the program

if __name__ == "__main__":
	app = wx.App(False)
	frame = MyForm()
	frame.Show()
	app.MainLoop()
 
