#!/usr/bin/env micropython
from robot import Robot
from server import Server

robot = Robot()
power = 1
angle = 1

robot.beep()

connection_enabled = robot.select_connection_mode()

if connection_enabled:
    server = Server("10.42.0.3")
    server.start_server()
    server.wait_for_connection()

while True:
    if connection_enabled:
        robot.print("Press to take picture")
        server.send_data_to_client("READY")
        (direction, power, angle) = server.wait_for_data()
    else:
        (power, angle) = robot.wait_for_power_select(power, angle)
        direction = 0

    robot.calibrate_swing()
    robot.ready_swing(angle)

    robot.calibrate_dir()
    robot.set_direction(direction)

    robot.wait_for_button()
    robot.shoot(power)

    robot.wait_for_button()
