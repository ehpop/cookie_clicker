file_location = 'settings/settings.txt'


def read_settings():
    settings = {}
    try:
        with open(file_location, 'r') as file:
            file_content = file.read()

        lines = file_content.split('\n')
        for line in lines:
            values_in_line = line.split(':')
            if len(values_in_line) > 1:
                settings.update({values_in_line[0]: values_in_line[1]})

    except FileNotFoundError:
        pass

    return settings


def save_setting(settings: {}):
    with open(file_location, 'w') as file:
        for key in settings.keys():
            file.write(str(key) + ':' + str(settings[key]) + '\n')


def test_save():
    settings = read_settings()
    save_setting(settings)


if __name__ == '__main__':
    test_save()
