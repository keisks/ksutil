import os
import sys
import csv

"""
create html file to show workers submissions
"""

header = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <style>
    .input-sentence {
        background-color: #d3f4ff;
        color: black;
        padding-left: 3px;
        padding-right: 3px;

    }

    .cause-sentence {
        background-color: #fff8c9;
        color: black;
        padding-left: 3px;
        padding-right: 3px;

    }

    .block-sentence {
        background-color: #ffe2f9;
        color: black;
        padding-left: 3px;
        padding-right: 3px;

    }
  </style>
  </head>
  <body>
  <div class="container">
  <h1 align="center"> collected knowledge </h1>

"""

footer = """\
</div>
</body>
</html>
"""

DIR_PATH = sys.argv[1]
csv_file_path = os.path.join(DIR_PATH, "merged_results.csv")
csv_reader = csv.DictReader(open(csv_file_path, 'r'))
seed_dict = {}

# load merged_results file
for row in csv_reader:
    if not row["HITId"] in seed_dict.keys():
        seed_dict[row["HITId"]] = {}
        seed_dict[row["HITId"]]["cause"] = []
        seed_dict[row["HITId"]]["block"] = []
        seed_dict[row["HITId"]]["promprt"] = None
    # seed_dict[row["HITId"]]["seed"] = row["InputSentence"]
    seed_dict[row["HITId"]]["InputEvent1"] = row["InputEvent1"]
    seed_dict[row["HITId"]]["InputEvent2"] = row["InputEvent2"]
    seed_dict[row["HITId"]]["prompt"] = row["InputPrompt"]
    seed_dict[row["HITId"]]["cause"].append(row["cause"])
    seed_dict[row["HITId"]]["block"].append(row["block"])

print(header)

# print table
table_head = """\
<table class="table table-bordered">
<thead>
<tbody>
<tr align="center">
<td colspan="2">
"""

for hitid, sentences in seed_dict.items():
    print(table_head)
    print("Prompt (not shown to workers): ")
    print('<span><i>')
    print(sentences["prompt"])
    print('</i></span><br />')

    print('<span class="input-sentence">')
    print("Event1: ")
    print(sentences["InputEvent1"])
    print("<br />")
    print("Event2: ")
    print(sentences["InputEvent2"])
    print('</span>')

    print("</td></tr>")
    # print table header and seed
    print('<tr align="center">')
    print('<td style="width:50%"> <span class="cause-sentence"><b>CAUSES</b></span> </td>')
    print('<td style="width:50%"> <span class="block-sentence"><b>BLOCKS</b></span> </td>')
    print("</tr>")

    for cause, block in zip(sentences["cause"], sentences["block"]):
        print("<tr>")
        print('<td style="width:50%">' + cause + "</td>")
        print('<td style="width:50%">' + block + "</td>")
        print("</tr>")

    print("</tbody></thead></table>")

# read csv and add submissions

print(footer)


