n = 55

svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position: absolute;">
    <defs>
        <filter id="floodfill" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
            <feComponentTransfer in="SourceGraphic" result="limit">
                <feFuncA type="discrete" tableValues="0 0 1" />
            </feComponentTransfer>
            <feComponentTransfer in="SourceGraphic" result="seed0">
                <feFuncA type="discrete" tableValues="0 1 0" />
            </feComponentTransfer>
"""

for i in range(1, n + 1):
    svg += f'            <feMorphology in="seed{i-1}" operator="dilate" radius="16" result="dilate{i}"></feMorphology>\n'
    svg += f'            <feComposite in="dilate{i}" in2="limit" operator="out" result="seed{i}"></feComposite>\n'

svg += f"""
                <feMerge>
                    <feMergeNode in="seed{n}"></feMergeNode>
                    <feMergeNode in="limit"></feMergeNode>
                </feMerge>
        </filter>
    </defs>
</svg>
"""

with open("floodfill.txt", "w") as file:
    file.write(svg)