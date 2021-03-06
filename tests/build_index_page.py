import glob

html_files = glob.glob("tests/render/output/*.html")
json_files = glob.glob("tests/render/output/*.json")

html_list = ""
for f_ in html_files:
    html_list += '\t<li><a href="{}">{}</li>\n'.format(
        f_.split("/")[-1],
        f_.split(".")[-2],
    )

json_list = ""
for f_ in json_files:
    json_list += '\t<li><a href="{}">{}</li>\n'.format(
        f_.split("/")[-1],
        f_.split(".")[-2],
    )

html_file = """
<html>
<body>
  <h3>HTML</h3>
  <ul>
    {}
  </ul>
  <br/><br/>
  <h3>JSON</h3>
  <ul>
    {}
  </ul>
</body>
</html>
""".format(
    html_list,
    json_list
)

print(html_file)
