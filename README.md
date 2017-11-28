used example_aruco_calibrate_camera_charuco and example_aruco_create_board_charuco to generate board + calibration

commands:

bin/example_aruco_calibrate_camera_charuco -d=0 -h=8 -w=6 -m=10 -ml=.0023 -si=true -sl=.0033 ~/calibration.xml

bin/example_aruco_create_board_charuco --bb=1 -d=0 -h=8 -w=6 -m=10 -ml=70 -si=true -sl=100 ~/board.png

printed on 8.5x11 at 130%, measured to be 33 mm square size and 23 mm marker size
