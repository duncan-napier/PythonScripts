import wx
import wx.adv
import sqlite3, sys
import datetime, dateutil.parser
from math import sqrt

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


db_file = ""
devices = []

global USE_DATEPICKERCTRL
USE_DATEPICKERCTRL = 1

def distance( x0, y0, x1, y1 ):
	dist = sqrt( pow( x1 - x0, 2 ) + pow( y1 - y0, 2 ) )
	return dist


#
#	lineColour
#
def lineColour( method_desc ):

	if method_desc == 'Car' or method_desc == 'CarPetrolSmall':
		return 'red'
	elif method_desc == 'Bicycle': 
		return 'green'
	elif method_desc == 'Bus':
		return 'blue'
	elif method_desc == 'InternationalRail' or method_desc == 'Metro' or method_desc == 'NationalRail':
		return 'magenta'
	elif method_desc == 'ShortWalk' or method_desc == 'Walk':
		return 'cyan'
	elif method_desc == 'Aeroplane':
		return 'yellow'
	elif method_desc == 'Unknown' or method_desc == 'Stationary' or method_desc == 'TrainChange':
		return 'black'
	else:
		print "Unknown Method description.... " + method_desc
	return 'black'
		
	
#
#
#	Embedded wxPanel/Matplotlib
#
class CanvasPanel( wx.Panel ):

	def __init__( self, parent ):
		wx.Panel.__init__( self, parent )
		self.figure = Figure()
		self.axes = self.figure.add_subplot(111)
		
		self.canvas = FigureCanvas( self, -1, self.figure )
		self.sizer = wx.BoxSizer( wx.VERTICAL )
		self.sizer.Add( self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW )
		self.SetSizer( self.sizer )
		self.Fit()
		
	def AddLine( self, x0, y0, x1, y1, colour = 'blue', showArrows = True, annotationText = '' ):
		minimum_scale_gap =1
		
		lineWidth = 2
		lines = self.axes.plot( [x0, x1], [y0, y1], color=colour, linewidth = lineWidth )

		if len( annotationText ) > 0:
			self.axes.annotate( annotationText, xy=(x0, y0), xytext=( x0,y0), arrowprops=dict( facecolor='black', shrink=0.75 ) )
		
		if showArrows == True:
			if not ( x0 == x1 and y0 == y1 ):
				dx = 0.5 * ( x1 - x0 )
				dy = 0.5 * ( y1 - y0 )
				
				line_len = sqrt(  dx*dx + dy*dy  );

				width = line_len / 8;
				length = line_len / 5 
				arrow = self.axes.arrow( x0, y0, dx, dy, color=colour, head_width=width, head_length=length )
			
		return lines[0]
		
	def SetTitle( self, title ):
		self.axes.set_title(title)
		self.RefreshView()
		
	def SetAxisTitle( self, xTitle, yTitle ):
		for ax in self.figure.axes:
			ax.set_xlabel( xTitle )
			ax.set_ylabel( yTitle )
		self.figure.tight_layout()
		self.RefreshView()
		
	def ClearLines( self ):
		for ax in self.figure.axes:
			ax.lines = []
			ax.cla()
		self.RefreshView()
			
	def RefreshView( self ):
		self.figure.canvas.draw()
	
	
class TestPlot( wx.Frame ):

	def __init__( self, title ):
		wx.Frame.__init__( self, None, title=title, size=(512,512) )
		
		panel = wx.Panel( self, -1 )
		box = wx.BoxSizer( wx.VERTICAL )
		self.plot = CanvasPanel( panel )
		box.Add( self.plot,10, wx.EXPAND )
		panel.SetSizer( box )
		
		self.Center()
		
		self.plot.AddLine( 0, 0, 1, 1, 'red', True )
		self.plot.AddLine( 0, 0, 1, 0.5, 'blue', True )
		self.plot.AddLine( 0, 0, 0.25, 0.5, 'green', True )
		self.plot.AddLine( 1, 1, 2, 5, 'magenta', True )
		self.plot.AddLine( 2, 5, 6, 3, 'cyan', True )
		self.plot.AddLine( 6, 3, 9, 9, 'yellow', True )
#
#	Application window
#	
class MyFrame( wx.Frame ):

	def __init__( self, title ):
		wx.Frame.__init__( self, None, title=title, size=(512,512) )
		
		# get list of devices in the database
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		global devices;
		devices = []
		for row in c.execute( "SELECT DISTINCT device_id FROM travel_events ORDER BY device_id ASC" ):
			devices.append( row[0] )

		panel = wx.Panel( self, -1 )
		
		combobox = wx.BoxSizer( wx.HORIZONTAL )
		btnbox = wx.BoxSizer( wx.HORIZONTAL )
		datebox = wx.BoxSizer( wx.HORIZONTAL )
		box = wx.BoxSizer( wx.VERTICAL )
		
		combobox.Add( wx.StaticText( panel, -1, label="Device" ) )
		
		self.deviceSelctor = wx.ComboBox( panel, -1, choices=devices, name='currentDevice', value=devices[0], style=wx.CB_READONLY )
		combobox.Add( self.deviceSelctor )
		
		combobox.Add( wx.StaticText( panel, -1, label="Method" ) )
		self.methodSelctor =  wx.ComboBox( panel, -1, choices=[], name='methods', style=wx.CB_READONLY )
		combobox.Add( self.methodSelctor )
		
		
		
		combobox.Add( wx.StaticText( panel, -1, label="Legend Pos" ) )
		self.legendPos = [ 'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'  ]
		self.legendPosition =  wx.ComboBox( panel, -1, choices=self.legendPos, value=self.legendPos[0],  name='Legend', style=wx.CB_READONLY )
		combobox.Add( self.legendPosition )
		
		self.update_btn= wx.Button( panel, -1, 'View Plots')
		btnbox.Add( self.update_btn, 0, wx.EXPAND )
		
		self.clear_btn= wx.Button( panel, -1, 'Clear Plots')
		btnbox.Add(self.clear_btn, 0, wx.EXPAND )
		
		self.kml_btn = wx.Button( panel, -1, 'Export as KML')
		btnbox.Add(self.kml_btn, 0, wx.EXPAND )
		
		self.arrowCheckBox = wx.CheckBox( panel, -1, label='Show Arrows', style = wx.ALIGN_RIGHT )
		btnbox.Add( self.arrowCheckBox )
		
		self.timeCheckBox = wx.CheckBox( panel, -1, label='Show Times', style = wx.ALIGN_RIGHT )
		btnbox.Add( self.timeCheckBox )
		
		
		self.fromDate = wx.adv.DatePickerCtrl( panel, -1, style=wx.adv.DP_SPIN | wx.adv.DP_SHOWCENTURY )
		self.fromTime = wx.adv.TimePickerCtrl( panel, -1 )
		self.toDate = wx.adv.DatePickerCtrl( panel, -1, style=wx.adv.DP_SPIN | wx.adv.DP_SHOWCENTURY )
		self.toTime = wx.adv.TimePickerCtrl( panel, -1 )
		
		
		datebox.Add( wx.StaticText( panel, -1, label="From" ) )
		datebox.Add( self.fromDate, 0, wx.EXPAND )
		datebox.Add( self.fromTime, 0, wx.EXPAND )
		datebox.Add( wx.StaticText( panel, -1, label="To" ) )
		datebox.Add( self.toDate, 0, wx.EXPAND )
		datebox.Add( self.toTime, 0, wx.EXPAND )
		
		
		box.Add( combobox, 0, wx.EXPAND )
		box.Add( btnbox, 0, wx.EXPAND )
		box.Add( datebox, 0, wx.EXPAND )
		
		self.infoBox = wx.StaticText( panel, -1, label = '' ) 
		box.Add( self.infoBox, 0, wx.EXPAND )
		
		self.plot = CanvasPanel( panel )
		box.Add( self.plot,10, wx.LEFT | wx.TOP | wx.GROW )
		panel.SetSizer( box )
		
		self.Center()

		self.Bind( wx.EVT_COMBOBOX, self.OnLegendPositionChanged, self.legendPosition )
		self.Bind( wx.EVT_COMBOBOX, self.OnDeviceChanged, self.deviceSelctor )
		self.Bind( wx.EVT_COMBOBOX, self.OnMethodChanged, self.methodSelctor )
		self.Bind( wx.EVT_BUTTON, self.OnShowPlot, self.update_btn )
		self.Bind( wx.EVT_BUTTON, self.OnClearPlot, self.clear_btn )
		self.Bind( wx.EVT_BUTTON, self.OnKMLExport, self.kml_btn )
		#self.Fit()
		
	def OnShowPlot( self, event ):
		self.DrawNewLines()
		
	def OnClearPlot( self, event ):
		self.plot.ClearLines()
		
	def GetSelectCommand( self ):
	
		device = self.deviceSelctor.GetStringSelection()
		fromDT = wx.DateTime( self.fromDate.GetValue().GetDay(), self.fromDate.GetValue().GetMonth(), self.fromDate.GetValue().GetYear(), self.fromTime.GetValue().GetHour(), self.fromTime.GetValue().GetMinute() , self.fromTime.GetValue().GetSecond() )
		toDT = wx.DateTime( self.toDate.GetValue().GetDay(), self.toDate.GetValue().GetMonth(), self.toDate.GetValue().GetYear(), self.toTime.GetValue().GetHour(), self.toTime.GetValue().GetMinute() , self.toTime.GetValue().GetSecond() )
			
		sqlCommand = 'SELECT from_lat, from_long, to_lat, to_long, method_desc, ts, id FROM travel_events WHERE device_id=\'' + device + '\' AND ts BETWEEN \'' + fromDT.FormatISOCombined() + '\' AND \'' + toDT.FormatISOCombined() + '\''
			
		method = self.methodSelctor.GetValue()
		if method != 'ALL':
			sqlCommand += ' AND method_desc=\'' + method + '\''
			
		return sqlCommand

	def DrawNewLines( self ):
		self.plot.ClearLines()
		if None != self.deviceSelctor:
			device = self.deviceSelctor.GetStringSelection()
			if len( device ) == 0:
				return
			
			self.plot.SetTitle( device )
			self.plot.SetAxisTitle( "Longitude",  "Latitude" )
		
			

			legendMethods = []
			
			self.plot.title = device
			conn = sqlite3.connect(db_file)
			c = conn.cursor()
			
			sqlCommand = self.GetSelectCommand()
			print 'Select Command: ' + sqlCommand
			
			for row in c.execute( sqlCommand ):
				x_values = [ row[0], row[2] ]
				y_values = [ row[1], row[3] ]
				colour= lineColour( row[4] )
			
				time_str = ''
				if self.timeCheckBox.GetValue() == True:
					dt = dateutil.parser.parse( row[5] )
					time_str = dt.time().strftime( "%H:%M:%S" )
					
				newLine = self.plot.AddLine( row[1]*100, row[0]*100, row[3]*100, row[2]*100, colour=colour, showArrows = self.arrowCheckBox.GetValue(), annotationText=time_str  )
				
				if row[4] not in legendMethods:
					newLine.set_label( row[4] )
					legendMethods.append( row[4] )
					
			if None != self.plot.axes.legend():
				self.plot.axes.legend().draggable( state=True )
				self.plot.axes.legend()
			
		self.plot.axes.legend( loc = self.legendPosition.GetStringSelection() )
		self.plot.RefreshView()
		
	def OnDeviceChanged( self, event ):
		device = self.deviceSelctor.GetStringSelection()
		sqlCommand = 'SELECT DISTINCT method_desc FROM travel_events WHERE device_id=\'' + device + '\''
		
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		methods = [ 'ALL' ]
		for row in c.execute( sqlCommand ):
			methods.append( row[0] ) 
			
		self.methodSelctor.SetItems(methods)
		self.methodSelctor.SetValue( methods[0] )
		
		sqlCommand ='SELECT min(ts) AS \'min\', max(ts) AS \'max\' FROM travel_events WHERE device_id=\'' + device + '\''
		c.execute( sqlCommand )
		row = c.fetchone()
		
		minTime = dateutil.parser.parse( row[0] )
		maxTime = dateutil.parser.parse( row[1] )
		
		
		self.fromDate.SetValue( minTime )
		self.fromTime.SetValue( minTime )
		
		self.toDate.SetValue( maxTime )
		self.toTime.SetValue( maxTime )
		
		sqlCommand = 'SELECT COUNT(id) FROM travel_events WHERE device_id=\'' + device + '\''
		c.execute( sqlCommand )
		row = c.fetchone()
		
		event_count = row[0]
		self.infoBox.SetLabel( 'Number of Events: ' + str( event_count ) )
		
	def OnMethodChanged( self, event ):
		print 'Method changed...'
		return
		
	def OnLegendPositionChanged( self, event ):
		self.plot.axes.legend( loc = self.legendPosition.GetStringSelection() )
		self.plot.RefreshView()
		
		
	def __WriteStyle( self, name, colour, width, xmlfile ):
		xmlfile.write( '<Style id="' + name + '">\n' )
		xmlfile.write( '<LineStyle>\n' )
		xmlfile.write( '<color>' + colour + '</color>\n' )
		xmlfile.write( '<colorMode>normal</colorMode>\n')
		xmlfile.write( '<width>' + str( width ) + '</width>\n' )
		xmlfile.write( '</LineStyle>\n' )
		xmlfile.write( '</Style>\n' )
	
	def OnKMLExport( self, event  ):
		print 'Exporting to KML'
		
		device = self.deviceSelctor.GetStringSelection()
		xmlfile = open(  device + "_journey.kml", 'w' )
		if xmlfile.closed:
			raise RunTimeError( 'Writing KML file failed to open file.' )
		
		xmlfile.write( '<?xml version="1.0" encoding="UTF-8"?>\n' )
		xmlfile.write( '<kml xmlns="http://www.opengis.net/kml/2.2">\n' )
		xmlfile.write( '<Document>\n' )
		xmlfile.write( '<name>' + device + ' paths</name>\n' )
		xmlfile.write( '<description> travel events for ' + device + '</description>\n' )
		
		self.__WriteStyle( 'UnknownPath',     'FF000000', 4, xmlfile )
		self.__WriteStyle( 'CarPath',         'FF0000FF', 4, xmlfile )
		self.__WriteStyle( 'BikePath',        'FF00FF00', 4, xmlfile )
		self.__WriteStyle( 'BusPath',         'FFFF0000', 4, xmlfile )
		self.__WriteStyle( 'TrainPath',       'FFFF00FF', 4, xmlfile )
		self.__WriteStyle( 'WalkPath',        'FFFFFF00', 4, xmlfile )
		self.__WriteStyle( 'AirplanePath',    'FF00FFFF', 4, xmlfile )
		self.__WriteStyle( 'NoTransportPath', 'FFFFFFFF', 4, xmlfile )

		
		sqlCommand = self.GetSelectCommand()
		
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		for row in c.execute( sqlCommand ):
			
			method_desc = row[4]
			
			if method_desc == 'Car' or method_desc == 'CarPetrolSmall':
				stylename = 'CarPath'
			elif method_desc == 'Bicycle': 
				stylename = 'BikePath'
			elif method_desc == 'Bus':
				stylename = 'BusPath'
			elif method_desc == 'InternationalRail' or method_desc == 'Metro' or method_desc == 'NationalRail':
				stylename = 'TrainPath'
			elif method_desc == 'ShortWalk' or method_desc == 'Walk':
				stylename = 'WalkPath'
			elif method_desc == 'Aeroplane':
				stylename = 'AirplanePath'
			elif method_desc == 'Stationary' or method_desc == 'TrainChange':
				stylename = 'NoTransportPath'
			else:
				stylename = 'UnknownPath'
			
			xmlfile.write( '<Placemark>\n' )
			xmlfile.write( '<name>' + str( row[6] ) +  '_' + method_desc + '</name>\n' )
			xmlfile.write( '<styleUrl>#' +  stylename + '</styleUrl>\n' )
			xmlfile.write( '<LineString>\n' )
			xmlfile.write( '<gx:altitudeOffset>clampToGround</gx:altitudeOffset>\n' )
			xmlfile.write( '<tessellate>1</tessellate>\n' )
			
			xmlfile.write( '<coordinates>\n' )
			
			xmlfile.write( str( row[1] ) + ',' + str( row[0] ) + ',0\n' )
			xmlfile.write( str( row[3] ) + ',' + str( row[2] ) + ',0\n' )
			
			xmlfile.write( '</coordinates>\n' )
			xmlfile.write( '</LineString>\n' )
			xmlfile.write( '</Placemark>\n' )
		
		
		
		xmlfile.write( '</Document>\n' )
		xmlfile.write( '</kml>\n' )
		xmlfile.close()
		
def main():

	global db_file
	db_file = sys.argv[1]
	
	app = wx.App(False)
	frame = MyFrame( "Window1" )
	#frame = TestPlot( "Test Plot" )
	frame.Show()
	
	app.MainLoop()
	

if __name__=="__main__":
	main()