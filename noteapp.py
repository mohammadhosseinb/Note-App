import sys
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QApplication , QLabel
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QMessageBox
from uuid import uuid4
from PySide6.QtCore import Qt
import pandas as pd

class NoteManager:
    def __init__(self):
        self.notes = {}
    
    def add_note(self, note_name, note_description):
         if note_name == "" :
             return
         note_id = str(uuid4())
         self.notes[note_id] = {"title": note_name, "description": note_description}

    def load_data(self):
        df = pd.read_csv("notedata.csv")
        for i in range(len(df)):
            note = df.loc[i,:].to_list()
            self.notes[note[1]]={"title": note[2], "description": note[3]}

    def save_data(self):
        df = list()
        for note in self.notes.items():
            note_dict = {"note_id": note[0], "title": note[1]["title"], "description": note[1]["description"]}
            df.append(note_dict)
        df = pd.DataFrame(df)
        df.to_csv("notedata.csv")

class NoteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = NoteManager()
        #self
        self.load_data()
        self.setup_window()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def load_data(self):
        try:
            self.manager.load_data()
        except:
            print("No such file or directory: 'notedata.csv'")
    def setup_window(self):
        self.setWindowTitle("Note App")
        self.resize(1080, 720)
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

    def create_widgets(self):
        self.note_name = QLabel("note name")
        self.app_name_label = QLabel('Note list')
        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText("write a new note . . .")
        self.note_list = QListWidget()
        self.note_list.setMaximumSize(200,634)
        self.note_name_edit = QLineEdit()
        self.note_name_edit.setPlaceholderText("note name *")

        #buttons
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.add_button = QPushButton("Add")
        self.clear_button = QPushButton("cancle select")
        self.clear_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.edit_button.setEnabled(False)
    def create_layout(self):
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        #--------------------------------------left layout
        left_layout.addWidget(self.app_name_label)
        left_layout.addWidget(self.note_list)
        left_layout.addWidget(self.clear_button)
        self.refresh_note_list()
        #--------------------------------------right layout
        option_layout = QHBoxLayout()
        #option menu
        option_layout.addWidget(self.note_name)
        option_layout.addWidget(self.add_button)
        option_layout.addWidget(self.edit_button)
        option_layout.addWidget(self.delete_button)
        right_layout.addLayout(option_layout)

        #name field
        right_layout.addWidget(self.note_name_edit)
        
        #text editor
        right_layout.addWidget(self.text_editor)

        #add to main layout
        self.main_layout.addLayout(left_layout)
        self.main_layout.addLayout(right_layout)

    def create_connections(self):
        self.add_button.clicked.connect(self.add_note)
        self.note_list.itemClicked.connect(self.show_detail)
        self.note_list.itemClicked.connect(self.clear_option)
        self.edit_button.clicked.connect(self.edit_note)
        self.delete_button.clicked.connect(self.delete_note)

    def refresh_note_list(self):
        self.note_list.clear()
        note_dict = self.manager.notes
        for id, note in note_dict.items():
            item = QListWidgetItem()
            item.setText(note["title"])
            item.setData(Qt.UserRole, id)
            self.note_list.addItem(item)
        self.manager.save_data()

    def add_note(self):
        note_name = self.note_name_edit.text()
        description = self.text_editor.toPlainText()
        self.manager.add_note(note_name, description)
        self.refresh_note_list()
        self.note_name_edit.clear()
        self.text_editor.clear()
        self.note_name.setText("note name")
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.note_name_edit.setPlaceholderText("note name *")

    def edit_note(self):
        item = self.note_list.currentItem()
        note_id = item.data(Qt.UserRole)
        title = self.manager.notes[note_id]["title"]
        description = self.manager.notes[note_id]["description"]

        new_title = self.note_name_edit.text()
        new_description = self.text_editor.toPlainText()

        if new_description == description and new_title == "":
            return
        if new_title == "":
            new_title = title
        self.manager.notes[note_id]["title"] = new_title
        self.manager.notes[note_id]["description"] = new_description
        self.refresh_note_list()
        self.note_name_edit.clear()
        self.text_editor.clear()
        self.note_name.setText("note name")
        QMessageBox.information(self, "Edit", "Edit complete")
        self.note_name.setText("note name")
        self.note_name_edit.setPlaceholderText("note name *")
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        
    def delete_note(self):
        reply = QMessageBox.question(
        self, "Delete Note", "Are you sure you want to delete this note?")
        if reply == QMessageBox.No:
            return
        item = self.note_list.currentItem()
        note_id = item.data(Qt.UserRole)
        self.manager.notes.pop(note_id)
        self.refresh_note_list()
        self.note_name_edit.clear()
        self.text_editor.clear()
        self.note_name.setText("note name")
        self.note_name_edit.setPlaceholderText("note name *")
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.clear_button.setEnabled(False)

    def show_detail(self, item):
        note_id = item.data(Qt.UserRole)
        title = self.manager.notes[note_id]["title"]
        description = self.manager.notes[note_id]["description"]
        self.note_name.setText(title)
        self.text_editor.setText(description)
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)
    
    def clear_option(self):
        self.note_name_edit.setPlaceholderText(self.note_name.text() + " . . .")
        def clear_func():
            self.note_list.clearFocus()
            self.note_name_edit.clear()
            self.text_editor.clear()
            self.note_name.setText("note name")
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.clear_button.setEnabled(False)
            self.note_name_edit.setPlaceholderText("note name *")

        self.clear_button.setEnabled(True)
        self.clear_button.clicked.connect(clear_func)
        

app = QApplication(sys.argv)
window = NoteApp()
window.show()
app.exec()