# config

STYLESHEET = """
    QMainWindow{
        background-color: #f8fcfe;
    }
    QWidget {
        font-family: 'Montserrat';
        font-size: 14px;
    }
    QWidget#dropZone {
        border: 2px dashed #f48fb1;
        border-radius: 2px;
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
"""
