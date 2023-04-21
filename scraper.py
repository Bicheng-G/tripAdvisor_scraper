import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
import crawler

def run_script():
    city = city_entry.text()
    start_page = int(start_page_entry.text())
    num_pages = int(num_pages_entry.text())
    # print("City:", city)
    # print("Start Page:", start_page)
    # print("Number of Pages:", num_pages)
    
    # Call your script function here and pass the arguments
    # your_script_function(city, start_page, num_pages)
    crawler.scrape(city, start_page, num_pages)

app = QApplication(sys.argv)

# Create main window
main_window = QWidget()
main_window.setWindowTitle("Python Script GUI")

# Create layout
layout = QVBoxLayout()

# Create labels
city_label = QLabel("City:")
start_page_label = QLabel("Start Page:")
num_pages_label = QLabel("Number of Pages:")

# Create entry fields
city_entry = QLineEdit()
start_page_entry = QLineEdit()
num_pages_entry = QLineEdit()

# Create run button
run_button = QPushButton("Run")
run_button.clicked.connect(run_script)

# Add widgets to layout
layout.addWidget(city_label)
layout.addWidget(city_entry)
layout.addWidget(start_page_label)
layout.addWidget(start_page_entry)
layout.addWidget(num_pages_label)
layout.addWidget(num_pages_entry)
layout.addWidget(run_button)

# Set layout
main_window.setLayout(layout)

# Show main window
main_window.show()

# Run the main loop
sys.exit(app.exec_())
