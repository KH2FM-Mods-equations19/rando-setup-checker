from PySide6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QFileDialog, QLabel, QVBoxLayout, QTextEdit

import validation
from randoconfig import PcRandoConfiguration, path_or_none


class PcConfigurationDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('PC Configuration')
        self.setMinimumWidth(800)

        grid = QGridLayout()

        mods_manager_bridge_path_field = QLineEdit()
        mods_manager_bridge_path_field.setToolTip('Extracts and patches KH2 game data. Also known as build_from_mm.')
        self.mods_manager_bridge_path_path_field = mods_manager_bridge_path_field
        mods_manager_bridge_path_button = QPushButton('Choose')
        mods_manager_bridge_path_button.clicked.connect(self._choose_mods_manager_bridge_path)
        grid.addWidget(QLabel('Mods Manager Bridge (build_from_mm) Location'), 0, 0, 1, 2)
        grid.addWidget(mods_manager_bridge_path_field, 1, 0)
        grid.addWidget(mods_manager_bridge_path_button, 1, 1)

        validate = QPushButton('Check Configuration')
        validate.clicked.connect(self._validate_clicked)

        validation_result = QTextEdit()
        validation_result.setReadOnly(True)
        self.validation_result = validation_result

        box = QVBoxLayout()
        box.addLayout(grid)
        box.addWidget(validate)
        box.addWidget(validation_result)
        self.setLayout(box)

    def _choose_mods_manager_bridge_path(self):
        output = QFileDialog.getExistingDirectory()
        if output is not None and output != '':
            self.mods_manager_bridge_path_path_field.setText(output)

    def _validate_clicked(self):
        mods_manager_bridge_path = path_or_none(self.mods_manager_bridge_path_path_field.text())
        rando_configuration = PcRandoConfiguration.read_from_mods_manager_bridge(mods_manager_bridge_path)
        all_results = rando_configuration.validate_all()
        validation.show_validation_result(self.validation_result, all_results)
