"""
This example script will NOT work if you run it directly; it is meant to be used as a reference
in case you'd like to implement something similar.

This script is used for CS70 at UC Berkeley to automatically post
homework, discussion, and note threads. All of these threads are tracked in a locked index post,
which is continually updated by this script as well.

Homework templates are also posted with each homework, by uploading a zip file to Overleaf
and prompting the user to finalize the new Overleaf project.
This Overleaf view link is included in a separate post for students.

Usage:
    post_threads.py hw <num>
    post_threads.py dis <num> [--summer]
    post_threads.py note <num>
    post_threads.py init-index

Requirements:
    config file with:
        course_id: id of course to target
        index_thread_num: id of index thread for homeworks/discussions
    environment variables:
        ED_API_KEY: ed api key
"""

import json
import os
from dataclasses import dataclass
from typing import Optional

from edapi import EdAPI
from edapi.constants import ThreadType
from edapi.utils import new_document, parse_content
from PIL import Image

OVERLEAF_UPLOAD_URL = "https://www.overleaf.com/docs?snip_uri="
ANSI_BLUE = lambda text: f"\u001b[34m{text}\u001b[0m"


@dataclass
class Config:
    """Configuration for posting Ed threads."""

    course_id: int
    index_thread_num: Optional[int]

    def copy(self) -> "Config":
        """Make a copy of the current configuration."""
        return Config(course_id=self.course_id, index_thread_num=self.index_thread_num)

    @staticmethod
    def from_json(obj: dict) -> "Config":
        """Convert a JSON object (dict) into a Config dataclass."""
        assert "course_id" in obj, "config JSON must contain 'course_id' value"

        index_thread_num = obj.get("index_thread_num", None)
        if index_thread_num is not None:
            index_thread_num = int(index_thread_num)

        return Config(
            course_id=int(obj["course_id"]),
            index_thread_num=index_thread_num,
        )

    def as_json(self) -> dict:
        """Convert this dataclass into a dict to write to a JSON file."""
        return {
            "course_id": self.course_id,
            "index_thread_num": self.index_thread_num,
        }


# ========== File path helpers ==========

HOMEWORK_IMAGE_EXTENSION = ".png"


def get_hw_folder(hw_num: str):
    """Compute the base path for homework files."""
    return f"../rendered/hw{hw_num}/"


def get_hw_template_zip(hw_num: str):
    """Compute the path to the homework template zip file."""
    return f"../rendered/hw{hw_num}/raw/hw{hw_num}-template.zip"


# ========== Ed post helpers ==========


def post_hw(ed: EdAPI, config: Config, hw_num: str):
    """
    Post homework question threads and update the homework/discussion index.
    """
    assert config.index_thread_num is not None, "Index thread number must be provided."

    summary = []
    hw_num_fmt = str(int(hw_num))
    base_path = get_hw_folder(hw_num)
    # retrieve all images from the rendered directory
    hw_imgs = [
        f
        for f in os.listdir(base_path)
        if os.path.isfile(os.path.join(base_path, f))
        and f.endswith(HOMEWORK_IMAGE_EXTENSION)
    ]
    # sort images by problem number (names are of the format "hwXX-imgXX.png")
    hw_imgs.sort(key=lambda x: int(x.split(".")[0].split("-")[1][3:]), reverse=True)
    num_imgs = len(hw_imgs)

    for hw_idx, hw_img in enumerate(hw_imgs, 1):
        with open(base_path + hw_img, "rb") as f:
            curr_img = f.read()

        # upload image to ed
        img_url = ed.upload_file(hw_img, curr_img, "image/png")
        print(f"[{hw_idx}/{num_imgs}] Uploaded {hw_img}: {img_url}")

        # get image dimensions for display
        img = Image.open(base_path + hw_img)
        img_width, img_height = img.size

        # hw_img has format hw<hw #>-img<problem #>.png
        problem_num = hw_img.split(".")[0][-1]

        # create post body
        problem_soup, document = new_document()
        problem_figure = problem_soup.new_tag("figure")
        problem_image = problem_soup.new_tag(
            "image", src=img_url, width=img_width, height=img_height
        )
        problem_figure.append(problem_image)
        document.append(problem_figure)

        result = ed.post_thread(
            config.course_id,
            {
                "type": ThreadType.POST,
                "title": f"Homework {hw_num_fmt} Problem {problem_num} Thread",
                "category": "Homework",
                "subcategory": f"HW{hw_num_fmt}",
                "subsubcategory": "",
                "content": str(document),
                "is_pinned": False,
                "is_private": False,
                "is_anonymous": False,
                "is_megathread": True,
                "anonymous_comments": True,
            },
        )
        print(
            f"[{hw_idx}/{num_imgs}] Posted thread for HW{hw_num_fmt} Q{problem_num}:"
            f" #{result['number']}"
        )
        summary.append(f"Question {problem_num} (#{result['number']})")

    summary.reverse()

    # LaTeX Template
    with open(get_hw_template_zip(hw_num), "rb") as f:
        template_zip = f.read()
    template_url = ed.upload_file(
        f"hw{hw_num}-template.zip", template_zip, "multipart/form-data"
    )

    template_creation_url = OVERLEAF_UPLOAD_URL + template_url
    print(f"\nGo to:\n\t{ANSI_BLUE(template_creation_url)}")
    student_link = input("Enter shareable Overleaf link: ")

    # create post body
    post_soup, document = new_document()
    link_paragraph = post_soup.new_tag("paragraph")
    link_paragraph.string = "Overleaf link: "
    link_link = post_soup.new_tag("link", href=student_link)
    link_link.string = student_link
    link_paragraph.append(link_link)
    document.append(link_paragraph)

    zip_paragraph = post_soup.new_tag("paragraph")
    zip_paragraph.string = "Source files:"
    document.append(zip_paragraph)
    zip_link = post_soup.new_tag(
        "file", url=template_url, filename=f"hw{hw_num}-template.zip"
    )
    zip_paragraph.append(zip_link)
    document.append(zip_link)

    template_result = ed.post_thread(
        config.course_id,
        {
            "type": ThreadType.POST,
            "title": f"LaTeX Template for HW {hw_num_fmt}",
            "category": "Homework",
            "subcategory": f"HW{hw_num_fmt}",
            "subsubcategory": "",
            "content": str(document),
            "is_pinned": False,
            "is_private": False,
            "is_anonymous": False,
            "is_megathread": True,
            "anonymous_comments": True,
        },
    )
    print(f"Posted template for HW{hw_num_fmt}: #{template_result['number']}")
    summary.append(f"LaTeX Template (#{template_result['number']})")

    # Update summary

    course_id = config.course_id
    hw_dis_post_num = config.index_thread_num
    hw_dis_post = ed.get_course_thread(course_id, hw_dis_post_num)
    hw_dis_post_id = hw_dis_post["id"]

    last_content = hw_dis_post["content"]
    soup, document = parse_content(last_content)
    # hw list is first, dis list is second
    hw_list = document.find_all("list", recursive=False)[0]

    hw_summary = soup.new_tag("list-item")
    hw_summary_heading = soup.new_tag("paragraph")
    hw_summary_heading.string = f"Homework {hw_num_fmt}"
    hw_summary.append(hw_summary_heading)

    question_list = soup.new_tag("list")
    question_list.attrs["style"] = "bullet"
    for question_content in summary:
        question_item = soup.new_tag("list-item")
        question_paragraph = soup.new_tag("paragraph")
        question_paragraph.append(question_content)
        question_item.append(question_paragraph)
        question_list.append(question_item)
    hw_summary.append(question_list)

    hw_list.append(hw_summary)

    ed.edit_thread(hw_dis_post_id, {"content": str(document)})
    print("Updated Index Thread")


def post_dis(ed: EdAPI, config: Config, dis_num: str, is_summer: bool):
    """
    Post discussion thread and update the homework/discussion index.
    """
    assert config.index_thread_num is not None, "Index thread number must be provided."

    dis_num_fmt = int(dis_num)

    # create post body
    discussion_soup, document = new_document()
    dis_a_paragraph = discussion_soup.new_tag("paragraph")
    dis_a_paragraph.string = f"Discussion {dis_num_fmt}a: "
    dis_a_text = f"https://www.eecs70.org/assets/pdf/dis{dis_num}a.pdf"
    dis_a_link = discussion_soup.new_tag("link", href=dis_a_text)
    dis_a_link.string = dis_a_text
    dis_a_paragraph.append(dis_a_link)
    document.append(dis_a_paragraph)

    dis_b_paragraph = discussion_soup.new_tag("paragraph")
    dis_b_paragraph.string = f"Discussion {dis_num_fmt}b: "
    dis_b_text = f"https://www.eecs70.org/assets/pdf/dis{dis_num}b.pdf"
    dis_b_link = discussion_soup.new_tag("link", href=dis_b_text)
    dis_b_link.string = dis_b_text
    dis_b_paragraph.append(dis_b_link)
    document.append(dis_b_paragraph)

    if is_summer:
        dis_c_paragraph = discussion_soup.new_tag("paragraph")
        dis_c_paragraph.string = f"Discussion {dis_num_fmt}c: "
        dis_c_text = f"https://www.eecs70.org/assets/pdf/dis{dis_num}c.pdf"
        dis_c_link = discussion_soup.new_tag("link", href=dis_c_text)
        dis_c_link.string = dis_c_text
        dis_c_paragraph.append(dis_c_link)
        document.append(dis_c_paragraph)

        dis_d_paragraph = discussion_soup.new_tag("paragraph")
        dis_d_paragraph.string = f"Discussion {dis_num_fmt}d: "
        dis_d_text = f"https://www.eecs70.org/assets/pdf/dis{dis_num}d.pdf"
        dis_d_link = discussion_soup.new_tag("link", href=dis_d_text)
        dis_d_link.string = dis_d_text
        dis_d_paragraph.append(dis_d_link)
        document.append(dis_d_paragraph)

    # post thread
    dis_post_result = ed.post_thread(
        config.course_id,
        {
            "type": ThreadType.POST,
            "title": f"Discussion {dis_num_fmt} Thread",
            "category": "Discussion",
            "subcategory": f"DIS{dis_num_fmt}",
            "subsubcategory": "",
            "content": str(document),
            "is_pinned": False,
            "is_private": False,
            "is_anonymous": False,
            "is_megathread": True,
            "anonymous_comments": True,
        },
    )
    if is_summer:
        print(f"Posted discussion {dis_num_fmt}a/b/c/d: #{dis_post_result['number']}")
    else:
        print(f"Posted discussion {dis_num_fmt}a/b: #{dis_post_result['number']}")

    # update summary
    hw_dis_post_num = config.index_thread_num
    hw_dis_post = ed.get_course_thread(config.course_id, hw_dis_post_num)
    hw_dis_post_id = hw_dis_post["id"]

    last_content = hw_dis_post["content"]
    soup, document = parse_content(last_content)
    # hw list is first, dis list is second
    dis_list = document.find_all("list", recursive=False)[1]

    dis_item = soup.new_tag("list-item")
    dis_item_paragraph = soup.new_tag("paragraph")
    if is_summer:
        dis_item_paragraph.string = (
            f"Discussion {dis_num_fmt}a, {dis_num_fmt}b, {dis_num_fmt}c, {dis_num_fmt}d"
            f" (#{dis_post_result['number']})"
        )
    else:
        dis_item_paragraph.string = (
            f"Discussion {dis_num_fmt}a, {dis_num_fmt}b (#{dis_post_result['number']})"
        )
    dis_item.append(dis_item_paragraph)
    dis_list.append(dis_item)

    ed.edit_thread(hw_dis_post_id, {"content": str(document)})
    print("Updated Index Thread")


def post_note(ed: EdAPI, config: Config, note_num: str):
    """
    Post note thread and update the homework/discussion index.
    """
    assert config.index_thread_num is not None, "Index thread number must be provided."

    # create post body
    note_soup, document = new_document()
    note_link_paragraph = note_soup.new_tag("paragraph")
    note_link_paragraph.string = f"Note {note_num}: "

    link_text = f"https://www.eecs70.org/assets/pdf/notes/n{note_num}.pdf"
    note_link = note_soup.new_tag("link", href=link_text)
    note_link.string = link_text

    note_link_paragraph.append(note_link)
    document.append(note_link_paragraph)

    # second paragraph
    note_paragraph = note_soup.new_tag("paragraph")
    note_paragraph.string = (
        f"Please ask any questions you have about note {note_num} here."
    )
    document.append(note_paragraph)

    # post thread
    note_post_result = ed.post_thread(
        config.course_id,
        {
            "type": ThreadType.POST,
            "title": f"Note {note_num} Thread",
            "category": "Notes",
            "subcategory": "",
            "subsubcategory": "",
            "content": str(document),
            "is_pinned": False,
            "is_private": False,
            "is_anonymous": False,
            "is_megathread": True,
            "anonymous_comments": True,
        },
    )
    print(f"Posted note {note_num} thread: #{note_post_result['number']}")

    # update summary
    hw_dis_post_num = config.index_thread_num
    hw_dis_post = ed.get_course_thread(config.course_id, hw_dis_post_num)
    hw_dis_post_id = hw_dis_post["id"]

    last_content = hw_dis_post["content"]
    soup, document = parse_content(last_content)
    # hw list is first, dis list is second, note list is third
    note_list = document.find_all("list", recursive=False)[2]

    note_item = soup.new_tag("list-item")
    note_item_paragraph = soup.new_tag("paragraph")
    note_item_paragraph.string = f"Note {note_num} (#{note_post_result['number']})"
    note_item.append(note_item_paragraph)
    note_list.append(note_item)

    ed.edit_thread(hw_dis_post_id, {"content": str(document)})
    print("Updated Index Thread")


def init_index(ed: EdAPI, config: Config):
    """Initialize the index post, updating the config file with the post number."""
    course_id = config.course_id

    index_soup, document = new_document()

    # Homework section
    homework_title = index_soup.new_tag("heading", level=2)
    homework_title.string = "Homeworks"
    homework_list = index_soup.new_tag("list", style="bullet")
    document.extend([homework_title, homework_list])

    # Discussion section
    discussion_title = index_soup.new_tag("heading", level=2)
    discussion_title.string = "Discussions"
    discussion_list = index_soup.new_tag("list", style="bullet")
    document.extend([discussion_title, discussion_list])

    # Note section
    note_title = index_soup.new_tag("heading", level=2)
    note_title.string = "Notes"
    note_list = index_soup.new_tag("list", style="bullet")
    document.extend([note_title, note_list])

    # create and lock the index thread
    index_thread = ed.post_thread(
        course_id,
        {
            "type": ThreadType.POST,
            "title": "Homework/Discussion/Note Thread",
            "category": "Logistics",
            "subcategory": "",
            "subsubcategory": "",
            "content": str(document),
            "is_pinned": True,
            "is_private": False,
            "is_anonymous": False,
            "is_megathread": True,
            "anonymous_comments": True,
        },
    )
    ed.lock_thread(index_thread["id"])

    index_thread_num = index_thread["number"]
    print(f"Created index thread: #{index_thread_num}")

    # update config json file
    new_config = Config(course_id=config.course_id, index_thread_num=index_thread_num)

    with open("./config.json", "w", encoding="utf-8") as config_file:
        json.dump(new_config.as_json(), config_file, indent=2)
        config_file.write("\n")  # add newline at end of file

    print("Updated config file")


def main(args):
    """
    Main method, delegating to other functions to post threads.
    """

    # read configuration
    with open("./config.json", "r", encoding="utf-8") as config_file:
        config_json = json.load(config_file)
        config = Config.from_json(config_json)

    ed = EdAPI()
    ed.login()

    if args.type == "hw":
        post_hw(ed, config, args.num)
    elif args.type == "dis":
        post_dis(ed, config, args.num, args.summer)
    elif args.type == "note":
        post_note(ed, config, args.num)
    elif args.type == "init-index":
        init_index(ed, config)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="type")
    subparsers.required = True

    hw_parser = subparsers.add_parser("hw")
    dis_parser = subparsers.add_parser("dis")
    note_parser = subparsers.add_parser("note")
    init_parser = subparsers.add_parser("init-index")

    # add "num" argument to hw/dis/note parsers
    for p in (hw_parser, dis_parser, note_parser):
        p.add_argument("num", help="HW/discussion/note number")

    # optional summer flag for discussions
    dis_parser.add_argument(
        "--summer",
        action="store_true",
        help="Flag for summer discussions; creates 4 discussion threads instead of 2",
    )

    arguments = parser.parse_args()
    main(arguments)
