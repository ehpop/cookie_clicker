import PySimpleGUI
import PySimpleGUI as sG
import pyautogui
import auto_clicker as ac


control_panel_run = [
    [sG.Button("RUN", size=(10, 10), button_color="#75FA61", mouseover_colors="#25D900"), sG.Button("STOP", size=(10, 10), button_color="#EB3324", mouseover_colors="#F00000")],
    [sG.Button("CANCEL", size=(10, 10), button_color="#808080", mouseover_colors="#5E5E5E"), sG.Button("SETTINGS", size=(10, 10), button_color="#808080", mouseover_colors="#5E5E5E")]
]
control_panel_set = [
    [sG.Button("CANCEL", size=(10, 10), button_color="#808080", mouseover_colors="#5E5E5E"), sG.Button("SETTINGS", size=(10, 10), button_color="#808080", mouseover_colors="#5E5E5E")]
]

logger_column = [
    [sG.Text("LOGGER (current session)", size=(40, 1), key="-Logger-")],
    [sG.Multiline(size=(200, 100), key='-LOG-', disabled=True, default_text="---LOGGER INFO---\n", autoscroll=True)]
]

layout = [
    [
        sG.Column(control_panel_run, background_color="#2B2B2B"),
        PySimpleGUI.VSeparator(),
        sG.Column(logger_column, background_color="#2B2B2B")
    ]
]

window = sG.Window("Auto Clicker", layout, resizable=True, size=(720, 480), background_color="#1F1F1F", icon='res/logo.ico')


def run_clicker_loop(settings: {}):
    pyautogui.moveTo(100, 100)

    cookies_clicked_in_loop = 0
    while True:
        res = ac.run_clicker_single(cookies_clicked_in_loop,
                                                passive=not settings['column-upgrades'] == 'False',
                                                active=not settings['horizontal-upgrades'] == 'False',
                                                golden_cookie=not settings['golden-cookie-search'] == 'False',
                                                hide_boards=not settings['clear-board'] == 'False',
                                                close_notification=not settings['clear-notification'] == 'False',
                                                upgrades_from_top=not settings['direction-upgrades'] == 'From Bottom',
                                                log_frequency=int(settings['log-frequency']))

        if res == -1:
            return res
        elif res == -2:
            window["-LOG-"].update('---GOLDEN COOKIE FOUND---\n', append=True)
        else:
            cookies_clicked_in_loop += res

        if not cookies_clicked_in_loop % int(settings['log-frequency']):
            msg = ac.write_to_log(amount_of_clicks=int(settings['log-frequency']), write_to_file=False)
            window["-LOG-"].update(msg, append=True)
            window.refresh()


def main():

    settings = {'column-upgrades': 'False', 'direction-upgrades': 'From Bottom', 'horizontal-upgrades': 'False', 'clear-notification': 'True', 'clear-board': 'True', 'golden-cookie-search': 'True', 'log-frequency': '100'}

    while True:
        event, values = window.read()


        if event == "SETTINGS":
            layout_buttons = [
                sG.Button("CANCEL", size=(10, 10), button_color="#808080", mouseover_colors="#5E5E5E"),
                sG.Button("SAVE", size=(10, 10), button_color="#75FA61", mouseover_colors="#25D900")
            ]
            layout_inputs = [
                [sG.Text('Auto Upgrade Vertical', size=(20, 1), font='Lucida', justification='left')],
                [sG.Combo(['True', 'False'], default_value=settings['column-upgrades'], key='column-upgrades'), sG.Combo(['From Bottom', 'From Top'], default_value=settings['direction-upgrades'], key='direction-upgrades')],
                [sG.Text('Auto Upgrade Horizontal', size=(20, 1), font='Lucida', justification='left')],
                [sG.Combo(['True', 'False'], default_value=settings['horizontal-upgrades'], key='horizontal-upgrades')],
                [sG.Text('Clear Notifications', size=(20, 1), font='Lucida', justification='left')],
                [sG.Combo(['True', 'False'], default_value=settings['clear-notification'], key='clear-notification')],
                [sG.Text('Clear Board', size=(20, 1), font='Lucida', justification='left')],
                [sG.Combo(['True', 'False'], default_value=settings['clear-board'], key='clear-board')],
                [sG.Text('Search For Golden Cookie', size=(25, 1), font='Lucida', justification='left')],
                [sG.Combo(['True', 'False'], default_value=settings['golden-cookie-search'], key='golden-cookie-search')],
                [sG.Text('Log Info Per Clicks', size=(25, 1), font='Lucida', justification='left')],
                [sG.Combo(['100', '1000', '10_000', '100_000'], default_value=settings['log-frequency'], key='log-frequency')],
            ]
            layout_settings = [
                layout_inputs,
                layout_buttons

            ]
            settings_window = sG.Window("Settings", layout=layout_settings, resizable=False, size=(240, 480))
            while True:
                event_s, values_s = settings_window.read()

                if event_s == sG.WIN_CLOSED or event_s == "CANCEL":
                    break

                if event_s == "SAVE":
                    settings = values_s
                    break

            settings_window.close()

        if event == "CANCEL" or event == sG.WIN_CLOSED:
            break

        if event == "RUN":
            msg = ac.write_to_log(amount_of_clicks=100, add_separator=True, write_to_file=False)
            window["-LOG-"].update(msg, append=True)
            window.refresh()

            result = run_clicker_loop(settings)

            if result == -1:
                window["-LOG-"].update('Clicker stopped by moving mouse on negative x\n', append=True)

    window.close()


if __name__ == '__main__':
    main()
