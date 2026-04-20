"""Lightweight builder for AWS-styled drawio diagrams (SAP training material).

Usage:
    from drawio_builder import Diagram, Colors

    d = Diagram(title="VPC Endpoint ...", width=1000, height=600)
    d.group_vpc(x=60,y=80,w=400,h=400,label="VPC A")
    d.icon("ec2", x=120, y=150, label="EC2")
    d.save("path.drawio")
"""
from __future__ import annotations
import os
from typing import List

AWS_FONT = "#232F3E"


class Colors:
    ORANGE = "#ED7100"   # EC2
    GREEN = "#248814"    # S3 / VPC (reused as VPC boundary)
    PURPLE = "#8C4FFF"   # Endpoint
    BLUE = "#3B48CC"     # VPC network / Interface EP highlights
    S3_GREEN = "#7AA116"
    DDB_BLUE = "#3334B9"
    MAGENTA = "#E7157B"  # Generic AWS service
    RED = "#DD344C"
    NAV = "#232F3E"
    GRAY = "#666666"
    YELLOW = "#FF9900"
    LIGHT_GREEN_BG = "#E9F3E6"
    LIGHT_BLUE_BG = "#EBF1FF"
    LIGHT_GRAY_BG = "#F5F5F5"
    LIGHT_YELLOW_BG = "#FFEFD5"


# AWS icon name -> (resIcon, fillColor)
ICONS = {
    "ec2": ("mxgraph.aws4.ec2", Colors.ORANGE),
    "endpoint": ("mxgraph.aws4.endpoint", Colors.PURPLE),
    "vpc": ("mxgraph.aws4.vpc", Colors.GREEN),
    "s3": ("mxgraph.aws4.s3", Colors.S3_GREEN),
    "dynamodb": ("mxgraph.aws4.dynamodb", Colors.DDB_BLUE),
    "route_53": ("mxgraph.aws4.route_53", "#8C4FFF"),
    "nat_gateway": ("mxgraph.aws4.nat_gateway", Colors.PURPLE),
    "nlb": ("mxgraph.aws4.network_load_balancer", Colors.PURPLE),
    "transit_gateway": ("mxgraph.aws4.transit_gateway", Colors.PURPLE),
    "direct_connect": ("mxgraph.aws4.direct_connect", "#8C4FFF"),
}

# Group styles: (grIcon, strokeColor, fillColor)
GROUPS = {
    "vpc": ("mxgraph.aws4.group_vpc", "#248814", "#E9F3E6"),
    "account": ("mxgraph.aws4.group_account", "#CD2264", "#F3D5DD"),
    "onprem": ("mxgraph.aws4.group_corporate_data_center", "#666666", "#F5F5F5"),
}


class Diagram:
    def __init__(self, title: str, width: int = 1000, height: int = 600, diagram_name: str = "diagram"):
        self.title = title
        self.width = width
        self.height = height
        self.cells: List[str] = []
        self.counter = 0
        self.diagram_name = diagram_name
        # Title at top
        self.text(x=20, y=12, w=width - 40, h=28, value=title,
                  fontsize=15, bold=True, color=Colors.NAV, align="center")

    def _uid(self, prefix="c"):
        self.counter += 1
        return f"{prefix}{self.counter}"

    def rect(self, x, y, w, h, fill="#FFFFFF", stroke=Colors.GRAY, stroke_width=1,
             value="", fontsize=10, bold=False, color=Colors.NAV, align="center",
             valign="middle", rounded=True, dashed=False, cid=None):
        cid = cid or self._uid("r")
        bold_s = 1 if bold else 0
        rounded_s = 1 if rounded else 0
        dashed_s = 1 if dashed else 0
        style = (f"rounded={rounded_s};whiteSpace=wrap;html=1;"
                 f"fillColor={fill};strokeColor={stroke};strokeWidth={stroke_width};"
                 f"fontSize={fontsize};fontStyle={bold_s};fontColor={color};"
                 f"align={align};verticalAlign={valign};dashed={dashed_s};")
        self.cells.append(
            f'<mxCell id="{cid}" value="{_esc(value)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        return cid

    def text(self, x, y, w, h, value, fontsize=11, bold=False, color=Colors.NAV, align="center"):
        cid = self._uid("t")
        bold_s = 1 if bold else 0
        style = (f"text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;"
                 f"whiteSpace=wrap;rounded=0;fontSize={fontsize};fontStyle={bold_s};fontColor={color};")
        self.cells.append(
            f'<mxCell id="{cid}" value="{_esc(value)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        return cid

    def group(self, x, y, w, h, label, kind="vpc"):
        g_icon, stroke, fill = GROUPS[kind]
        cid = self._uid("g")
        style = (
            "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],"
            "[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
            "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;"
            "container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;"
            f"grIcon={g_icon};strokeColor={stroke};fillColor={fill};"
            f"verticalAlign=top;align=left;spacingLeft=30;fontColor={Colors.NAV};dashed=0;"
        )
        self.cells.append(
            f'<mxCell id="{cid}" value="{_esc(label)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        return cid

    def group_vpc(self, x, y, w, h, label):
        return self.group(x, y, w, h, label, "vpc")

    def group_account(self, x, y, w, h, label):
        return self.group(x, y, w, h, label, "account")

    def group_onprem(self, x, y, w, h, label):
        return self.group(x, y, w, h, label, "onprem")

    def icon(self, kind: str, x, y, label=None, size=50, label_width=120):
        res, fill = ICONS[kind]
        cid = self._uid("i")
        style = (f"sketch=0;outlineConnect=0;fontColor={Colors.NAV};gradientColor=none;"
                 f"fillColor={fill};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;"
                 f"verticalAlign=top;align=center;html=1;fontSize=11;fontStyle=0;aspect=fixed;"
                 f"shape=mxgraph.aws4.resourceIcon;resIcon={res};")
        self.cells.append(
            f'<mxCell id="{cid}" value="" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{size}" height="{size}" as="geometry"/></mxCell>'
        )
        if label:
            lcx = x + size / 2 - label_width / 2
            self.text(lcx, y + 58, label_width, 22, value=label, fontsize=10)
        return cid

    def arrow(self, src, tgt, color=Colors.GRAY, width=2, dashed=False, label=None):
        aid = self._uid("a")
        dashed_s = 1 if dashed else 0
        style = f"endArrow=classic;html=1;strokeColor={color};strokeWidth={width};dashed={dashed_s};"
        if label:
            style += "labelBackgroundColor=#FFFFFF;fontSize=10;"
            label_attr = f' value="{_esc(label)}"'
        else:
            label_attr = ""
        self.cells.append(
            f'<mxCell id="{aid}"{label_attr} style="{style}" edge="1" parent="1" '
            f'source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        return aid

    def arrow_xy(self, x1, y1, x2, y2, color=Colors.GRAY, width=2, dashed=False, label=None):
        aid = self._uid("a")
        dashed_s = 1 if dashed else 0
        style = f"endArrow=classic;html=1;strokeColor={color};strokeWidth={width};dashed={dashed_s};"
        if label:
            style += "labelBackgroundColor=#FFFFFF;fontSize=10;"
            label_attr = f' value="{_esc(label)}"'
        else:
            label_attr = ""
        self.cells.append(
            f'<mxCell id="{aid}"{label_attr} style="{style}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/>'
            f'</mxGeometry></mxCell>'
        )
        return aid

    def note(self, x, y, w, h, value, stroke=Colors.GRAY, fill="#FFFFFF"):
        """Left-aligned informational note."""
        cid = self._uid("n")
        style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=1;"
                 f"fontSize=10;fontColor={Colors.NAV};verticalAlign=top;align=left;"
                 f"spacingLeft=8;spacingTop=6;spacingRight=8;")
        self.cells.append(
            f'<mxCell id="{cid}" value="{_esc(value)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        return cid

    def to_xml(self) -> str:
        body = "\n".join(self.cells)
        return f"""<mxfile host="app.diagrams.net" modified="2026-04-20T00:00:00.000Z" agent="Claude" version="24.0.0">
  <diagram id="{self.diagram_name}" name="{self.diagram_name}">
    <mxGraphModel dx="1422" dy="757" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.width}" pageHeight="{self.height}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_xml())


def _esc(s: str) -> str:
    if s is None:
        return ""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("\n", "&#10;"))
