import os
from datetime import datetime

import dominate
from dominate.tags import *


is_local = os.environ.get("local")


def format_monitoring_email(success_list, failed_list):
    timestamp = datetime.today().strftime('%d.%m.%Y')
    doc = dominate.document(title="Email sending Report")

    css = open("style.css").read()
    with doc.head:
        style(css)
    with doc:
        with table():
            with thead():
                tr(align="center", bgcolor="#0070FF", style="color:white")
                th("Project Name", align="center")
                th("Status", align="center")
            with tbody():
                for project in success_list:
                    item_key = 'project_name'
                    if 'CostCenter' in project['delivery']:
                        item_key = 'CostCenter'
                    with tr(_class='success'):
                        td(project['delivery'][item_key], align="center")
                        td('SENT', align="center")

                if len(failed_list) > 0:
                    for project in failed_list:
                        item_key = 'project_name'
                        if 'CostCenter' in project['delivery']:
                            item_key = 'CostCenter'
                        with tr(_class='failed'):
                            td(project['delivery']
                               [item_key], align="center")
                            td(f"{project['attachment']}", align="center")

    filename = f'sending_report_{timestamp}.html'
    if is_local:
        filename = '../data/' + filename
    else:
        filename = '/tmp/' + filename

    f = open(filename, "w")
    f.write(doc.render())
    f.close()

    return filename
