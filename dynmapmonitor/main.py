import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer, QDateTime
from data_processing import fetch_player_data, get_time, format_time

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Account", "Health", "Armor", "X", "Y", "Z"])

        layout.addWidget(self.table)

        self.timestamp_label = QLabel()
        layout.addWidget(self.timestamp_label)

        self.setLayout(layout)
        self.setWindowTitle('Player Information')

        # Set dark mode stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #222;
                color: white;
            }
            QTableWidget {
                alternate-background-color: #444;
            }
            QTableWidget QHeaderView::section {
                background-color: #333;
                color: white;
                padding: 4px;
            }
        """)

        self.update_data()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second

    def update_data(self):
        players, server_time = fetch_player_data()

        # Sort players list by account alphabetically
        players.sort(key=lambda x: x.get("account", "").lower())

        self.table.setRowCount(len(players))
        for i, player in enumerate(players):
            account = player.get("account", "")
            health = player.get("health")
            armor = player.get("armor")
            x = player.get("x")
            y = player.get("y")
            z = player.get("z")

            # Modify account name based on presence of dot
            if account.startswith("."):
                display_account = account[1:] + " (Bedrock)"
            else:
                display_account = account + " (Java)"

            account_item = QTableWidgetItem(display_account)
            health_item = QTableWidgetItem(str(health))
            armor_item = QTableWidgetItem(str(armor))
            x_item = QTableWidgetItem(str(x))
            y_item = QTableWidgetItem(str(y))
            z_item = QTableWidgetItem(str(z))

            self.table.setItem(i, 0, account_item)
            self.table.setItem(i, 1, health_item)
            self.table.setItem(i, 2, armor_item)
            self.table.setItem(i, 3, x_item)
            self.table.setItem(i, 4, y_item)
            self.table.setItem(i, 5, z_item)

            # Set text color of all table items to white
            for j in range(6):
                self.table.item(i, j).setForeground(QColor("white"))

            # Check the world field and set row color accordingly
            world = player.get("world", "")
            if world == "realworld3":
                for j in range(6):
                    self.table.item(i, j).setBackground(QColor("green"))
            elif world == "realworld3_nether":
                for j in range(6):
                    self.table.item(i, j).setBackground(QColor("red"))
            elif world == "realworld3_the_end":
                for j in range(6):
                    self.table.item(i, j).setBackground(QColor("black"))

        if server_time is not None:
            hours, minutes = get_time(server_time)
            formatted_time = format_time(hours, minutes)
            self.timestamp_label.setText(f"Server Time: {formatted_time}")
        else:
            self.timestamp_label.setText("Error fetching data")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
