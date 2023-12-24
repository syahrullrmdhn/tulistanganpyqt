import sys
from PyQt6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,QWidget,QHBoxLayout,QVBoxLayout,QLabel,
                             QGraphicsPixmapItem, QGraphicsRectItem, QMainWindow,QMessageBox,
                             QGraphicsTextItem, QPushButton,QInputDialog,QComboBox,
                             QSlider,QVBoxLayout,QFileDialog,QColorDialog,QTextEdit,QDialog,QLineEdit)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import (QGuiApplication,QPixmap, 
                         QPainter, QImage, QFont, 
                         QKeySequence,QShortcut,QFont, 
                         QFontDatabase,QColor,QIcon)

class ImageCreator(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initLayout()
        self.center()
    
    def initUI(self):
        self.setWindowTitle('Create a Solid Color Background Image')
        self.setGeometry(100,100,300,300)
        self.setWindowIcon(QIcon('logo.png'))
    
    def center(self):
        qr=self.frameGeometry()
        cp=QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initLayout(self):

        self.color_label = QLabel('current color:(255,255,255,255)', self)
        self.color_button = QPushButton('choose the color', self)
        self.color=QColor('black')
        self.color_button.clicked.connect(self.showColorDialog)
        color_layout=QHBoxLayout()
        color_layout.addStretch(1)
        color_layout.addWidget(self.color_label)
        color_layout.addWidget(self.color_button)
        color_layout.addStretch(1)

        self.bg_a=QLabel('Image opacity：255')
        self.bg_a_slider=QSlider(Qt.Orientation.Horizontal)
        self.bg_a_slider.setRange(0, 255)
        self.bg_a_slider.setSingleStep(1)
        self.bg_a_slider.setValue(255)
        bg_a_layout=QHBoxLayout()
        bg_a_layout.addStretch(1)
        bg_a_layout.addWidget(self.bg_a)
        bg_a_layout.addWidget(self.bg_a_slider)
        bg_a_layout.addStretch(1)
        self.bg_a_slider.valueChanged.connect(self.update_bg_a_label)

        self.color_pre=QLabel('Color preview:')
        self.color_rect=QLabel()
        self.color_rect.setFixedSize(50,50)
        self.color_rect.setStyleSheet(f'background-color: {self.color.name()}')
        color_pre_layout=QHBoxLayout()
        color_pre_layout.addStretch(1)
        color_pre_layout.addWidget(self.color_pre)
        color_pre_layout.addWidget(self.color_rect)
        color_pre_layout.addStretch(1)

        self.width_label = QLabel('Image length:', self)
        self.width_input_line = QLineEdit(self)
        self.width_input_line.setPlaceholderText('Enter integer here')
        self.width_unit_label = QLabel('Pixel', self)
        width_input_layout = QHBoxLayout()
        width_input_layout.addStretch(1)
        width_input_layout.addWidget(self.width_label)
        width_input_layout.addWidget(self.width_input_line)
        width_input_layout.addWidget(self.width_unit_label)
        width_input_layout.addStretch(1)

        self.height_label = QLabel('Image width:', self)
        self.height_input_line = QLineEdit(self)
        self.height_input_line.setPlaceholderText('Enter integer here')
        self.height_unit_label = QLabel('Pixel', self)
        height_input_layout = QHBoxLayout()
        height_input_layout.addStretch(1)
        height_input_layout.addWidget(self.height_label)
        height_input_layout.addWidget(self.height_input_line)
        height_input_layout.addWidget(self.height_unit_label)
        height_input_layout.addStretch(1)

        self.create_button = QPushButton('Create image', self)
        self.create_button.clicked.connect(self.createImage)

        layout = QVBoxLayout()
        layout.addLayout(color_layout)
        layout.addLayout(bg_a_layout)
        layout.addLayout(color_pre_layout)

        layout.addLayout(width_input_layout)
        layout.addLayout(height_input_layout)

        layout.addWidget(self.create_button)

        self.setLayout(layout)
    
    def update_bg_a_label(self):
        self.bg_a.setText(f'Image opacity:{self.bg_a_slider.value()}')
        self.color.setAlpha(self.bg_a_slider.value())
        self.color_rect.setStyleSheet(f'background-color: {self.color.name()}')

    def showColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_label.setText(f'current color:{self.color.getRgb()}')
            self.color_button.setStyleSheet(f'background-color: {color.name()}')
            self.color_rect.setStyleSheet(f'background-color: {color.name()}')
            self.color = color

    def createImage(self):
        width = int(self.width_input_line.text())
        height = int(self.height_input_line.text())
        if width <= 0 or height <= 0:
            return
        if not hasattr(self, 'color'):
            return
        image = QPixmap(width, height)
        image.fill(self.color)
        image.save(f'./bgs/{self.color.name()}-{width}x{height}.png')
        QMessageBox.information(self, 'Prompt', 'The picture has been saved in the bgs directory!', QMessageBox.StandardButton.Ok)
        

class HandFontWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1200, 600)
        self.setWindowTitle('Tugas Pak Anas')
        self.setWindowIcon(QIcon('ittshd.png'))

        self.initView()
        self.config_widget=self.initConfigForm()


        main_layout = QHBoxLayout()
        main_layout.addWidget(self.config_widget)
        main_layout.addWidget(self.view)
        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

   
        export_shortcut = QShortcut(QKeySequence(QKeySequence.StandardKey.Save), self)
        export_shortcut.activated.connect(self.view.exportSceneToImage)

        self.updateView()

        self.show()
    
    def initView(self):
        self.my_scene = QGraphicsScene(self)
        self.view = GraphicsView(self.my_scene, self)
        self.setCentralWidget(self.view)

    def initConfigForm(self):
     
        config_widget = QWidget(self)
        config_layout = QVBoxLayout(config_widget)
      
        text_config_label = QLabel('Effect configuration:')
        config_layout.addWidget(text_config_label)
       
        self.label_bg=QLabel('letter.png')
        self.button_bg=QPushButton('Select background image')
        self.button_bg.clicked.connect(self.show_file_dialog)
        self.bg_path='./bgs/letter.png'
        config_layout.addWidget(self.label_bg)
        config_layout.addWidget(self.button_bg)

        creat_bg_layout=QHBoxLayout()
        creat_bg_label=QLabel('Don’t have a background image you like?')
        creat_bg_button=QPushButton('Create a solid color background')
        creat_bg_button.clicked.connect(self.create_bg_widget)
        creat_bg_layout.addWidget(creat_bg_label)
        creat_bg_layout.addWidget(creat_bg_button)
        config_layout.addLayout(creat_bg_layout)

        self.label_font = QLabel("Choose font:")
        self.combo_box = QComboBox(self)
        self.combo_box.addItem('Autography.otf')
        self.combo_box.addItem('Daykids.otf')
        self.combo_box.addItem('Study Alone.otf')
        self.combo_box.addItem('Handwind.ttf')
        config_layout.addWidget(self.label_font)
        config_layout.addWidget(self.combo_box)
        self.combo_box.currentIndexChanged.connect(self.updateView)

        self.label_font_color = QLabel("Current font color: black")
        self.button_font_color = QPushButton('Choose font color')
        self.font_color='black'
        config_layout.addWidget(self.label_font_color)
        config_layout.addWidget(self.button_font_color)
        self.button_font_color.clicked.connect(self.show_color_dialog)

        self.label_text=QLabel('text to display:')
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText('text to display')
        self.text_edit.setText('''It took me a day to talk to gpt3.5 and make hundreds of sentences, revise and revise, and finally achieve this effect.
My handwriting has always been poor, and I hate writing. I spend a lot of time practicing calligraphy, but my handwriting is worse than good. So when I saw the possibility of generating handwritten pictures, I couldn't wait to try it.
When I was halfway through, I suddenly thought if there was something already done online. Indeed, I was a little disappointed, but after taking a closer look, I found that its supposed operation was a bit more complicated than mine, so I continued to finish it and the result is now.''')
        # text_edit.toPlainText()
        self.text_edit.textChanged.connect(self.updateView)
        config_layout.addWidget(self.label_text)
        config_layout.addWidget(self.text_edit)


        self.slider_x = QSlider(Qt.Orientation.Horizontal)
        self.slider_x.setRange(0, 500)
        self.slider_x.setSingleStep(1)
        self.slider_x.valueChanged.connect(self.updateView)
        self.slider_x.setValue(0)
        self.label_x = QLabel("Text coordinate x: 0")
        config_layout.addWidget(self.label_x)
        config_layout.addWidget(self.slider_x)

        self.slider_y = QSlider(Qt.Orientation.Horizontal)
        self.slider_y.setRange(0, 800)
        self.slider_y.setSingleStep(1)
        self.slider_y.valueChanged.connect(self.updateView)
        self.slider_x.setValue(0)
        self.label_y = QLabel("Text coordinate y: 0")
        config_layout.addWidget(self.label_y)
        config_layout.addWidget(self.slider_y)

  
        self.slider_width = QSlider(Qt.Orientation.Horizontal)
        self.slider_width.setRange(10, 2000)
        self.slider_width.setSingleStep(1)
        self.slider_width.setValue(100)
        self.slider_width.valueChanged.connect(self.updateView)
        self.label_width = QLabel("Text display width: 100")
        config_layout.addWidget(self.label_width)
        config_layout.addWidget(self.slider_width)        
        
        self.slider_height = QSlider(Qt.Orientation.Horizontal)
        self.slider_height.setRange(1, 2000)
        self.slider_height.setSingleStep(1)
        self.slider_height.setValue(200)
        self.slider_height.valueChanged.connect(self.updateView)
        self.label_height = QLabel("Text display height: 200")
        config_layout.addWidget(self.label_height)
        config_layout.addWidget(self.slider_height)


        self.slider_font_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_font_size.setRange(1, 100)
        self.slider_font_size.setSingleStep(1)
        self.slider_font_size.setValue(16)
        self.slider_font_size.valueChanged.connect(self.updateView)
        self.label_font_size = QLabel("Text size: 16")
        config_layout.addWidget(self.label_font_size)
        config_layout.addWidget(self.slider_font_size)

        self.slider_font_weight = QSlider(Qt.Orientation.Horizontal)
        self.slider_font_weight.setRange(100, 1000)
        self.slider_font_weight.setSingleStep(100)
        self.slider_font_weight.setValue(500)
        self.slider_font_weight.valueChanged.connect(self.updateView)
        self.label_font_weight = QLabel("Text weight: 500")
        config_layout.addWidget(self.label_font_weight)
        config_layout.addWidget(self.slider_font_weight)


        self.slider_font_spacing = QSlider(Qt.Orientation.Horizontal)
        self.slider_font_spacing.setRange(-20,20)
        self.slider_font_spacing.setSingleStep(1)
        self.slider_font_spacing.setValue(2)
        self.slider_font_spacing.valueChanged.connect(self.updateView)
        self.label_font_spacing = QLabel("Font spacing: 0.1")
        config_layout.addWidget(self.label_font_spacing)
        config_layout.addWidget(self.slider_font_spacing)


        self.slider_line_spacing = QSlider(Qt.Orientation.Horizontal)
        self.slider_line_spacing.setRange(20,80)
        self.slider_line_spacing.setSingleStep(1)
        self.slider_line_spacing.setValue(40)
        self.slider_line_spacing.valueChanged.connect(self.updateView)
        self.label_line_spacing = QLabel("Line spacing: 1")
        config_layout.addWidget(self.label_line_spacing)
        config_layout.addWidget(self.slider_line_spacing)


        export_btn = QPushButton('Export pictures:', self)
        export_btn.clicked.connect(self.view.exportSceneToImage)
        config_layout.addWidget(export_btn)
        config_widget.setLayout(config_layout)

        return config_widget
    
    def create_bg_widget(self):
        self.dialog=ImageCreator()
        self.dialog.show()
    
    def show_file_dialog(self):

        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Open File')
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)


        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:

            selected_file = file_dialog.selectedFiles()[0]
            self.label_bg.setText(selected_file)
            self.bg_path=selected_file
            self.updateView()
    def show_color_dialog(self):

        color_dialog = QColorDialog(self)
        color_dialog.setWindowTitle('Choose Color')


        color_dialog.setCurrentColor(QColor(255, 0, 0))
        if color_dialog.exec() == QColorDialog.DialogCode.Accepted:
            self.font_color = color_dialog.currentColor().name()
            self.label_font_color.setText('Current font color:'+self.font_color)
            self.updateView()    

    def updateView(self):
        current_text = self.combo_box.currentText()
        font_path='./font/'+current_text
        self.label_x.setText(f"Text coordinate x:{self.slider_x.value()}")
        self.label_y.setText(f"Text coordinate y:{self.slider_y.value()}")
        self.label_font_size.setText(f"font size:{self.slider_font_size.value()}")
        self.label_font_weight.setText(f"Text weight:{self.slider_font_weight.value()}")
        self.label_font_color.setText(f"Current font color:{self.font_color}")
        self.label_font_spacing.setText(f"Text spacing:{round(self.slider_font_spacing.value()/20,2)}")
        self.label_line_spacing.setText(f"Row spacing x:{round(self.slider_line_spacing.value()/20,2)}")
        self.label_width.setText(f"Text display width:{self.slider_width.value()}")
        self.label_height.setText(f"Text display height:{self.slider_height.value()}")

        text_tmp=self.text_edit.toPlainText().replace(' ','&nbsp;').replace('\n','<br>')

        self.view.addTextItem(text=text_tmp, 
                        bg_path=self.bg_path,
                        font_path=font_path,
                        font_color=self.font_color,
                        font_weight=self.slider_font_weight.value(),
                        x=self.slider_x.value(),y=self.slider_y.value(),                        
                        font_size=self.slider_font_size.value(),
                        font_spacing=round(self.slider_font_spacing.value()/20,2),
                        line_spacing=round(self.slider_line_spacing.value()/40,2),
                        rect_width=self.slider_width.value(), 
                        rect_height=self.slider_height.value()
                        )

class GraphicsView(QGraphicsView):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)
        
        self.setStyleSheet('GraphicsView{background-color:#FDF6E3;}')
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  

        self.drawing_rect = None
        self.origin = None
        self.is_drawing = False
        self.coordinate_text_items = {}

    def wheelEvent(self, event):
        modifiers = event.modifiers()
        if modifiers == Qt.KeyboardModifier.ControlModifier:
           
            factor = 1.2  
            if event.angleDelta().y() < 0:
                factor = 1.0 / factor  
            self.scale(factor, factor)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            double_click_position = event.pos()
            double_click_scene_position = self.mapToScene(double_click_position)
            item = self.scene().itemAt(double_click_scene_position, self.transform())
            if isinstance(item, QGraphicsRectItem):
                rect_key = id(item)
                if rect_key in self.coordinate_text_items:
                    self.removeCoordinateTextItems(self.coordinate_text_items[rect_key])
                self.scene().removeItem(item)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if event.buttons() & Qt.MouseButton.RightButton:
            if self.is_drawing and self.origin is not None:
                current_position = event.pos()
                current_scene_position = self.mapToScene(current_position)
                self.drawing_rect.setRect(QRectF(self.origin, current_scene_position))


        scene_rect = self.sceneRect()
        self.setSceneRect(scene_rect)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if event.button() == Qt.MouseButton.RightButton:
            if self.is_drawing and self.origin is not None:
                self.is_drawing = False
                release_position = event.pos()
                release_scene_position = self.mapToScene(release_position)
                self.drawing_rect.setRect(QRectF(self.origin, release_scene_position))
                self.showRectCoordinates(self.drawing_rect)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if event.button() == Qt.MouseButton.RightButton:
            if not self.is_drawing:
                click_position = event.pos()
                scene_position = self.mapToScene(click_position)
                self.origin = scene_position
                self.is_drawing = True

                self.drawing_rect = QGraphicsRectItem(QRectF(self.origin, self.origin))
                self.scene().addItem(self.drawing_rect)

    def showRectCoordinates(self, rect_item):
        rect_top_left = rect_item.rect().topLeft()
        rect_bottom_right = rect_item.rect().bottomRight()
        text_item_top_left = QGraphicsTextItem(f"({int(rect_top_left.x())}, {int(rect_top_left.y())})")
        text_item_top_left.setFont(QFont('Arial', 10))
        text_item_top_left.setDefaultTextColor(Qt.GlobalColor.red)
        text_item_top_left.setPos(rect_top_left.x() + 5, rect_top_left.y() - 20)
        self.scene().addItem(text_item_top_left)

        text_item_bottom_right = QGraphicsTextItem(f"({int(rect_bottom_right.x())}, {int(rect_bottom_right.y())})")
        text_item_bottom_right.setFont(QFont('Arial', 10))
        text_item_bottom_right.setDefaultTextColor(Qt.GlobalColor.red)
        text_item_bottom_right.setPos(rect_bottom_right.x() - 50, rect_bottom_right.y() + 5)
        self.scene().addItem(text_item_bottom_right)
    
        rect_key = id(rect_item)
        self.coordinate_text_items[rect_key] = [text_item_top_left, text_item_bottom_right]

    def removeCoordinateTextItems(self, text_items):

        for text_item in text_items:
            self.scene().removeItem(text_item)


        text_items.clear()
    def addTextItem(self, text,
                    bg_path='./bgs/letter.png',
                    font_path="./fonts/hand.ttf",font_size=12, 
                    font_color='black',
                    font_weight=600,
                    x=100,y=100,
                    font_spacing=0, line_spacing=1.2, 
                    rect_width=500, rect_height=50):

        self.scene().clear()

        pixmap = QPixmap(bg_path)
        item = QGraphicsPixmapItem(pixmap)
        self.scene().addItem(item)
        self.scene().setSceneRect(0, 0, 5000, 5000)
  
        text_item = QGraphicsTextItem()
        text_item.setPos(x, y)

        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family,font_size)
        text_item.setFont(font)
 
        html_text = f"<div style='font-weight: {font_weight};color:{font_color};font-size:{font_size}pt; line-height:{line_spacing * 100}%; letter-spacing:{font_spacing}em;'>{text}</div>"
        text_item.setHtml(html_text)
    
        text_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        text_item.setTextWidth(rect_width)
     
        self.scene().addItem(text_item)
    
    def exportSceneToImage(self):
        
        scene_rect = self.sceneRect()
  
        content_rect = self.scene().itemsBoundingRect()
 
        image_size = content_rect.size().toSize()
     
        file_name, _ = QInputDialog.getText(self, 'Export pictures', 'Enter file name', text='img_1.png')
        if not file_name:
            return
        image = QImage(image_size, QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(Qt.GlobalColor.transparent)  
        painter = QPainter(image)
 
        self.scene().render(painter, QRectF(image.rect()), content_rect)
     
        painter.end()
       
        image.save(file_name)
        QMessageBox.information(self, 'hint', ' The picture has been saved in the current directory!', QMessageBox.StandardButton.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = HandFontWindow()
    sys.exit(app.exec())