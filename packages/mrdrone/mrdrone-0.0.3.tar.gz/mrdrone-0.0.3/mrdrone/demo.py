import time
import cv2
from pynput import keyboard


def fly_tello():
    from mrdrone import tello  # 引入tello包
    drone = tello.Tello()  # 初始化
    print(drone.get_battery())
    drone.streamon()  # 打开视频流并显示视频
    # drone.identify_animal()
    drone.takeoff()  # 起飞
    # drone.forward(100)  # 前进100cm
    drone.cw(360)  # 旋转90°
    drone.stream_service_on()
    drone.identify_animal()
    input()
    drone.ccw(360)
    # drone.flip('l')  # 左翻滚
    drone.land()  # 降落
    drone.streamoff()


def fly_folk():
    from mrdrone import folk  # 引入folk包，第一次使用时需要运行FolkTools.exe文件进行激活
    uav = folk.Folk()  # 初始化
    uav.stream_on()  # 打开视频流
    uav.stream_show()  # 显示视频流
    uav.takeoff()  # 起飞
    # uav.forward(100)  # 前进100cm
    # uav.turn_right(90)  # 旋转90°
    # uav.flip_left()  # 左翻滚
    uav.up(50)  # 上升50cm
    uav.land()  # 降落


def on_press(key):
    '按下按键时执行。'
    try:
        # print('alphanumeric key {0} pressed'.format(key.char))
        getKeyboardInput()
    except AttributeError:
        print('special key {0} pressed'.format(key))
    # 通过属性判断按键类型。


def on_release(key):
    '松开按键时执行。'
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        print('esc')
        # Stop listener
        return False


# Collect events until released
def getKeyboardInput(speed=10):
    lr, fb, ud, yv = 0, 0, 0, 0

    if keyboard.KeyCode.from_char('t'):
        drone.takeoff()
    elif keyboard.KeyCode.from_char('l'):
        drone.land()
    if keyboard.KeyCode.from_char('a'):
        lr = -speed
    elif keyboard.KeyCode.from_char('d'):
        lr = speed
    if keyboard.KeyCode.from_char('w'):
        fb = speed
    elif keyboard.KeyCode.from_char('s'):
        fb = -speed
    if keyboard.Key.down:
        ud = -speed
    elif keyboard.Key.up:
        ud = speed
    if keyboard.Key.left:
        yv = -speed
    elif keyboard.Key.right:
        yv = speed
    # 横滚 (-100~100)ad
    # 俯仰 (-100~100)ws
    # 油门 (-100~100)up down
    # 偏航 (-100~100)left right
    drone.rc_control(lr, fb, ud, yv)


if __name__ == '__main__':
    # from mrdrone import tello  # 引入tello包
    # drone = tello.Tello()
    # drone.takeoff()
    # with keyboard.Listener(on_press=on_press) as listener:
    #     listener.join()
    # print('res')

    fly_tello()
    # fly_folk()
