from . import constants as const


class DayOfWeekConverter:
    regex = '({}|{}|{}|{}|{}|{}|{}|{}|{})'.format(const.MONDAY, const.TUESDAY, const.WEDNESDAY,
                                                  const.THURSDAY, const.FRIDAY, const.SATURDAY,
                                                  const.SUNDAY, const.WEEKDAY, const.WEEKEND)

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


class TimezoneConverter:
    regex = '{}|{}|{}'.format(const.America_Chicago, const.America_Denver, const.America_Phoenix)

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
