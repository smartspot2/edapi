from edapi import EdAPI

ed = EdAPI()
ed.login()

lesson_info = ed.list_lessons()

print(f"Lesson 1: {lesson_info['lessons'][0]['title']}")