
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from resources.uipy.web import *
import os


class WebAlbum(QDialog, Ui_WebAlbum):
    
    def __init__(self, files, supervisor, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.textBox.setOpenLinks(False)
        
        self.files = files #QFileInfo objects
        self.supervisor = supervisor

        self.setInitPath()
        self.progress = 0 
        self.total = len(self.files)*3 + 2 #2 x resize + 1 x html pages + 1x index + 1x css       
               
        self.error = False
        self.setupSlots()
        
        
    def setupSlots(self):
        self.btnCancel.pressed.connect(self.interuptResize)
        self.btnCreate.pressed.connect(self.gameTime)      
        self.textBox.anchorClicked.connect(self.openUrl)
        self.supervisor.newItemReady.connect(self.treatResizedImage)
        
 
    def openUrl(self, qurl):
        link = qurl.toString()
        os.startfile(link)
    
   
    def setInitPath(self):
        fi = self.files[0]
        dir = fi.dir()
        dirName = dir.dirName()
        path = fi.absolutePath()
        self.editLocation.setText(path + "/../web/")
                
  
    def log(self,txt):
        self.textBox.append(txt)

   
    def updateProgressBar(self):
        self.progress += 1
        x = self.progress / self.total * 100
        self.progressBar.setValue(x)
        
        if x == 100:
            self.log("Finished...")
            self.log("Location of the directory:")
            self.log("<a href='" + self.editLocation.text()+"'>"+self.editLocation.text()+"</a>")
            self.log("Location of the index:")
            self.log("<a href='" + self.editLocation.text() +"/index.html"+"'>"+self.editLocation.text() +"/index.html"+"</a>")


    def interuptResize(self):
        self.log("Aborting...")
        self.error = True
        self.supervisor.clear_queue()
        
        
    def gameTime(self):
        self.html()
        self.createAllHTMLFiles()
        self.startResizeProcess()
    
    
    def html(self):
        self.html_2_text = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
   <title></title>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <link rel="prefetch" href="CURRENTPIC" />
   <link rel="stylesheet" type="text/css" href="main.css" />
</head>
<body>
   <h1 class="title"></h1>
   <div id="photograph">
    <a href="NEXTHTML"><img src="CURRENTPIC" title="CURRENTPIC" alt="CURRENTPIC" /></a>
   </div>

<div id="navigation">
    <tr class="textnavigation">
        <td class="previous"><span class="previous"><a href="PREVHTML" title="Next Photograph">&lt;&lt; </span></td>
        <td class="index" colspan="3"><span class="index"><a href="index.html" title="Return to Index">^</a></span></td>
        <td class="next"><span class="next"><a href="NEXTHTML" title="Next Photograph">&gt;&gt;</a></span></td>
    </tr>
    </table>
</div>

</body>
</html>
"""

        self.html_3_text = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
   <title>ALBUMTITLE</title>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
   <link rel="stylesheet" type="text/css" href="main.css" />
</head>
<body>
   <div id="header">
      <h1>ALBUMTITLE</h1>
   </div>
<p class="description">ALBUMDESCRIPTION</p>
   
<div id="index">
    <table>
    """
        self.html_4_text = """
            </table>
</div>

</body>
</html>
"""

        self.html_5_text = """
        <td class="thumbcell"><a href="CHTML"><img src="CPICSMALL" title="CHTML" alt="CPICSMALL" /></a></td>
        """


        self.css_text = """
        
        /* Main Selectors */
body {
    background-color: #425164;
    color: #C0C0C0;
}

a, a:visited {
    background-color: transparent;
    color: #9BAAB3;
}

a:hover {
    background-color: transparent;
    color: #D0D6DD;
}

/* Header */
div#header h1 {
    font-family: tahoma, arial, helvetica, sans-serif;
    text-align: center;
    background-color: transparent;
    color: #C0C0C0;
}

/* Thumbnail Index */
div#index {
    margin: 1ex 0 1ex 0;
    text-align: center;
}

div#index table {
    text-align: center;
    margin: 0 auto 0 auto;
}

div#index td.thumbcell {
    width: 200px;
    border-style: solid;
    border-color: #6A798C;
    border-width: 1px;
    text-align: center;
    vertical-align: middle;
    padding: 10px;
}

div#index td.thumbcell img {
    border-style: none;
}

div#index div.pages {
    font-family: tahoma, arial, helvetica, sans-serif;
    font-size: 0.8em;
    text-align: right;
}

/* Photo Navigation */
div#navigation {
    text-align: center;
    font-family: tahoma, arial, helvetica, sans-serif;
    font-size: 0.8em;
    margin: 1ex 0 1ex 0;
}

div#navigation table {
    text-align: center;
    margin: 0 auto 0 auto;
}

div#navigation td.previous {
    text-align: left;
    width: 200px;
}

div#navigation td.index {
    text-align: center;
}

div#navigation td.next {
    text-align: right;
    width: 200px;
}

div#navigation td.thumbcell {
    width: 200px;
    border-style: solid;
    border-color: #6A798C;
    border-width: 1px;
    text-align: center;
    vertical-align: middle;
    padding: 10px;
}

div#navigation td.thumbcell img {
    border-style: none;
}

div#navigation td.selected {
    border-style: outset;
    border-width: 2px;
}

div#navigation span.home {
    display: block;
    padding-bottom: 1em;
}

/* Photograph */
div#photograph {
    text-align: center;
    margin: 1ex 0 1ex 0;
}

div#photograph img {
    margin: 0 auto 0 auto;
    border-style: solid;
    border-color: #C0C0C0;
    border-width: 1px;
}

/* Photograph Title */
h1.title {
    text-align: center;
    font-family: tahoma, arial, helvetica, sans-serif;
    font-size: 0.8em;
    font-weight: bold;
    margin: 0px;
}

/* Photograph Caption */
p.caption, p.description {
    font-family: tahoma, arial, helvetica, sans-serif;
    text-align: center;
    font-size: 0.8em;
    display: block;
    width: 1024px;
    margin: auto;
}

/* Footnote */
p.footnote {
    font-family: tahoma, arial, helvetica, sans-serif;
    font-size: 0.6em;
    text-align: right;
    padding: 0 2em 0 0;
}
"""

       
            
    def createAllHTMLFiles(self):
        #create the folder
        self.log("STEP 1/5: Creating directory")
        newPath = self.editLocation.text()
        fi = self.files[0]
        dirp = fi.dir()
        
        if dirp.mkpath(newPath):
            self.log("Directory created...")
        else:
            self.error = True
            self.log("Creating directory failed...")
            
        self.log("STEP 2/5: Creating index page & css")       
        #write CSS
        name = self.editLocation.text() +"/main.css"
        
        fh = QFile(name)
        if not fh.open(QIODevice.WriteOnly):
            self.error = True
            self.log("Creating of main.css failed...")
        else:
            stream = QTextStream(fh)
            stream << self.css_text
            self.log("main.css generated...")
            self.updateProgressBar()

        #create the html page with the thumbnailoverview
        if not self.error:
            name = self.editLocation.text() +"/index.html"
            
            fh = QFile(name)
            if not fh.open(QIODevice.WriteOnly):
                self.log("Creating of main.css failed...")
                self.error = True
            else:
                stream = QTextStream(fh)
                text = self.html_3_text
                text = text.replace("ALBUMTITLE",self.editTitle.text())
                text = text.replace("ALBUMDESCRIPTION",self.editDescription.text())
                stream << text
                
                i = 1
                for fi in self.files:
                    if i%3 == 1: 
                        if i < 3:
                            stream << "<tr>"
                        else:
                            stream << "</tr><tr>"
                    text = self.html_5_text
                    text = text.replace("CHTML",fi.baseName()+".html")
                    text = text.replace("CPICSMALL","1_"+fi.fileName())
                    stream << text
                    
                    i +=1
                
                stream << self.html_4_text
                self.log("index.html generated...")
                self.updateProgressBar()

        #create the html pages for the single image views
        if not self.error:
            self.log("STEP 3/5: Creating single image html pages")
            
            NEXTHTML = ""
            PREVHTML = ""
            CURRENTPIC = ""
            i = 0
            for fi in self.files:
                #create the html file
                name = fi.baseName() + ".html"
                name = self.editLocation.text() +"/"+name
                
                #create the file handle
                fh = QFile(name)
                if not fh.open(QIODevice.WriteOnly):
                    self.log("Creating of html file failed: "+name)
                    self.error = True
                else:
                    if i > 0:
                        PREVHTML = self.files[i-1].baseName()+".html"
                    else:
                        PREVHTML = ""
                    if i < len(self.files) - 1:
                        NEXTHTML = self.files[i+1].baseName()+".html"
                    else:
                        NEXTHTML = ""
                    CURRENTPIC = "0_"+fi.fileName()
                    
                    html = self.html_2_text.replace("PREVHTML",PREVHTML)
                    html = html.replace("NEXTHTML",NEXTHTML)
                    html = html.replace("CURRENTPIC",CURRENTPIC)
                    
                    
                    stream = QTextStream(fh)
                    stream << html
                    
                    self.updateProgressBar()
                    
                i+=1
                
        self.log("Finished")    

  
    def startResizeProcess(self):
        #create the thumbnails
        newPath = self.editLocation.text()
        if not self.error:
            self.log("STEP 4/5: Creating thumbnails")
            q = []
            for fi in self.files:
                q.append([fi, 150, False]) #not smooth
                self.queueSmall = self.supervisor.add_items(q)
                self.supervisor.process_queue()

            self.log("STEP 5/5: Creating resized images")
            q = []
            for fi in self.files:
                q.append([fi, 1250, True]) #smooth
                self.queueLarge = self.supervisor.add_items(q)
                self.supervisor.process_queue()

               
    def treatResizedImage(self, ticket, img):
        newPath = self.editLocation.text()
        match = False
        
        for item in self.queueSmall:
            if item[3] == ticket:
                match = item
                newName = "1_"
                break

        if not match: 
            for item in self.queueLarge:
                if item[3] == ticket:
                    match = item
                    newName = "0_"
                    break
                
        if match:                
            fileInfo = match[0]
            
            newName += fileInfo.baseName()
            newName += "."
            newName += fileInfo.completeSuffix()
            newNameAbs = newPath + "/" + newName
             
            if img.save(newNameAbs):
                self.updateProgressBar()
                #print("success")
            else:
                self.log("Failed to write an image...")
                #print("failed")

      
        
              

      