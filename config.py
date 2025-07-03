STYLESHEET = """
    QMainWindow {
        background-color: #f8fcfe;
    }
    QWidget {
        font-family: 'Montserrat';
        font-size: 14px;
        color: #000000;
    }
    QWidget#dropZone {
        border: 2px dashed #f48fb1;
        border-radius: 2px;
    }
    QWidget#dropZone:hover {
        background: #F4DBE3;
    }
    QGroupBox {
        border: 1px solid #f48fb1;
        border-radius: 8px;
        margin-top: 1em;
        font-weight: bold;
    }
    QTextEdit {
        border: 2px dashed #f48fb1;
        background-color: #f8fcfe;
    }
    QLabel#frameSelect {
        border: 2px dashed #f48fb1;
    }
    QSlider::groove:horizontal {
        border: 1px solid #f4b6c2;
        height: 8px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #fff0f5, stop:1 #ffe4ec);
        border-radius: 4px;
    }
    QSlider::sub-page:horizontal {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #f8bbd0, stop:1 #f48fb1);
        border: 1px solid #f48fb1;
        height: 8px;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        background: #f8f8f8;
        border: 1px solid #ccc;
        width: 14px;
        height: 14px;
        margin: -3px 0;
        border-radius: 7px;
    }
    QPushButton {
        background: #f48fb1;
        color: #ffffff;
        border: 0px;
        font-family: 'Montserrat';
        font-weight: bold;
        border-radius: 4px;
    }
    QPushButton:hover {
        background: #F477A1;
    }
    QPushButton:pressed {
        background: #994A64;
    }
    QComboBox {
        background: #ffffff;
        color: #f06292;
        border: 2px solid #f48fb1;
        font-family: 'Montserrat';
        font-weight: bold;
        border-radius: 6px;
        padding: 4px;
    }
    QComboBox QAbstractItemView {
        margin: 0px;
        padding: 0px;
    }
    QComboBox::drop-down {
        border: 0px;
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 40px;
    }

    QComboBox::item {
        background: #ffffff;
        selection-background-color: #f48fb1;
        selection-color: #ffffff;
    }
    QCheckBox:hover {
        outline: 0px;
        border: 0px;
        background: #f8f8f8;
    }
    
    QListView {
        outline: 0px;
        border: 0px;
        background: #f8f8f8;
    }
"""
