# -*- coding: utf-8 -*-

"""
Web album is a pure UI operation.
As such all of the logic is contained in this module.
There is no separate operation module for the file system operations.
There is a separate .ui file for the dialog.
"""

import os
from urllib.parse import unquote

from PyQt6.QtCore import QFileInfo, QFile, QIODevice, QTextStream
from PyQt6.QtWidgets import QDialog, QMessageBox

from src.ui.designer.web_album import Ui_web_album
from threaded_resizer.threaded_resizer import Supervisor, ImageResizeTask
from ui import constants


def handle_web_album(main_window):
    folder_select = main_window.folder_select
    browser_selection: list[QFileInfo] = main_window.browser.get_selection()
    resize_supervisor = main_window.supervisor  # this module will use the same threaded resize as the browser
    if len(browser_selection) == 0:
        QMessageBox.warning(main_window, "No selection", "Create a selection first.")
    else:
        """create the dialog"""
        dlg = WebAlbumDialog(browser_selection, resize_supervisor)
        dlg.exec()


class WebAlbumDialog(QDialog, Ui_web_album):
    """
    WebAlbumDialog is a dialog that allows the user to create the web album.
    """

    def __init__(self, files: list[QFileInfo], supervisor: Supervisor, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.text_box.setOpenLinks(False)

        self.files: list[QFileInfo] = files
        self.supervisor = supervisor

        self.set_initial_output_location()
        self.progress = 0
        self.total = len(self.files) * 3 + 2  # 2 x resize + 1 x html pages + 1x index + 1x css

        self.error = False  # bool to keep track of an error or a user interrupt
        self.setup_slots()

    def setup_slots(self):
        self.btn_cancel.pressed.connect(self.interupt_resize)
        self.btn_create.pressed.connect(self.create_web_album)
        self.text_box.anchorClicked.connect(self.open_url)
        self.supervisor.newItemReady.connect(self.process_resized_image)

    def open_url(self, qurl):
        """If the user clicks on a link in the text box, open it in the default browser."""
        link = unquote(qurl.toString())
        os.startfile(link)

    def set_initial_output_location(self):
        """set the default location to a subfolder called web next to the folder of the first file"""
        file_info = self.files[0]
        base_dir = os.path.abspath(os.path.join(file_info.dir().path(), os.pardir))
        new_folder_path = os.path.join(base_dir, "web")
        self.edit_location.setText(new_folder_path)

    def log(self, txt):
        """append a message to the text box"""
        self.text_box.append(txt)

    def update_progress_bar(self):
        """update the progress bar and check if the entire process is done"""
        self.progress += 1
        x = int(self.progress / self.total * 100)
        self.progress_bar.setValue(x)
        if x == 100:
            self.log_finished_message()

    def log_finished_message(self):
        """Log the finished message and the location of the created files."""
        self.log("Finished...")
        self.log("Location of the directory:")
        self.log("<a href='" + self.edit_location.text() + "'>" + self.edit_location.text() + "</a>")
        self.log("Location of the index:")
        self.log(
            "<a href='" + self.edit_location.text() + "/index.html" + "'>" + self.edit_location.text() + "/index.html" + "</a>")

    def interupt_resize(self):
        """interupt the resize process and clear the resizer queue"""
        self.log("Aborting...")
        self.error = True
        self.supervisor.clear_queue()

    def create_web_album(self):
        """trigger the creation of the web album html files and resized images"""
        html_template_strings: dict['str', 'str'] = self.generate_html_templates()
        self.create_all_html_files(html_template_strings)
        self.start_resize_process()

    def create_all_html_files(self, templates: dict[str, str]):
        """create the html files and css for the web album"""
        # create the folder
        self.log("STEP 1/5: Creating directory")
        newPath = self.edit_location.text()
        file = self.files[0]
        folder_path = file.dir()

        if folder_path.mkpath(newPath):
            self.log("Directory created...")
        else:
            self.error = True
            self.log("Creating directory failed...")

        self.log("STEP 2/5: Creating index page & css")
        # write CSS
        name = self.edit_location.text() + "/main.css"

        fh = QFile(name)
        if not fh.open(QIODevice.OpenModeFlag.WriteOnly):
            self.error = True
            self.log("Creating of main.css failed...")
        else:
            stream = QTextStream(fh)
            stream << templates["css"]
            self.log("main.css generated...")
            self.update_progress_bar()

        # create the html page with the thumbnailoverview
        if not self.error:
            name = self.edit_location.text() + "/index.html"

            fh = QFile(name)
            if not fh.open(QIODevice.OpenModeFlag.WriteOnly):
                self.log("Creating of main.css failed...")
                self.error = True
            else:
                stream = QTextStream(fh)
                text = templates["album_top"]
                text = text.replace("ALBUMTITLE", self.edit_title.text())
                text = text.replace("ALBUMDESCRIPTION", self.edit_description.text())
                stream << text

                # add thumbnails in a table 3 per row
                i = 1
                for file in self.files:
                    if i % 3 == 1:
                        if i < 3:
                            stream << "<tr>"
                        else:
                            stream << "</tr><tr>"
                    text = templates["thumbnail"]
                    text = text.replace("CHTML", file.baseName() + ".html")
                    text = text.replace("CPICSMALL", "1_" + file.fileName())
                    stream << text

                    i += 1

                stream << templates["album_bottom"]
                self.log("index.html generated...")
                self.update_progress_bar()

        # create the html pages for the single image views
        if not self.error:
            self.log("STEP 3/5: Creating single image html pages")

            NEXTHTML = ""
            PREVHTML = ""
            CURRENTPIC = ""
            i = 0
            for file in self.files:
                # create the html file
                name = file.baseName() + ".html"
                name = self.edit_location.text() + "/" + name

                # create the file handle
                fh = QFile(name)
                if not fh.open(QIODevice.OpenModeFlag.WriteOnly):
                    self.log("Creating of html file failed: " + name)
                    self.error = True
                else:
                    if i > 0:
                        PREVHTML = self.files[i - 1].baseName() + ".html"
                    else:
                        PREVHTML = ""
                    if i < len(self.files) - 1:
                        NEXTHTML = self.files[i + 1].baseName() + ".html"
                    else:
                        NEXTHTML = ""
                    CURRENTPIC = "0_" + file.fileName()

                    html = templates["zoom"].replace("PREVHTML", PREVHTML)
                    html = html.replace("NEXTHTML", NEXTHTML)
                    html = html.replace("CURRENTPIC", CURRENTPIC)

                    stream = QTextStream(fh)
                    stream << html

                    self.update_progress_bar()

                i += 1

        self.log("Finished")

    def start_resize_process(self):
        """start the resize process for the thumbnails and resized images"""
        output_folder_path = self.edit_location.text()
        if not self.error:
            self.log("STEP 4/5: Creating thumbnails")
            image_resize_tasks = [ImageResizeTask(file_info, constants.WEB_ALBUM_THUMBNAIL_SIZE, fast=False) for
                                  file_info in self.files]
            self.queue_for_thumbnail_images = self.supervisor.add_items(image_resize_tasks)
            self.supervisor.process_queue()

            self.log("STEP 5/5: Creating resized images")
            image_resize_tasks = [ImageResizeTask(file_info, constants.WEB_ALBUM_ZOOM_SIZE, fast=False) for file_info in
                                  self.files]
            self.queue_for_zoomed_images = self.supervisor.add_items(image_resize_tasks)
            self.supervisor.process_queue()

    def process_resized_image(self, ticket, img):
        output_folder_path = self.edit_location.text()

        # look for the matching imageresizetask in both queues
        match = None
        for item in self.queue_for_thumbnail_images:
            if item.ticket == ticket:
                match = item  # ImageResizeTask
                new_file_name = "1_"
                break
        if not match:
            for item in self.queue_for_zoomed_images:
                if item.ticket == ticket:
                    match = item
                    new_file_name = "0_"
                    break

        # save the image to disk with the proper filename
        if match:
            file_info = match.file_info
            new_file_name += file_info.baseName()
            new_file_name += "."
            new_file_name += file_info.completeSuffix()
            newNameAbs = output_folder_path + "/" + new_file_name

            if img.save(newNameAbs):
                self.update_progress_bar()
                # print("success")
            else:
                self.log("Failed to write an image...")
                # print("failed")

    def generate_html_templates(self):
        """generate the html templates for the web album"""
        templates = dict()
        templates['zoom'] = """
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

        templates['album_top'] = """
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
        templates['album_bottom'] = """
            </table>
</div>

</body>
</html>
"""

        templates['thumbnail'] = """
        <td class="thumbcell"><a href="CHTML"><img src="CPICSMALL" title="CHTML" alt="CPICSMALL" /></a></td>
        """

        templates['css'] = """

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
        return templates
