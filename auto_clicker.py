import pyautogui
import numpy as np
import time
import datetime as dt

cookie_position = (300, 503)

upgrade_line = (1676, 327, 1686, 900)
upgrade_line_scrolled = (1676, 270, 1686, 1000)

notification_check_pos = (1121, 1018)
notification_check_color = [10, 10, 10]

golden_cookie_scan = (0, 225, 1567, 1028)
upper_upgrade_right_corner = (1661, 197)

golden_cookie_active_location_1 = (531, 144)
golden_cookie_active_location_2 = (0, 761)

upper_upgrade_ready_color = [169, 130, 64]
golden_cookie_color = [202, 169, 81]
active_upgrade_color_check_1 = [25, 81, 129]
active_upgrade_color_check_2 = [255, 225, 135]

bottom_scroll_position = (1920 - 10, 138)
scroll_amount_per_one_field = -80
scroll_amount = scroll_amount_per_one_field * 10

green_upgrade = ''
upper_color = ''

red = 0
green = 1
blue = 2

hide_display_feature_scan_location = (1481, 432)
hide_display_color = [92, 57, 32]


def scroll_wrap(x, y, scroll_amount):
    if x and y:
        pyautogui.click(x, y)
        pyautogui.click(x, y)

        pyautogui.scroll(scroll_amount)


def log_separator():
    date = f'{dt.date.today()}'
    time = f'{dt.datetime.now().hour}:{dt.datetime.now().minute}'
    return '-' * 45 + '\n' + \
           'Starting new program at: ' + date + ' ' + time + '\n' + \
           '-' * 45 + '\n'


def write_to_log(amount_of_clicks, add_separator=False, wipe_file=False, write_to_file=True):
    amount_of_clicks_prev = 0
    if wipe_file:
        file_mode = 'w'
    else:
        file_mode = 'a'

    try:
        with open('res/cookies_log.txt', 'r') as log_file:
            file_lines = log_file.read().rstrip().split('\n')

            data = file_lines[len(file_lines) - 1].split('->')

            if data and not wipe_file:
                amount_of_clicks_prev = int(data[1])

            log_file.close()

    except FileNotFoundError:
        pass

    if not write_to_file:
        string = ''
        curr_date = dt.datetime.now()
        if add_separator:
            string += log_separator()

        print(amount_of_clicks, amount_of_clicks_prev, amount_of_clicks_prev + amount_of_clicks)

        string += '\tcookies clicked at ' + str(curr_date.year) + '-' + str(curr_date.month) + '-' + str(
            curr_date.day) + ' ' + str(curr_date.hour) + ':' + str(curr_date.minute) + '->' + "{:,}".format(
            amount_of_clicks_prev + amount_of_clicks) + '\n'

        return string

    with open('res/cookies_log.txt', file_mode) as log_file:
        curr_date = dt.datetime.now()
        if add_separator:
            log_file.write(log_separator())

        log_file.write(
            f'\tcookies clicked at {curr_date.year}-{curr_date.month}-{curr_date.day} {curr_date.hour}:{curr_date.minute} -> {amount_of_clicks_prev + amount_of_clicks:_} \n'
        )

        log_file.close()


def get_array_picture(area):
    screen = pyautogui.screenshot()
    area_screenshot = screen.crop(area)
    return np.asarray(area_screenshot)


def get_pixel(pix: ()):
    screen = pyautogui.screenshot()
    px = np.asarray(screen.crop((pix[0], pix[1], pix[0] + 1, pix[1] + 1)))
    px = [px[0][0][0], px[0][0][1], px[0][0][2]]
    return px


def upgrade_passive_income_from_top():
    # upgrade_scan_screen.show()
    # upper_upgrade_scan_screen.show()

    scroll_to_top()

    screen_arr = get_array_picture(upgrade_line)
    column = row = 0
    while column < len(screen_arr[0]):
        row = 0
        while row < len(screen_arr):
            color = screen_arr[row][column]
            if (color == [255, 255, 255]).all():
                (start_width, start_height, *rest) = upgrade_line
                pyautogui.click(start_width + column, start_height + row)
                row -= 64  # we will check that same upgrade again
                screen_arr = get_array_picture(upgrade_line)  # we take another screenshot
            row += 64
        column += 1


def upgrade_passive_income_from_bottom():
    # upgrade_scan_screen.show()
    # upper_upgrade_scan_screen.show()

    scroll_to_bottom()

    screen_arr = get_array_picture(upgrade_line_scrolled)
    column = 0
    row = 729
    while column < len(screen_arr[1]):
        row = 729
        while row > upgrade_line_scrolled[1]:
            color = screen_arr[row][column]
            if (color == [255, 255, 255]).all():
                (start_width, start_height, *rest) = upgrade_line_scrolled
                pyautogui.click(start_width + column, start_height + row)
                row += 64  # we will check that same upgrade again
                screen_arr = get_array_picture(upgrade_line_scrolled)  # we take another screenshot
            row -= 64
        column += 1


def upgrade_click_income():
    scroll_to_top()
    px = get_pixel(upper_upgrade_right_corner)
    x, y = upper_upgrade_right_corner[0], upper_upgrade_right_corner[1]
    while px == upper_upgrade_ready_color:
        pyautogui.click(x, y)
        pyautogui.moveTo(100, 100)
        px = get_pixel(upper_upgrade_right_corner)


def click_cookie(mouse_x, clicks_to_perform=10):
    pyautogui.click(cookie_position[0], cookie_position[1], clicks=clicks_to_perform, interval=0.001)

    if mouse_x > 0:
        return clicks_to_perform
    else:
        return -1


def click_golden_cookie_on_screen():
    golden_cookies = 0

    screen = pyautogui.screenshot()
    array = np.array(screen.crop(golden_cookie_scan))
    for y in range(0, len(array), 10):
        for x in range(0, len(array[0]), 10):
            if golden_cookie_color[red] - 20 <= array[y][x][red] <= golden_cookie_color[red] + 20 \
                    and golden_cookie_color[blue] - 20 <= array[y][x][blue] <= golden_cookie_color[blue] + 20 \
                    and golden_cookie_color[green] - 20 <= array[y][x][green] <= golden_cookie_color[green] + 20:
                pyautogui.click(golden_cookie_scan[0] + x, golden_cookie_scan[1] + y)
                golden_cookies += 1

    return golden_cookies


def is_golden_cookie_active():
    return get_pixel(golden_cookie_active_location_1) == active_upgrade_color_check_1 \
           and get_pixel(golden_cookie_active_location_2) == active_upgrade_color_check_2


def is_notification_up():
    px = get_pixel(notification_check_pos)
    return px[red] < notification_check_color[red] and px[blue] < notification_check_color[blue] and px[green] < \
           notification_check_color[green]


def close_notifications():
    if is_notification_up():
        pyautogui.click(notification_check_pos[0] - 2, notification_check_pos[1] - 2)


def is_any_board_up():
    pyautogui.moveTo(hide_display_feature_scan_location[0]-100, hide_display_feature_scan_location[0]-100)
    px = get_pixel(hide_display_feature_scan_location)
    return px[red] == hide_display_color[red] and px[blue] == hide_display_color[blue] \
           and px[green] == hide_display_color[green]


def hide_board():
    if is_any_board_up():
        pyautogui.click(hide_display_feature_scan_location[0], hide_display_feature_scan_location[1])

    for i in range(10):  # could be while True, but I want to avoid potential infinite clicking
        if not is_any_board_up():
            break

        pyautogui.click(hide_display_feature_scan_location[0], hide_display_feature_scan_location[1])


def run_upgrades(passive, active, golden_cookie, close_notification=True, hide_boards=False, upgrades_from='From Bottom'):
    default_result = 0
    golden_cookie_was_clicked = -2

    if active:
        upgrade_click_income()

    if passive:
        if upgrades_from == 'From Top':
            upgrade_passive_income_from_top()
            print('topped')
        elif upgrades_from == 'From Bottom':
            print('bottomed')
            upgrade_passive_income_from_bottom()

    if close_notification:
        close_notifications()

    if hide_boards:
        hide_board()

    if golden_cookie and not is_golden_cookie_active():
        clicks = click_golden_cookie_on_screen()
        if clicks >= 10:
            return golden_cookie_was_clicked

    return default_result


def scroll_to_bottom():
    scroll_wrap(bottom_scroll_position[0], bottom_scroll_position[1], scroll_amount)
    pyautogui.scroll(abs(scroll_amount_per_one_field))


def scroll_to_top():
    scroll_wrap(bottom_scroll_position[0], bottom_scroll_position[1], 1000)


def run_clicker_single(cookies_clicked, passive=False, active=False, golden_cookie=False, hide_boards=False,
                       close_notification=False, upgrades_from='From Bottom', log_frequency=100):
    result_upgrades = run_upgrades(passive=passive,
                                   active=active,
                                   golden_cookie=not (cookies_clicked % 500) and golden_cookie,
                                   # doing it that way doesn't scan every single time
                                   hide_boards=not (cookies_clicked % 10_000) and hide_boards,
                                   close_notification=not (cookies_clicked % 10_000) and close_notification,
                                   upgrades_from=upgrades_from
                                   )

    if result_upgrades == -2:  # quits loop, -2 is golden cookie signal
        return result_upgrades

    for i in range(10):
        if not cookies_clicked % log_frequency:
            write_to_log(log_frequency, add_separator=False, wipe_file=False, write_to_file=True)

        pos = pyautogui.position()
        res = click_cookie(mouse_x=pos.x, clicks_to_perform=10)

        if res == -1:  # quits loop, -1 is break signal
            return res

        cookies_clicked += res

    return cookies_clicked


def test_main():
    scroll_to_bottom()


if __name__ == '__main__':
    test_main()
