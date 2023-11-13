import os
import subprocess



# 指定文件夹路径
save_path = os.getcwd()


# 创建16个R Markdown文档

# region
for band in range(1, 5):
    for section in range(1, 5):
        section_name = ""
        if section == 1:
            section_name = "Text"
        elif section == 2:
            section_name = "Writing"
        elif section == 3:
            section_name = "Language"
        elif section == 4:
            section_name = "CET-4"

        filename = os.path.join(save_path, f"B{band}-{section_name}.Rmd")
        with open(filename, 'w') as file:
            # 写入元信息
            file.write("---\n")
            file.write(f"title: \"B{band}-{section_name}\"\n")
            file.write("author: \"Ning Ning\"\n")
            file.write("date: \" `r format(Sys.Date(), '%d %B, %Y')`\"\n")
            file.write("output:\n")
            file.write("  revealjs::revealjs_presentation:\n")
            file.write("    incremental: true\n")
            file.write("    css: writing.css\n")
            file.write('    header: |\n')
            file.write("    slide_number: 'c/t'\n")  # 使用单引号将 'c/t' 包含在字符串内
          # 使用单引号将 'c/t' 包含在字符串内
            file.write("---\n\n")

            # 写入Section和H1标题
            for h1 in range(1, 7):
                section_title = f"B{band}-{section_name}-U{h1}"
                file.write(f"# {section_title}\n\n")

                if section_name.endswith("Text"):
                    h2_titles = ["Lead in", "Structural Analysis", "Close Reading", "Critical Thinking"]
                    for h2_title in h2_titles:
                        file.write(f"## {h2_title}\n\n")
                if section_name.endswith("Writing"):
                    h2_titles = ["Writing Technique", "Topic"]
                    for h2_title in h2_titles:
                        file.write(f"## {h2_title}\n\n")
                if section_name.endswith("Language"):
                    h2_titles = ["Translation", "Long sentences", "Grammar", "Essay Review"]
                    for h2_title in h2_titles:
                        file.write(f"## {h2_title}\n\n")
                if section_name.endswith("4"):
                    h2_titles = ["Section Name", "Exam Strategies", "Past Paper Practice"]
                    for h2_title in h2_titles:
                        file.write(f"## {h2_title}\n\n")
# endregion

# 填入授课内容

#region
def read_and_process_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_lines = file.readlines()

    contents_blocks = []
    current_block = []

    for line in markdown_lines:
        if line.startswith('### '):  # 新标题
            if current_block:
                contents_blocks.append('\n'.join(current_block).strip())
                current_block = []
        current_block.append(line.strip())

    if current_block:
        contents_blocks.append('\n'.join(current_block).strip())

    return contents_blocks

def update_rmd_files(folder_path, rmd_file_end, markdown_blocks, target_heading):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith(rmd_file_end)])
    contents_split = [markdown_blocks[i:i + 6] for i in range(0, len(markdown_blocks), 6)]

    for i, file in enumerate(files):
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            new_lines = []
            lead_in_counter = 0
            for line in lines:
                new_lines.append(line)
                if line.startswith(target_heading):
                    if lead_in_counter < len(contents_split[i]):
                        new_lines.append(contents_split[i][lead_in_counter] + "\n")
                        lead_in_counter += 1
            f.seek(0)
            f.truncate()
            f.writelines(new_lines)

# 文件路径和标题
folder_path = os.getcwd()
markdown_paths = [
    'allleadin.md',
    'allstructure.md',
    'alldetails.md',
    'allthinking.md',
    'allwriting.md'
]
rmd_file_ends = ['Text.Rmd', 'Text.Rmd', 'Text.Rmd', 'Text.Rmd', 'Writing.Rmd']
target_headings = ['## Lead in', '## Structural Analysis', '## Close Reading','## Critical Thinking', '## Task']

# 执行更新
for md_path, rmd_end, heading in zip(markdown_paths, rmd_file_ends, target_headings):
    full_md_path = os.path.join(folder_path, md_path)
    markdown_blocks = read_and_process_markdown(full_md_path)
    update_rmd_files(folder_path, rmd_end, markdown_blocks, heading)



print("生成R Markdown文档完成")

# endregion

# 渲染markdown文件
# region
for band in range(1, 5):
    for section in range(1, 5):
        section_name = ""
        if section == 1:
            section_name = "Text"
        elif section == 2:
            section_name = "Writing"
        elif section == 3:
            section_name = "Language"
        elif section == 4:
            section_name = "CET-4"


        html_path = os.getcwd()

        rmd_file = os.path.join(save_path, f"B{band}-{section_name}.Rmd")
        html_output = os.path.join(html_path, f"B{band}-{section_name}.html")
        subprocess.run(["Rscript", "-e", f"rmarkdown::render('{rmd_file}', output_file='{html_output}')"])


print("R Markdown文档渲染完成")
# endregion

# 组合起来#

# region
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ning Ning's English Class</title>
    <style>
        .section-container {
            display: flex;
            flex-direction: column; /* 垂直排列容器 */
            width: 200vw;
            height: 100vw;
        }

        .band-container {
            display: flex; /* 水平排列部分 */
            margin-left:20px;

        }

        .iframe {
            width: 50vw; /* 每个 iframe 占据视口宽度的一半 */
            height: 50vh; /* 每个 iframe 占据视口高度的一半 */
            margin-right: 25px; /* 页面之间的右边距，可根据需要调整 */
            margin-bottom: 20px;
        }
         .section-container {
            margin-top: 20px; /* 页面之间的下边距，可根据需要调整 */
        }
    </style>
</head>
<body>
    <div class="band-container">
        <div class="section-container">
            <iframe class="iframe" src="B1-Text.html"></iframe>
            <iframe class="iframe" src="B1-Writing.html"></iframe>
            <iframe class="iframe" src="B1-Language.html"></iframe>
            <iframe class="iframe" src="B1-CET-4.html"></iframe>
        </div>
        <div class="section-container">
            <iframe class="iframe" src="B2-Text.html"></iframe>
            <iframe class="iframe" src="B2-Writing.html"></iframe>
            <iframe class="iframe" src="B2-Language.html"></iframe>
            <iframe class="iframe" src="B2-CET-4.html"></iframe>
        </div>
        <div class="section-container">
            <iframe class="iframe" src="B3-Text.html"></iframe>
            <iframe class="iframe" src="B3-Writing.html"></iframe>
            <iframe class="iframe" src="B3-Language.html"></iframe>
            <iframe class="iframe" src="B3-CET-4.html"></iframe>
        </div>
        <div class="section-container">
            <iframe class="iframe" src="B4-Text.html"></iframe>
            <iframe class="iframe" src="B4-Writing.html"></iframe>
            <iframe class="iframe" src="B4-Language.html"></iframe>
            <iframe class="iframe" src="B4-CET-4.html"></iframe>
        </div>
    </div>
</body>
</html>
"""


# 将HTML内容写入文件
with open("index.html", "w") as html_file:
    html_file.write(html_content)

print("生成HTML文件完成")
# endregion