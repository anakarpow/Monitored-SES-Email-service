import dominate
from dominate.tags import *


def format_monitoring_email(success_list, failed_list):

    doc = dominate.document(title="Cost Report")

    css = open("style.css").read()
    with doc.head:
        style(css)
    with doc:
        with table():
            with thead():
                tr(align="center", bgcolor="#0070FF", style="color:white")
                th("Project Name")
                th("Status")
            with tbody():
                for project in success_list:
                    with tr(_class='success'):
                        td(project['delivery']['project_name'], align="center")
                        td('SENT')
                if len(failed_list) > 0:
                    for project in failed_list:
                        with tr(_class='failed'):
                            td(project['delivery']
                               ['project_name'], align="center")
                            td(f"{project['attachment']}")

    filename = 'filename.html'
    f = open(filename, "w")
    f.write(doc.render())
    f.close()

    return filename
