#Polynomial and exponential classes
from tkinter import *
from tkinter import ttk
from math import e
     
class Application():
    def __init__(self, parent):
        self.parent = parent
        self.ScreenWidth = self.parent.winfo_screenwidth()  #Used to fit the app to the user's screen
        self.ScreenHeight = self.parent.winfo_screenheight()
        #Preset coordinates for x and y graph axes
        self.XMin = -10
        self.XMax = 10
        self.YMin = -10
        self.YMax = 10
        self.Graph = None
        self.Answer = ''
        self.TrailList = []
        self.CurrentZoomScale = 1    #Used for scaling methods
        self.Equation = None    #Changes class between polynomial and exponential

        self.CreateGUI()

    def CreateGUI(self):
        self.MainFrame = Frame(self.parent, width = self.ScreenWidth, height = self.ScreenHeight)
        self.MainFrame.grid()
        
        #Create frame for user inputs
        self.EquationFrame = Frame(self.MainFrame, width = 150, height = self.ScreenHeight)
        self.EquationFrame.grid(row = 0, column = 0)

        #Frame for the instructions textbox
        self.InstructionsFrame = Frame(self.EquationFrame, width = 150, height = 200)
        self.InstructionsFrame.grid(row = 0)

        #Frame for the user's entries
        self.EntryFrame = Frame(self.EquationFrame, width = 150, height = 75)
        self.EntryFrame.grid(row = 1)

        #Create widgets for input frame
        self.CreateDrawGraphButton(self.EquationFrame)
        self.ChoiceOfGraphRadioButtons(self.EquationFrame)
        self.CreateInstructionsTextBox(self.EquationFrame)

        #Frame for widget layout for the bottom left corner of the GUI
        self.BottomLeftFrame = Frame(self.EquationFrame, width = 150, height = 100)
        self.BottomLeftFrame.grid(row = 6, column = 0)
        self.CreateZoomingButtons(self.BottomLeftFrame)
        self.CreateExamplesMenu(self.BottomLeftFrame)

        #Create frame for the graph canvas
        self.GraphFrame = Frame(self.MainFrame, width = 550, height = 550)
        self.GraphFrame.grid(row = 0, column = 1)
        
        self.Canvas = Canvas(self.GraphFrame, width = 550, height = 550, bg = 'white')
        self.Canvas.grid()

        #The use of '+20' , '+15', etc is to centre the canvas in the middle of the frame.
        #This allows the axes' coordinates to fit on the screen.
        #set up x axis
        self.Canvas.create_line(self.CanvasX(self.XMin)+20, self.CanvasY(0)+20, self.CanvasX(self.XMax)+20, self.CanvasY(0)+20, width = 2)
        for XLabel in range(self.XMin, self.XMax + 1, 1):
            if XLabel != 0:
                self.Canvas.create_line(self.CanvasX(XLabel)+20, self.CanvasY(0)+25, self.CanvasX(XLabel)+20, self.CanvasY(0)+15, width = 2)
                self.Canvas.create_text(self.CanvasX(XLabel)+20, self.CanvasY(0)+5, text = str("%.0f" % XLabel))

        #set up y axis
        self.Canvas.create_line(self.CanvasX(0)+20, self.CanvasY(self.YMin)+20, self.CanvasX(0)+20, self.CanvasY(self.YMax)+20, width = 2)
        for YLabel in range(self.YMin, self.YMax + 1, 1):
            if YLabel != 0:
                self.Canvas.create_line(self.CanvasX(0)+15, self.CanvasY(YLabel)+20, self.CanvasX(0)+25, self.CanvasY(YLabel)+20, width = 2)
                self.Canvas.create_text(self.CanvasX(0), self.CanvasY(YLabel)+20, text = str("%.0f" % YLabel))

        #Bind left mouse button to move around canvas
        self.Canvas.bind('<ButtonPress-1>', self.StartScrolling)
        self.Canvas.bind('<B1-Motion>', self.MoveAround)

        #Create frame for outputs
        self.AnswerFrame = Frame(self.MainFrame, width = 150, height = self.ScreenHeight)
        self.AnswerFrame.grid(row = 0, column = 2)

        #Create widgets for output frame
        self.CreateOutputTextBox(self.AnswerFrame)
        self.CreateUserAnswerInput(self.AnswerFrame)
        self.CreateSolveButtons(self.AnswerFrame)
        self.CreateClearGraphButton(self.AnswerFrame)

        self.PlotLine() #Plots a y = x line

#Create method to recreate the entry frame after it is destroyed
    def RecreateEntryFrame(self):
        self.EntryFrame = Frame(self.EquationFrame, width = 150, height = 200)
        self.EntryFrame.grid(row = 1)
    
#Methods that create the ordinates
    def CanvasX(self, x):
        a = 500/(self.XMax - self.XMin)
        b = -a*self.XMin
        return a*x+b

    def CanvasY(self, y):
        c = 500/(self.YMin - self.YMax)
        d = -c*self.YMax
        return c*y+d

    def ActualX(self, x):
        a = 500/(self.XMax - self.XMin)
        b = -a*self.XMin
        return (x-b)/a

#If graph is a polynomial
    def PlotPolynomial(self):
        self.Canvas.delete(self.Graph)
        for loop in range(0, len(self.TrailList)):
            self.Canvas.delete(self.TrailList[loop])
        self.Equation.GetPolyInputs()
        if self.Equation.GotAllInputs == True:
            Scaled = []
            for x1 in range(0, 500):
                x = self.ActualX(x1)
                y = self.Equation.XCubedCoefficient*x**3 + self.Equation.XSquaredCoefficient*x**2 + self.Equation.XCoefficient*x + self.Equation.YIntercept
                y1 = self.CanvasY(y)
                Scaled.append((x1 + 20, y1 + 20))
            self.Graph = self.Canvas.create_line(Scaled)

#If graph is exponential
    def PlotExponential(self):
        self.Canvas.delete(self.Graph)
        for loop in range(0, len(self.TrailList)):
            self.Canvas.delete(self.TrailList[loop])
        self.Equation.GetExpoInputs()
        if self.Equation.GotAllInputs == True:
            Scaled = []
            for x1 in range(0, 500):
                x = self.ActualX(x1)
                y = self.Equation.eCoefficient ** (self.Equation.CoefficientOfExponent * x) + self.Equation.YTranslation
                y1 = self.CanvasY(y)
                Scaled.append((x1 + 20, y1 + 20))
            self.Graph = self.Canvas.create_line(Scaled)

#Plot y = x line
    def PlotLine(self):
        Scaled=[]
        for x1 in range(0, 500):
            x = self.ActualX(x1)
            y = x
            y1 = self.CanvasY(y)
            Scaled.append((x1 + 20, y1 + 20))
        self.Canvas.create_line(Scaled)

#Create method that plots the trail(s)
    def PlotTrail(self, X1, Y1, X2, Y2):  
        self.TrailList.append(self.Canvas.create_line(self.CanvasX(X1)+20, self.CanvasY(Y1)+20, self.CanvasX(X2)+20, self.CanvasY(Y2)+20, fill = 'blue', width = 1))

#Create method that decides which type of graph to draw
    def PlotGraph(self):
        self.RescaleCanvas()
        if isinstance(self.Equation, Polynomial):
            self.PlotPolynomial()
        elif isinstance(self.Equation, Exponential):
            self.PlotExponential()
        else:
            self.WorkingsBox.insert(END, 'No inputs\n')

#Create Methods that allow the user to zoom and navigate the canvas
    def CreateZoomingButtons(self, Frame):
        self.ButtonsFrame = ttk.Labelframe(Frame, text = 'Change scale of graph')
        self.ButtonsFrame.grid(row = 6, column = 0)

        self.ZoomInButton = Button(self.ButtonsFrame, text = 'Zoom In', command = self.ZoomIn)
        self.ZoomInButton.pack(side = TOP)

        self.ZoomOutButton = Button(self.ButtonsFrame, text = 'Zoom Out', command = self.ZoomOut)      
        self.ZoomOutButton.pack(side = BOTTOM)
        
    def ZoomIn(self):
        if self.CurrentZoomScale < 8:
            self.Canvas.addtag_all('all')
            self.Canvas.scale('all', 275, 275, 2, 2)
            self.CurrentZoomScale = self.CurrentZoomScale * 2

    def ZoomOut(self):
        if self.CurrentZoomScale > 0.5:
            self.Canvas.addtag_all('all')
            self.Canvas.scale('all', 275, 275, 0.5, 0.5)
            self.CurrentZoomScale = self.CurrentZoomScale * 0.5

#Methods to centre/recentre canvas after it's been scrolled
    def CentreCanvas(self):
        None
    
#Methods to allow the user to drag around the graph
    def StartScrolling(self, event):
        self.Canvas.scan_mark(event.x, event.y)
        
    def MoveAround(self, event):
        self.Canvas.scan_dragto(event.x, event.y, gain = 1)

#Method to reset canvas scale so lines are drawn correctly
    def RescaleCanvas(self):
        while self.CurrentZoomScale != 1:
            if self.CurrentZoomScale > 1:
                self.ZoomOut()
            elif self.CurrentZoomScale < 1:
                self.ZoomIn()
    
#Create methods that clear the graph and trails
#Ask the user, incase they misclicked
    def DoYouWantToDelete(self):
        Result = messagebox.askquestion('Warning', 'Are you sure? This will delete the current graph, diagram and the workings in the text box.')
        if Result == 'yes':
            self.Clear()

#Delete all contents of the graph and output textbox
    def Clear(self):
        self.Canvas.delete(self.Graph)
        for loop in range(0, len(self.TrailList)):
            self.Canvas.delete(self.TrailList[loop])
        self.WorkingsBox.delete(1.0, END)
        self.Equation.CurrentX = 0
        self.Equation.TempYValue = 0
        self.Equation.Limit = None
        self.Equation.LimitReached = False

#Create entry box for the user's answer
    def CreateUserAnswerInput(self, Frame):
        self.UserAnswerInputFrame = ttk.Labelframe(Frame, text = 'Enter your answer here (3 d.p.)')
        self.UserAnswerInputFrame.grid(row = 1, column = 0)

        self.UserAnswerInput = Entry(self.UserAnswerInputFrame, width = 30)
        self.UserAnswerInput.grid()

#Create Method to round the program's answer and check against the user's answer
    def CheckAnswers(self):
        self.UserAnswer = self.UserAnswerInput.get()
        self.Answer = '%.3f' % self.Answer  #Rounds the program's answer to 3 decimal places (3 d.p.)
        self.WorkingsBox.insert(END, 'The answer was: '+str(self.Answer)+'\n')
        self.WorkingsBox.insert(END, 'Coordinates of intersection:\n('+str(self.Answer)+', '+str(self.Answer)+')\n')
        if self.UserAnswer != '':
            if self.Answer == '%.3f' % float(self.UserAnswer):
                self.WorkingsBox.insert(END, 'Correct!\n')
            else:
                self.WorkingsBox.insert(END, 'You were incorrect\n')

#Create method to do one iteration towards the limit
    def DoOneIteration(self, event):
        self.RescaleCanvas()
        if self.Equation.X1Input.get() != '' and self.Equation.X1 != eval(self.Equation.X1Input.get()):
            self.Clear()
            self.PlotGraph()
            self.Equation.LimitReached = False
            self.Equation.X1 = eval(self.Equation.X1Input.get())
            self.Equation.CurrentX = 0
        elif self.Equation.LimitReached == True:
            None
        if self.Equation.CurrentX == 0:
            self.Equation.DoOneStep(self.Equation.X1)
        else:
            self.Equation.DoOneStep(self.Equation.TempYValue)
    
#Create method that determines the limit
    def SolveLimit(self, event):
        self.Answer = ''
        self.RescaleCanvas()
        self.WorkingsBox.delete(1.0, END)
        if isinstance(self.Equation, Polynomial):
            if self.Equation.CurrentX >= 1:
                self.Equation.CurrentX = 0
            self.Equation.TempYValue = 0
            self.Equation.X1 = eval(self.Equation.X1Input.get())
            for loop in range(0, len(self.TrailList)):
                self.Canvas.delete(self.TrailList[loop])
            self.Equation.PolynomialRoot(self.Equation.X1)
            if self.Answer != '':
                self.CheckAnswers()

        elif isinstance(self.Equation, Exponential):
            if self.Equation.CurrentX >= 1:
                self.Equation.CurrentX = 0
            self.Equation.TempYValue = 0
            self.Equation.X1 = eval(self.Equation.X1Input.get())
            for loop in range(0, len(self.TrailList)):
                self.Canvas.delete(self.TrailList[loop])
            self.Equation.ExponentialRoot(self.Equation.X1)
            if self.Answer != '':
                self.CheckAnswers()

        else:
            self.WorkingsBox.insert(END, 'Type of equation not selected\n')

#Create callback for finding the root
    def FindTheRootCallback(self, event):
        self.Equation.PolynomialRoot(self.Equation.X1, self.Canvas)

#Create buttons for inputs and outputs        
    def CreateSolveButtons(self, frame):
        self.SolvingButtonsFrame = Frame(frame)
        self.SolvingButtonsFrame.grid(row = 2, column = 0)

        #Button to do one iteration
        OneStepButton = Button(self.SolvingButtonsFrame, text = 'Next Iteration')
        OneStepButton.bind('<Button-1>', self.DoOneIteration)
        OneStepButton.pack(side = LEFT)

        #Button to solve the limit
        SolveButton = Button(self.SolvingButtonsFrame, text = 'Solve Limit')
        SolveButton.bind('<Button-1>', self.SolveLimit)
        SolveButton.pack(side = RIGHT)
    
    #Output buttons
    def CreateDrawGraphButton(self, Frame):
        DrawGraphButton = Button(Frame, text = 'Draw Graph', command = self.PlotGraph)
        DrawGraphButton.grid(row = 5, column = 0)

    def CreateClearGraphButton(self, Frame):
        ClearGraphButton = Button(Frame, text = 'Clear Graph', command = self.DoYouWantToDelete)
        ClearGraphButton.grid(row = 3, column = 0)
        
#Create events that change the equation type
    def SetAsPolynomial(self):
        if isinstance(self.Equation, Exponential):
            self.EntryFrame.destroy()   #Destroys the inputs for exponential so the polynomial inputs can be created
            self.RecreateEntryFrame()
            self.Equation = Polynomial(self.EntryFrame)
        else:
            self.Equation = Polynomial(self.EntryFrame)

    def SetAsExponential(self):
        if isinstance(self.Equation, Polynomial):
            self.EntryFrame.destroy()
            self.RecreateEntryFrame()
            self.Equation = Exponential(self.EntryFrame)
        else:
            self.Equation = Exponential(self.EntryFrame)
        
    def ChoiceOfGraphRadioButtons(self, Frame):
        #Create Label Frame
        self.COGFrame = ttk.Labelframe(Frame, text = 'Graph type') #COG = 'Choice of Graphs'
        self.COGFrame.grid(row = 3, column = 0)

        #Setup RadioButtons
        self.Var = IntVar()
        self.PolynomialGraph = ttk.Radiobutton(self.COGFrame, text = 'Polynomial', variable = self.Var, value = 1, command = self.SetAsPolynomial)
        self.PolynomialGraph.grid(row = 3, column = 0)
        self.ExponentialGraph = ttk.Radiobutton(self.COGFrame, text = 'Exponential', variable = self.Var, value = 2, command = self.SetAsExponential)
        self.ExponentialGraph.grid(row = 4, column = 0)

#Create the text box that outputs the program's workings
    def CreateOutputTextBox(self, frame):
        self.TextBoxFrame = Frame(frame)
        self.TextBoxFrame.grid(row = 0, column = 0)

        self.WorkingsBox = Text(self.TextBoxFrame, width = 35)
        self.WorkingsBox.pack(side = LEFT, fill = Y)

        self.TextBoxScrollbar = Scrollbar(self.TextBoxFrame)
        self.TextBoxScrollbar.pack(side = RIGHT, fill = Y)

        #Attach TextBox to scrollbar
        self.WorkingsBox.config(yscrollcommand = self.TextBoxScrollbar.set)
        self.TextBoxScrollbar.config(command = self.WorkingsBox.yview)

#Create info boxes for instructions on how to use the program
    def CreateInstructionsTextBox(self, frame):
        self.InstructionsTextBoxFrame = Frame(frame)
        self.InstructionsTextBoxFrame.grid(row = 0, column = 0)
        
        self.InstructionsTextBox = Text(self.InstructionsTextBoxFrame, width = 50, height = 20, wrap = WORD)
        self.InstructionsTextBox.pack(side = LEFT, fill = Y)

        self.InstructionsTextBoxScrollbar = Scrollbar(self.InstructionsTextBoxFrame)
        self.InstructionsTextBoxScrollbar.pack(side = RIGHT, fill = Y)

        #Attach TextBox to scrollbar
        self.InstructionsTextBox.config(yscrollcommand = self.InstructionsTextBoxScrollbar.set)
        self.InstructionsTextBoxScrollbar.config(command = self.InstructionsTextBox.yview)
        
        #Create Startup text
        self.InstructionsTextBox.tag_configure('center-text', justify = 'center')
        self.InstructionsTextBox.insert(END, '''Welcome to the Staircase/Cobweb Plotter!
\nTo get started first select the type of graph you are using below.
\nIf you know the limit you can enter it in the box at the bottom right.
\nWrite your answers to 3 d.p.''', 'center-text')
        self.InstructionsTextBox.config(state = DISABLED)

#Add ability to import parameters for example questions
    def CreateExamplesMenu(self, Frame):
        self.ExamplesMenuFrame = ttk.LabelFrame(Frame, text = 'Examples')
        self.ExamplesMenuFrame.grid(row = 6, column = 1)

        self.ExamplesMenu = ttk.Combobox(self.ExamplesMenuFrame)
        HowManyExamples = self.GetNoOfExamples()
        ExamplesList = []
        for ExampleNo in range(1, HowManyExamples + 1):
            ExamplesList.append('Example ' + str(ExampleNo))
        self.ExamplesMenu['values'] = (ExamplesList)
        self.ExamplesMenu.grid()
        self.ExamplesMenu.bind('<<ComboboxSelected>>', self.ImportParameters)

#Method to check how many example questions there are. Allows any number of examples to be put into the text file.
    def GetNoOfExamples(self):
        NoOfExamples = 0
        FileHandle = open('ExampleQuestions.txt', 'r')
        CurrentLine = None
        while CurrentLine != '':
            CurrentLine = FileHandle.readline()
            if CurrentLine.strip() == 'Polynomial' or CurrentLine.strip() == 'Exponential':
                NoOfExamples = NoOfExamples + 1
        FileHandle.close()  #Close file once done
        return NoOfExamples
          
#Method to get the values for the equations. The method checks if the question is Polynomial or Exponential first.
    def ImportParameters(self, event):
        CurrentExample = self.ExamplesMenu.current()
        FileHandle = open('ExampleQuestions.txt', 'r')
        Line = FileHandle.readline()
        #Find the location of the example in the text file
        while Line.strip() != str(CurrentExample + 1)+'.' and Line != '':    #This allows the user to number their example questions e.g. "1.", "2.", "3.", etc.
            Line = FileHandle.readline()
            
        Line = FileHandle.readline()
        if Line.strip() == 'Polynomial':    #When the example is a polynomial equation, program will use polynomial parameters
            self.Var.set(1)
            self.SetAsPolynomial()
            Count = 1    #Used to tell which parameter to import
            while Line != '':
                if Count == 1:
                    Line = FileHandle.readline()
                    self.Equation.XCubedInput.insert(END, Line.strip())
                    Count = Count + 1
                elif Count == 2:
                    Line = FileHandle.readline()
                    self.Equation.XSquaredInput.insert(END,Line.strip())
                    Count = Count + 1
                elif Count == 3:
                    Line = FileHandle.readline()
                    self.Equation.XInput.insert(END, Line.strip())
                    Count = Count + 1
                elif Count == 4:
                    Line = FileHandle.readline()
                    self.Equation.YInterceptInput.insert(END, Line.strip())
                    Count = Count + 1
                elif Count == 5:
                    Line = FileHandle.readline()
                    self.Equation.X1Input.insert(END, Line.strip())
                    Count = Count + 1
                else:
                    Line = FileHandle.readline()
        elif Line.strip() == 'Exponential': #When the example is an exponential equation, program will use the exponential parameters
            self.Var.set(2)
            self.SetAsExponential()
            Count = 1    #Used to tell which parameters to import
            while Line != '':
                if Count == 1:
                    Line = FileHandle.readline()
                    self.Equation.eCoefficientInput.insert(END, Line.strip())
                    Count = Count + 1
                elif Count == 2:
                    Line = FileHandle.readline()
                    self.Equation.CoefficientOfExponentInput.insert(END, Line.strip())
                    Count = Count + 1
                elif Count == 3:
                    Line = FileHandle.readline()
                    self.Equation.YTranslationInput.insert(END, Line.strip())
                    Count = Count + 1
                elif Count == 4:
                    Line = FileHandle.readline()
                    self.Equation.X1Input.insert(END, Line.strip())
                    Count = Count + 1
                else:
                    Line = FileHandle.readline()
        FileHandle.close()  #Close file once done
      
#Create class for polynomial equations
class Polynomial(Application):
    def __init__(self, parent):
        #Setup Attributes
        self.parent = parent
        self.XCubedCoefficient = 0
        self.XSquaredCoefficient = 0
        self.XCoefficient = 0
        self.YIntercept = 0
        self.Limit = None
        self.LimitReached = False
        self.CurrentX = 0
        self.X1 = '0'
        self.TempYValue = 0

        #Startup Methods
        self.XCubedInput(self.parent)
        self.XSquaredInput(self.parent)
        self.XInput(self.parent)
        self.YInterceptInput(self.parent)
        self.X1Input(self.parent)
        self.ChangeText()

#Change the instruction text to tell the user how to use the polynomial parameters
    def ChangeText(self):
        App.InstructionsTextBox.config(state = NORMAL)
        App.InstructionsTextBox.delete(1.0, END)
        App.InstructionsTextBox.insert(END, '''You are working with Polynomial graphs.
\n\nThe polynomial equations are written as \n"ax^3 + bx^2 + cx + d", where a, b, c and d are your inputs.
\n\nThe box that says "X1" is for the first value of x in the sequence you are using.
\n\nNotes: the symbol "^" is the symbol for powers/orders, for example you would read "x^3" as "x cubed"
\n\nIf your equation does not have one of the displayed terms, put a 0 as the coefficient for that term.''', 'center-text')
        App.InstructionsTextBox.config(state = DISABLED)
        

#Create text input boxes
    def XCubedInput(self, Frame):
        self.InputFrame1 = ttk.Labelframe(Frame, text = 'ax^3')
        self.InputFrame1.grid(row = 1, column = 0)
        self.XCubedInput = Entry(self.InputFrame1, width = 15)
        self.XCubedInput.grid()

    def XSquaredInput(self, Frame):
        self.InputFrame2 = ttk.Labelframe(Frame, text = '+ bx^2')
        self.InputFrame2.grid(row = 1, column = 1)
        self.XSquaredInput = Entry(self.InputFrame2, width = 15)
        self.XSquaredInput.grid()

    def XInput(self, Frame):
        self.InputFrame3 = ttk.Labelframe(Frame, text = '+ cx')
        self.InputFrame3.grid(row = 1, column = 2)
        self.XInput = Entry(self.InputFrame3, width = 15)
        self.XInput.grid()

    def YInterceptInput(self, Frame):
        self.InputFrame4 = ttk.Labelframe(Frame, text = '+ d')
        self.InputFrame4.grid(row = 1, column = 3)
        self.YInterceptInput = Entry(self.InputFrame4, width = 15)
        self.YInterceptInput.grid()

    def X1Input(self, Frame):
        self.InputFrame5 = ttk.Labelframe(Frame, text = 'X1')
        self.InputFrame5.grid(row = 2)
        self.X1Input = Entry(self.InputFrame5, width = 15)
        self.X1Input.grid()

    def GetPolyInputs(self):
        #Check that each input box isn't empty before checking
        #Also check that the input can be identified as a number
        self.GotAllInputs = True

        #XCubedCoefficient
        self.XCubedCoefficient = self.XCubedInput.get()
        if self.XCubedCoefficient != '':
            IsANumber = True
            for loop in range(0, len(self.XCubedCoefficient)):
                if self.XCubedCoefficient[loop].isdigit() == False:
                    if self.XCubedCoefficient[loop] == '/' or self.XCubedCoefficient[loop] == '.' or self.XCubedCoefficient[loop] == '-':
                        if self.XCubedCoefficient[loop-1].isdigit() == False:
                            IsANumber = False
                        elif self.XCubedCoefficient.endswith('/', 0, len(self.XCubedCoefficient)) == True:
                            IsANumber = False
                    else:
                        IsANumber = False
            if IsANumber == False:
                App.WorkingsBox.insert(END, '(ax^3) Incorrect type of input\n')
                self.GotAllInputs = False
            else:
                self.XCubedCoefficient = eval(self.XCubedCoefficient)
        else:
            App.WorkingsBox.insert(END, 'No input for ax^3 found\n')
            self.GotAllInputs = False

        #XSquaredCoefficient
        self.XSquaredCoefficient = self.XSquaredInput.get()
        if self.XSquaredCoefficient != '':
            IsANumber = True
            for loop in range(0, len(self.XSquaredCoefficient)):
                if self.XSquaredCoefficient[loop].isdigit() == False:
                    if self.XSquaredCoefficient[loop] == '/' or self.XSquaredCoefficient[loop] == '.' or self.XSquaredCoefficient[loop] == '-':
                        if self.XSquaredCoefficient[loop-1].isdigit() == False:
                            IsANumber = False
                        elif self.XSquaredCoefficient.endswith('/', 0, len(self.XSquaredCoefficient)) == True:
                            IsANumber = False
                    else:
                        IsANumber = False
            if IsANumber == False:
                App.WorkingsBox.insert(END, '(bx^2) Incorrect type of input\n')
                self.GotAllInputs = False
            else:
                self.XSquaredCoefficient = eval(self.XSquaredCoefficient)
        else:
            App.WorkingsBox.insert(END, 'No input for bx^2 found\n')
            self.GotAllInputs = False
            
        #XCoefficient
        self.XCoefficient = self.XInput.get()
        if self.XCoefficient != '':
            IsANumber = True
            for loop in range(0, len(self.XCoefficient)):
                if self.XCoefficient[loop].isdigit() == False:
                    if self.XCoefficient[loop] == '/' or self.XCoefficient[loop] == '.' or self.XCoefficient[loop] == '-':
                        if self.XCoefficient[loop-1].isdigit() == False:
                            IsANumber = False
                        elif self.XCoefficient.endswith('/', 0, len(self.XCoefficient)) == True:
                            IsANumber = False
                    else:
                        IsANumber = False
            if IsANumber == False:
                App.WorkingsBox.insert(END, '(cx) Incorrect type of input\n')
                self.GotAllInputs = False
            else:
                self.XCoefficient = eval(self.XCoefficient)
        else:
            App.WorkingsBox.insert(END, 'No input for cx found\n')
            self.GotAllInputs = False
            
        #YIntercept
        self.YIntercept = self.YInterceptInput.get()
        if self.YIntercept != '':
            IsANumber = True
            for loop in range(0, len(self.YIntercept)):
                if self.YIntercept[loop].isdigit() == False:
                    if self.YIntercept[loop] == '/' or self.YIntercept[loop] == '.' or self.YIntercept[loop] == '-':
                        if self.YIntercept[loop-1].isdigit() == False:
                            IsANumber = False
                        elif self.YIntercept.endswith('/', 0, len(self.YIntercept)) == True:
                            IsANumber = False
                    else:
                        IsANumber = False
            if IsANumber == False:
                App.WorkingsBox.insert(END, '(d) Incorrect type of input\n')
                self.GotAllInputs = False
            else:
                self.YIntercept = eval(self.YIntercept)
        else:
            App.WorkingsBox.insert(END, 'No input for d found\n')
            self.GotAllInputs = False

        if self.GotAllInputs == False:
            App.WorkingsBox.insert(END, '\n')
    def DoOneStep(self, Xn):
        try:
            self.CurrentX = self.CurrentX + 1
            YValue = self.XCubedCoefficient * (Xn) ** 3 + self.XSquaredCoefficient * (Xn) ** 2 + self.XCoefficient * (Xn) + self.YIntercept

            if self.LimitReached == True:
                App.WorkingsBox.insert(END, 'Limit has been reached\n')
            elif ('%.6f' % self.TempYValue) == ('%.6f' % (YValue)):
                App.WorkingsBox.insert(END, 'X'+str(self.CurrentX)+' = '+str(Xn)+'\n')
                self.Limit = YValue
                App.WorkingsBox.insert(END, 'Limit = '+str(self.Limit)+'\n')
                self.CurrentX = 0
                App.Answer = self.Limit
                self.LimitReached = True
            else:
                #Plot the trails
                App.WorkingsBox.insert(END, 'X'+str(self.CurrentX)+' = '+str(Xn)+'\n')
                App.PlotTrail(Xn, Xn, Xn, YValue)
                App.PlotTrail(Xn, YValue, YValue, YValue)
                self.TempYValue = YValue
        except OverflowError:
            App.WorkingsBox.insert(END, '\nResult too large, sequence does not converge to a limit\n')
            
#Recursive Algorithm        
    def PolynomialRoot(self, Xn):
        try:
            self.CurrentX = self.CurrentX + 1
            YValue = self.XCubedCoefficient * (Xn) ** 3 + self.XSquaredCoefficient * (Xn) ** 2 + self.XCoefficient * (Xn) + self.YIntercept

            #Plot the trails
            App.WorkingsBox.insert(END, 'X'+str(self.CurrentX)+' = '+str(Xn)+'\n')
            App.PlotTrail(Xn, Xn, Xn, YValue)
            App.PlotTrail(Xn, YValue, YValue, YValue)

            if ('%.6f' % self.TempYValue) == ('%.6f' % (YValue)):
                self.Limit = YValue
                App.WorkingsBox.insert(END, 'Limit = '+str(self.Limit)+'\n')
                self.CurrentX = 0
                App.Answer = self.Limit
                self.LimitReached = True
            else:
                self.TempYValue = YValue
                self.PolynomialRoot(self.TempYValue)    #Method calls itself until limit is found
        except OverflowError:
            App.WorkingsBox.insert(END, '\nResult too large, sequence does not converge to a limit\n')

#Create callback for finding the root
    def FindTheRootCallback(self, event):
        self.FindTheRoot(self.X1)

#Create class for exponential functions
class Exponential(Application):
    def __init__(self, parent):
        #Setup Attributes
        self.parent = parent
        self.eCoefficient = 1
        self.CoefficientOfExponent = 1
        self.YTranslation = 0
        self.Limit = None
        self.LimitReached = False
        self.X1 = '0'
        self.TempYValue = 0
        self.CurrentX = 0

        #Startup Methods
        self.eCoefficientInput(self.parent)
        self.CoefficientOfTheExponentInput(self.parent)
        self.YTranslationInput(self.parent)
        self.X1Input(self.parent)
        self.ChangeText()

#Change the instruction text to tell the user how to use the exponential parameters
    def ChangeText(self):
        App.InstructionsTextBox.config(state = NORMAL)
        App.InstructionsTextBox.delete(1.0, END)
        App.InstructionsTextBox.insert(END, '''You are working with Exponential graphs.
\n\nThe exponential equations are written as\n"a^bx + c", where a, b and c are your inputs.
\nInputs of "e" can be used for e^x graphs.
\n\nThe box that says "X1" is for the first value of x in the sequence you are using.
\n\nNote: the symbol "^" is the symbol for powers/orders, for example you would read "x^3" as "x cubed"''', 'center-text')
        App.InstructionsTextBox.config(state = DISABLED)

#Create input boxes
    def eCoefficientInput(self, Frame):
        self.InputFrame1 = ttk.Labelframe(Frame, text = 'a')
        self.InputFrame1.grid(row = 1, column = 0)
        self.eCoefficientInput = Entry(self.InputFrame1)
        self.eCoefficientInput.grid()

    def CoefficientOfTheExponentInput(self, Frame):
        self.InputFrame2 = ttk.Labelframe(Frame, text = '^bx')
        self.InputFrame2.grid(row = 1, column = 1)
        self.CoefficientOfExponentInput = Entry(self.InputFrame2)
        self.CoefficientOfExponentInput.grid()

    def YTranslationInput(self, Frame):
        self.InputFrame3 = ttk.Labelframe(Frame, text = '+c')
        self.InputFrame3.grid(row = 1, column = 2)
        self.YTranslationInput = Entry(self.InputFrame3)
        self.YTranslationInput.grid()

    def X1Input(self, Frame):
        self.InputFrame4 = ttk.Labelframe(Frame, text = 'X1')
        self.InputFrame4.grid(row = 2)
        self.X1Input = Entry(self.InputFrame4)
        self.X1Input.grid()

#Retrieve inputs for calculations
#NOTE: Add checks for the inputs
    def GetExpoInputs(self):
        #Check if inputs are there
        self.GotAllInputs = True

        #eCoefficient
        self.eCoefficient = self.eCoefficientInput.get()
        if self.eCoefficient != '':
            IsANumber = True
            for loop in range(0, len(self.eCoefficient)):
                if self.eCoefficient[loop].isdigit() == False:
                    if self.eCoefficient[loop] == '/' or self.eCoefficient[loop] == '.':
                        if self.eCoefficient[loop-1].isdigit() == False:
                            IsANumber = False
                        elif self.eCoefficient.endswith('/', 0, len(self.eCoefficient)) == True:
                            IsANumber = False
                    elif self.eCoefficient[loop] == 'e' or self.eCoefficient[loop] == '-':
                        None
                    else:
                        IsANumber = False
            if IsANumber == False:
                App.WorkingsBox.insert(END, '(a) Incorrect type of input\n')
                self.GotAllInputs = False
            else:
                self.eCoefficient = eval(self.eCoefficient)
        else:
            App.WorkingsBox.insert(END, 'No input for a found\n')
            self.GotAllInputs = False

        #CoefficientOfExponent
        self.CoefficientOfExponent = self.CoefficientOfExponentInput.get()
        if self.CoefficientOfExponent != '':
            IsANumber = True
            for loop in range(0, len(self.CoefficientOfExponent)):
                if self.CoefficientOfExponent[loop].isdigit() == False:
                    if self.CoefficientOfExponent[loop] == '/' or self.CoefficientOfExponent[loop] == '.':
                        if self.CoefficientOfExponent[loop-1].isdigit() == False:
                            IsANumber = False
                        elif self.CoefficientOfExponent.endswith('/', 0, len(self.CoefficientOfExponent)) == True:
                            IsANumber = False
                    elif self.CoefficientOfExponent[loop] == 'e' or self.CoefficientOfExponent[loop] == '-':
                        None
                    else:
                        IsANumber = False
            if IsANumber == False:
                App.WorkingsBox.insert(END, '(^bx) Incorrect type of input\n')
                self.GotAllInputs = False
            else:
                self.CoefficientOfExponent = eval(self.CoefficientOfExponent)
        else:
            App.WorkingsBox.insert(END, 'No input for ^bx found\n')
            self.GotAllInputs = False

        #YTranslation
        self.YTranslation = self.YTranslationInput.get()
        if self.YTranslation != '':
            IsANumber = True
            for loop in range(0, len(self.YTranslation)):
                if self.YTranslation[loop].isdigit() == False:
                    if self.YTranslation[loop] == '/' or self.YTranslation[loop] == '.':
                        if self.YTranslation[loop-1].isdigit() == False:
                            IsANumber = False
                        elif self.YTranslation.endswith('/', 0, len(self.YTranslation)) == True:
                            IsANumber = False
                    elif self.YTranslation[loop] == 'e' or self.YTranslation[loop] == '-':
                        None
                    else:
                        IsANumber = False
            if IsANumber == False:
                App.WorkingsBox.insert(END, '(c) Incorrect type of input\n')
                self.GotAllInputs = False
            else:
                self.YTranslation = eval(self.YTranslation)
        else:
            App.WorkingsBox.insert(END, 'No input for c found\n')
            self.GotAllInputs = False

        if self.GotAllInputs == False:
            App.WorkingsBox.insert(END, '\n')
            
#Method to perform a single iteration of the given sequence
    def DoOneStep(self, Xn):
        try:
            self.CurrentX = self.CurrentX + 1
            YValue = self.eCoefficient ** (self.CoefficientOfExponent * Xn) + self.YTranslation

            if self.LimitReached == True:
                App.WorkingsBox.insert(END, 'Limit has been reached\n')
            elif ('%.6f' % self.TempYValue) == ('%.6f' % YValue):
                App.WorkingsBox.insert(END, 'X'+str(self.CurrentX)+' = '+str(Xn)+'\n')
                self.Limit = YValue
                App.WorkingsBox.insert(END, 'Limit = '+str(self.Limit)+'\n')
                self.CurrentX = 0
                App.Answer = self.Limit
                self.LimitReached = True
            else:
                #Plot the trails
                App.WorkingsBox.insert(END, 'X'+str(self.CurrentX)+' = '+str(Xn)+'\n')
                App.PlotTrail(Xn, Xn, Xn, YValue)
                App.PlotTrail(Xn, YValue, YValue, YValue)
                self.TempYValue = YValue
        except OverflowError:
            App.WorkingsBox.insert(END, '\nResult too large, sequence does not converge to a limit\n')
            
#Recursive Algorithm
    def ExponentialRoot(self, Xn):
        try:
            self.CurrentX = self.CurrentX + 1
            YValue = self.eCoefficient ** (self.CoefficientOfExponent * Xn) + self.YTranslation

            #Plot the trails
            App.WorkingsBox.insert(END, 'X'+str(self.CurrentX)+' = '+str(Xn)+'\n')
            App.PlotTrail(Xn, Xn, Xn, YValue)
            App.PlotTrail(Xn, YValue, YValue, YValue)

            if ('%.6f' % self.TempYValue) == ('%.6f' % YValue):
                self.Limit = YValue
                App.WorkingsBox.insert(END, 'Limit = '+str(self.Limit)+'\n')
                self.CurrentX = 0
                App.Answer = self.Limit
                self.LimitReached = True
            else:
                self.TempYValue = YValue
                self.ExponentialRoot(self.TempYValue)   #Method calls itself until the limit is found
        except OverflowError:
            App.WorkingsBox.insert(END, '\nResult too large, sequence does not converge to a limit\n')

Root = Tk()
Root.wm_title('Staircase and Cobweb Diagram Plotter')
App = Application(Root)
Root.mainloop()


