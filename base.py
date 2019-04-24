from tkinter import Tk,Button,Label,Frame,Canvas,Entry,Text,StringVar, ttk, filedialog, messagebox
import pandas as pd
from pandas import datetime, read_csv
import numpy as np
import matplotlib as mp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import seaborn as sb
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from PIL import ImageTk, Image

root = Tk
class TimeSeriesAnalysis(Tk):
    """
    Class to manage frames and methods
    """
    def __init__(self, *main):
        Tk.__init__(self, *main)
        container = Frame(self)
        container.pack(side="top", expand=True)

        container.grid_rowconfigure(0, weight=1) ### allows for frames to expand
        container.grid_columnconfigure(0, weight=1)

        self.fileAddress = ""                   ## creates the variable which will be used fo the main functions to plot/forecast


        self.frames = {}                        #### creates dictionary to store alll frames which willl be used
        pages = (MainMenu, Op1, Op2, Op3, Op4, FileSelection)           ### list with all frames
        for i in (pages):           ##for loop to allow all pages to inherit methods from main class

            frame = i(container, self)

            self.frames[i] = frame #### allows frames to inherit characteristics of the main class and hence use its methods

            frame.grid(row=0, column=0, sticky="nsew")              #
            frame.grid_rowconfigure(0,minsize=8,weight=1)
            frame.grid_columnconfigure(0,minsize=8,weight=1)
            frame.grid_propagate(False)

    def show_frame(self, y):
        frame = self.frames[y]
        frame.tkraise()

    def ignore(event):
        pass

    ###def savefig(SaveFileAddress):
        #self.SaveFileAddress =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))




class MainMenu(Frame):
    """
    Frame which operated as main menu which allows user to pick options and change file selection
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Time Series Analysis")
        label.pack()
        im = Image.open("C:/Users/Fernando/Documents/NEA/logo.jpg")        ## imports logo
        canvas = Canvas(self,width=50,height=50)
        canvas.pack()
        canvas.image = ImageTk.PhotoImage(im)                                   ## uses tkinte library in order to display image on canvas
        canvas.create_image(25,25,image=canvas.image,anchor="center")              ## creates a canvas for which the image wiill be displayed on

        self.option1button = Button(self,text="Plot time series",command=lambda:                ## Button to direct user to frame OP1
                                                                                    controller.show_frame(Op1))
        self.option1button.pack()

        self.option2button =Button(self,text="Plot time series using rolling mean",command=lambda:  ## Button t direct user to frame OP2
                                                                                                    controller.show_frame(Op2))
        self.option2button.pack()


        self.option3button = Button(self,text="Plot time series using first order differencing",command=lambda:      ## Button t direct user to frame OP3
                                                                                                                controller.show_frame(Op3))
        self.option3button.pack()

        self.option4button = Button(self,text="Analyse time series using arima model",command=lambda:            ## Button t direct user to frame OP4
                                                                                                    controller.show_frame(Op4))
        self.option4button.pack()

        self.ChangeFile = Button(self,text="Select/Change input file",command=lambda:            ## Button t direct user to frame FileSelection
                                                                                controller.show_frame(FileSelection))
        self.ChangeFile.pack()

        self.exitbutton = Button(self,text="exit",command=lambda:
                                                                    exit())
        self.exitbutton.pack()

class FileSelection(Frame):
    """
    Frame which allows user to pick and change file selected
    """
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="File Entry")
        label.pack(pady=10,padx=10)

        TempFileA = StringVar()

        def OpenBrowser(event):
            self.EnterButton.tk_focusNext().focus()                 ## changes focus of tkinter in order to prevent from going into a recursive loop with no end casae
            TempFileA.set(filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("CSV Files","*.csv"),("all files","*.*"))))           ####Opens File browser at computer home directory in order to allow user to select file
            return("break")                 ##Returns break in order to ensure that focus is changed


        def GetVarChangeF():
            controller.fileAddress = TempFileA.get()                        ##Gets the value stored in the entry widget which is labeled # TempFileA
            if len(controller.fileAddress)>1 and controller.fileAddress.endswith("csv"):    ##### Allows users to move on when they have entered a valid file address for a file with a .csv extension
                    controller.show_frame(MainMenu)
            else:
                controller.fileAddress = ""
                messagebox.showinfo("Time Series Analysis", "Please enter a valid file address")



        self.FileEntry = Entry(self,textvariable=TempFileA) ## Create a entry which is used as a storage for the fileAddress so it can be passed to controller later on and used to plot/forecast
        self.FileEntry.pack(anchor="center")

        self.FileEntry.bind("<FocusIn>",OpenBrowser)            ### Binds when focus is put onnto the fille entry widget to OpenBrowser function
        self.FileEntry.bind("<FocusOut>",controller.ignore())  ### Ignores focus out event

        self.EnterButton = Button(self,text="Enter",command = lambda:
                                                                    GetVarChangeF())            ## runs GetVarChangeF functionn
        self.EnterButton.pack(anchor="center")



class Op1(Frame):
    """
    Frame which allows user to plot the standard graph
    """

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Plotting a time series")
        label.pack(anchor = "n", padx=10,pady=10)
        self.GraphDrawn = False
        def plot_graph(fileAddress):
            lf = ttk.Labelframe(self, text='Plot Area')         ### Adds plot area label
            lf.pack()
            headers = ['date','values']                 ### Created a list of the name of the headers which will serve as the axis labels
            dt=pd.read_csv(fileAddress,header = 0, names=headers,skiprows=1)
            dt.date = pd.to_datetime(dt.date)           ### Turns the date header into actual datetime data type values
            dt.set_index('date',inplace=True)
            f = Figure(figsize=(5,5),dpi = 100)        ### defines a figure in which to embed the graph
            ax1 = f.add_subplot(111)                   ### adds a subplot
            dt.plot(legend = True,ax=ax1)              ### plots graph

            PlotCanvas = FigureCanvasTkAgg(f, self)
            toolbar = NavigationToolbar2Tk(PlotCanvas,self)
            PlotCanvas.get_tk_widget().pack(anchor="n",expand = True)
            PlotCanvas.draw()
            PlotCanvas._tkcanvas.pack(anchor="n")
            if self.GraphDrawn == False:
                self.GraphDrawn = True                ###Only allows user to plot graph if it has not yet been plotted for this frame
            elif self.GraphDrawn == True:
                PlotCanvas.get_tk_widget().destroy()
                toolbar.destroy()

        self.previewButton=Button(self,text=("Preview"),command = lambda:
                                                                        plot_graph(controller.fileAddress))
        self.previewButton.pack(anchor = "s" ,pady=1)

        self.ChangeFile = Button(self,text="Select/Change input file",command=lambda:
                                    controller.show_frame(FileSelection))
        self.ChangeFile.pack(anchor = "s" ,pady=1)

        self.HomeButton = Button(self, text="Back to menu",command=lambda:
                                                                        controller.show_frame(MainMenu))
        self.HomeButton.pack(anchor = "s" ,pady=1)

        self.exitbutton = Button(self,text="exit",command=lambda:
                                                                exit())
        self.exitbutton.pack(anchor = "s" ,pady=1)





class Op2(Frame):
    """
    Frame which allows user to plot the graph using rolling mean
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Plotting time series with rolling mean")
        label.pack(anchor = "n", padx=10,pady=10)

        self.GraphDrawn = False

        def plot_graph(fileAddress):
            lf = ttk.Labelframe(self, text='Plot Area')         ### Adds plot area label
            lf.pack()
            headers = ['date','values']                 ### Created a list of the name of the headers which will serve as the axis labels
            dt=pd.read_csv(fileAddress,header = 0, names=headers,skiprows=1)
            dt.date = pd.to_datetime(dt.date)           ### Turns the date header into actual datetime data type values
            dt.set_index('date',inplace=True)
            f = Figure(figsize=(5,5),dpi = 100)        ### defines a figure in which to embed the graph
            ax1 = f.add_subplot(111)                   ### adds a subplot
            dt.rolling(12).mean().plot(legend = True,ax=ax1)        ## Plot the data using rolling mean method
            canvas = FigureCanvasTkAgg(f, self)                 ## Defines a canvas which can have a matploblib plot on it
            canvas.draw()                                       ##Makes the canvas
            canvas.get_tk_widget().pack(anchor="center",expand = True)      ### Adds the canvas to the frame
            toolbar = NavigationToolbar2Tk(canvas,self)                 ## Defines toolbar to be used
            canvas._tkcanvas.pack(anchor="center",expand = True)
            self.GraphDrawn == True

            if self.GraphDrawn == False:
                self.GraphDrawn = True                ###Only allows user to plot graph if it has not yet been plotted for this frame
            elif self.GraphDrawn == True:
                canvas.get_tk_widget().destroy()
                toolbar.destroy()

        self.previewButton=Button(self,text=("Preview"),command = lambda:
                                                                        plot_graph(controller.fileAddress))
        self.previewButton.pack(anchor = "s" ,pady=1)

        self.ChangeFile = Button(self,text="Select/Change input file",command=lambda:
                                    controller.show_frame(FileSelection))
        self.ChangeFile.pack(anchor = "s" ,pady=1)

        self.HomeButton = Button(self, text="Back to menu",command=lambda:
                                                                        controller.show_frame(MainMenu))
        self.HomeButton.pack(anchor = "s" ,pady=1)

        self.exitbutton = Button(self,text="exit",command=lambda:
                                                                exit())
        self.exitbutton.pack(anchor = "s" ,pady=1)

class Op3(Frame):
    """
    Frame which allows user to plot the graph of their data using first orderr differencinng
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Plot time series using first order differencing")
        label.pack(anchor = "n", padx=10,pady=10)

        self.GraphDrawn = False

        def plot_graph(fileAddress):

            lf = ttk.Labelframe(self, text='Plot Area')
            lf.pack()
            headers = ['date','values']
            dt=pd.read_csv(fileAddress,header = 0, names=headers,skiprows=1)
            dt.date = pd.to_datetime(dt.date)
            dt.set_index('date',inplace=True)

            f = Figure(figsize=(5,4),dpi = 100)
            ax1 = f.add_subplot(111)
            dt.diff().plot(legend = True,ax=ax1)
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().pack(anchor="center",expand = True)
            toolbar = NavigationToolbar2Tk(canvas,self)
            canvas._tkcanvas.pack(anchor="center",expand = True)
            self.GraphDrawn == True

            if self.GraphDrawn == False:
                self.GraphDrawn = True                ###Only allows user to plot graph if it has not yet been plotted for this frame
            elif self.GraphDrawn == True:
                canvas.get_tk_widget().destroy()
                toolbar.destroy()



        self.previewButton=Button(self,text=("Preview"),command = lambda:
                                                                        plot_graph(controller.fileAddress))
        self.previewButton.pack(anchor = "s" ,pady=1)

        self.ChangeFile = Button(self,text="Select/Change input file",command=lambda:
                                    controller.show_frame(FileSelection))
        self.ChangeFile.pack(anchor = "s" ,pady=1)

        self.HomeButton = Button(self, text="Back to menu",command=lambda:
                                                                        controller.show_frame(MainMenu))
        self.HomeButton.pack(anchor = "s" ,pady=1)

        self.exitbutton = Button(self,text="exit",command=lambda:
                                                                exit())
        self.exitbutton.pack(anchor = "s" ,pady=1)


class Op4(Frame):
    """
    Fame which handles TimeSeries forecasting which shows an image of the forecasted data against the given data and saves it onto a csv called predictions
    """

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="Analyse time series using arima model")
        label.pack(anchor = "n", padx=10,pady=10)

        self.GraphDrawn = False

        """
        fuction which plots graph and makes a figure then packing it
        """
        def plot_graph(dt):
            lf = ttk.Labelframe(self, text='Plot Area')
            lf.pack()
            headers = ['date','values']

            f = Figure(figsize=(5,4),dpi = 100)
            ax1 = f.add_subplot(111)
            dt.plot(legend = True,ax=ax1)
            canvas = FigureCanvasTkAgg(f, self)
            self.GraphDrawn = True
            canvas.draw()
            canvas.get_tk_widget().pack(anchor="center",expand = True)
            toolbar = NavigationToolbar2Tk(canvas,self)
            canvas._tkcanvas.pack(anchor="center")
            self.GraphDrawn = True

        def parser(x):
            try:
                return datetime.strptime(x, '%Y-%m-%d') ## Attempts to read the data given by using the format yyyy/mm/dd
            except:
                return datetime.strptime(x,'%Y-%m')     ## Attempts to read the data given by using the format yyyy/mm


        def forecast(fileAddress):
            if self.GraphDrawn == False:
                messagebox.showinfo("Time Series Analysis", "This will take a minute please wait. A file will be output with the prediction on the same location as the program.")
                series = pd.read_csv(fileAddress, header=0, parse_dates=[0],
                    index_col=0, squeeze=True, date_parser=parser,skiprows = 1)
                X = series.values
                size = int(len(X) * 0.6)            ## sets the amount of data that is going to be tested (max would be 0.1 min would be 0.9)
                train, test = X[0:size], X[size:len(X)]     ## defines the test data and the data which it will be compared to
                history = [x for x in train]
                predictions = list()                    ### defines a list for which the forecast will be input to
                for t in range(len(test)):
                    model = ARIMA(history, order=(5,1,0))           ## Runs arima algorithm in order make the model
                    model_fit = model.fit(disp=0)               ## Fits the model
                    output = model_fit.forecast()               ## Forecasts based on previous data within the window defined by arima
                    yhat = output[0]
                    predictions.append(yhat)
                    obs = test[t]
                    history.append(obs)
                """
                Part of the function which makes a new data fram with the predictions and plots said data frame
                """
                error = mean_squared_error(test, predictions)
                PredicVals = []
                for i in range (int(len(predictions))):
                    PredicVals.append(predictions[i].item())            ##Due to the output of the forecast function being a numpy array in oder for me to plot the graph i have to add them to a list and get the modulous of them
                headers = ['date','values']
                RowsNeedSkip =1+int(len(train))                                 ##This is to remove the data which is unused for testing
                dt = read_csv(fileAddress,header = 0, names=headers,skiprows=RowsNeedSkip)      #### Imports csv file again but having removed unneeded data
                dt.insert(2, "Predictions", PredicVals, True)               ## inserts data which is needed
                dt.date = pd.to_datetime(dt.date)           ### Turns the date header into actual datetime data type values
                dt.set_index('date',inplace=True)
                dt.to_csv('prediction.csv')                 ### This will save a csv file with the actual and predicted values for the dates
                plot_graph(dt)

            elif self.GraphDrawn == True:
                pass




        self.opButton = Button(self,text="Time series forecasting using a csv file",command = lambda: forecast(controller.fileAddress))
        self.opButton.pack(anchor="n")

        self.HomeButton = Button(self, text="Back to menu",command=lambda:
                                                                            controller.show_frame(MainMenu))
        self.HomeButton.pack(anchor="s")

        self.ChangeFile = Button(self,text="Select/Change input file",command=lambda:
                                                                            controller.Unpack_ShowFrame(FileSelection))
        self.ChangeFile.pack(anchor="s")

        self.exitbutton = Button(self,text="exit",command=lambda: exit())
        self.exitbutton.pack(anchor="s")

app = TimeSeriesAnalysis()
app.mainloop()
