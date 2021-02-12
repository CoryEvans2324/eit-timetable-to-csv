import os
import re
import bs4
import time
import requests

from to_calendar import convert_and_save

course_name_regex = re.compile(r'Timetable for:\s+([A-z ]+)')
course_code_regex = re.compile(r'MODULE CODE:(IT[A-Z]+\d\.\d+)/')
week_regex = re.compile(r'WEEK NUMBER: ([\d\- ,]+)')

class Course:
    def __init__(self, info_tables, calendar_tables) -> None:
        self.data = self.parse(info_tables, calendar_tables)

    def to_dict(self):
        to_return = {}
        # bit slow but bruteforce is always best
        for week_num in range(0, 53):
            for week_str, data in self.data['weeks'].items():
                if Course.week_num_is_in_week_info_str_range(week_num, week_str):
                    # to_return[f'2021-W{week_num}-'] = data
                    for week_day, class_data in data.items():
                        to_return[f'W{week_num}-{week_day}'] = class_data

        return to_return

    @staticmethod
    def week_num_is_in_week_info_str_range(n, week_info_str):
        weeks = week_info_str.split(', ')
        for w in weeks:
            if '-' in w:
                min_w, max_w = [int(x) for x in w.split('-')]
            else:
                min_w = max_w = int(w)

            if min_w <= n <= max_w:
                return True

        return False

    def parse(self, info_tables, calendar_tables):
        data = {'weeks': {}}
        course_code = ''
        course_name = ''
        for info, calendar in zip(info_tables, calendar_tables):
            info_data = self.parse_info_table(info)
            course_code = info_data['course_code']
            course_name = info_data['course_name']

            calendar_data = self.parse_calendar_table(course_code, calendar)

            data['weeks'][info_data['weeks']] = calendar_data

        data['course_code'] = course_code
        data['course_name'] = course_name
        return data

    def parse_info_table(self, table: bs4.element.Tag):
        text = table.text
        m = re.search(course_name_regex, text)
        course_name = m.group(1).strip()

        m = re.search(course_code_regex, text)
        course_code = m.group(1).strip()
        self.course_code = course_code

        m = re.search(week_regex, text)
        week_info = m.group(1)

        return {
            'course_name': course_name,
            'course_code': course_code,
            'weeks': week_info
        }

    def parse_calendar_table(self, course_code, table: bs4.element.Tag) -> dict:
        data = {}
        calender_table_rows = table.find_all('tr', recursive=False)[1:]
        for row in calender_table_rows:
            day, row_data = self.parse_calendar_row(course_code, row)
            data[day] = row_data

        return data

    def parse_calendar_row(self, course_code, row: bs4.element.Tag):
        day = row.td.text
        start_hour = 7
        row_data = []
        for td in row.find_all('td', recursive=False)[1:]:
            children_tags = [
                tag
                for tag in td.children
                if isinstance(tag, bs4.element.Tag)
            ]


            if len(children_tags) == 0:
                start_hour += 0.5
                continue

            assert len(children_tags) == 3

            classname = children_tags[0].tr.td.text
            lecturer, classroom = [
                tag.text
                for tag in children_tags[1].tr.find_all('td')
            ]

            duration = int(td.attrs['colspan']) * 0.5

            data = {
                'start': start_hour,
                'end': start_hour + duration,
                'lecturer': lecturer,
                'classroom': classroom,
                'classname': classname,
                'classcode': course_code
            }

            start_hour += duration

            row_data.append(data)

        return day, row_data


def main():
    # Download all the courses
    urls_file_path = os.path.join(
        os.getcwd(),
        'urls.txt'
    )
    if not os.path.exists(urls_file_path):
        with open(urls_file_path, 'w') as f:
            f.write('enter timetable urls (http://mytimetable1.eit.ac.nz/Home/Timetable...) on each line. Make sure to remove this line')

        print('Edit the urls.txt file.')
        return

    with open(urls_file_path) as f:
        urls = f.read().strip().splitlines()

    course_html_page_texts = []
    for url in urls:
        resp = requests.get(url)
        course_html_page_texts.append(
            resp.text
        )

        print(f'[*] Got {url}')
        print('[*] Waiting 1 second before next request.')
        time.sleep(1)

    courses = []
    for html_text in course_html_page_texts:
        soup = bs4.BeautifulSoup(html_text, 'html.parser')

        tables = soup.body.find_all('table', recursive=False)[:-1]

        assert len(tables) % 3 == 0

        info_tables = []
        calendar_tables = []

        for i in range(0, len(tables), 3):
            info_tables.append(tables[i])
            calendar_tables.append(tables[i+1])

        obj = Course(info_tables, calendar_tables)
        courses.append(obj)

    print('[*] Saving all courses into a csv file.')
    convert_and_save([
        obj.to_dict()
        for obj in courses
    ])

    print('[*] DONE')

if __name__ == '__main__':
    main()
