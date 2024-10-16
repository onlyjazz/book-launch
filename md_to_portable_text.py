import markdown
from bs4 import BeautifulSoup
import uuid

def markdown_to_portable_text(markdown_content):
    # Convert Markdown to HTML
    html = markdown.markdown(markdown_content)

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Initialize Portable Text array
    portable_text = []

    for element in soup.children:
        if element.name is None:
            continue

        if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            block = {
                "_type": "block",
                "_key": str(uuid.uuid4()),
                "children": [],
                "style": element.name if element.name != 'p' else 'normal'
            }

            for child in element.children:
                if child.name is None:
                    span = {
                        "_type": "span",
                        "_key": str(uuid.uuid4()),
                        "text": child.string,
                        "marks": []
                    }
                    block["children"].append(span)
                elif child.name in ['strong', 'em']:
                    span = {
                        "_type": "span",
                        "_key": str(uuid.uuid4()),
                        "text": child.string,
                        "marks": [child.name]
                    }
                    block["children"].append(span)

            portable_text.append(block)

        elif element.name in ['ul', 'ol']:
            list_style = 'bullet' if element.name == 'ul' else 'number'
            for li in element.find_all('li', recursive=False):
                block = {
                    "_type": "block",
                    "_key": str(uuid.uuid4()),
                    "children": [{
                        "_type": "span",
                        "_key": str(uuid.uuid4()),
                        "text": li.get_text(),
                        "marks": []
                    }],
                    "style": "normal",
                    "listItem": list_style
                }
                portable_text.append(block)

    return portable_text


# Example usage
markdown_content = """
### This is a title from the LLM

This is a **bold** and *italic* text.

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2
"""

portable_text = markdown_to_portable_text(markdown_content)
print(portable_text)
