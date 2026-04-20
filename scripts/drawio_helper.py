#!/usr/bin/env python3
"""Helper to generate drawio XML using AWS4 icons with a concise Python DSL."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

# AWS colors by common service categories
COLOR = {
    'orange': '#FF9900',   # Compute
    'red': '#DD344C',      # Security / IAM
    'blue': '#3B48CC',     # Networking / DB
    'green': '#7AA116',    # DB / Analytics
    'ec2': '#ED7100',
    'text': '#232F3E',
    'gray': '#666666',
    'bg_light': '#F5F5F5',
    'lambda': '#ED7100',
    'cognito': '#DD344C',
}

ICON_FILL = {
    'api_gateway': '#E7157B',
    'appsync': '#E7157B',
    'cognito': '#DD344C',
    'lambda': '#ED7100',
    'ecs': '#ED7100',
    'eks': '#ED7100',
    'fargate': '#ED7100',
    'ecr': '#ED7100',
    'ec2': '#ED7100',
    'dynamodb': '#3334B9',
    'rds': '#3334B9',
    'aurora': '#3334B9',
    'application_load_balancer': '#8C4FFF',
    'cloudfront': '#8C4FFF',
    'route_53': '#8C4FFF',
    'simple_storage_service': '#7AA116',
    's3': '#7AA116',
    'elastic_file_system': '#7AA116',
    'simple_queue_service': '#E7157B',
    'sqs': '#E7157B',
    'simple_notification_service': '#E7157B',
    'sns': '#E7157B',
    'step_functions': '#E7157B',
    'eventbridge': '#E7157B',
    'identity_and_access_management': '#DD344C',
    'waf': '#DD344C',
    'shield': '#DD344C',
    'certificate_manager': '#DD344C',
    'cloudwatch': '#E7157B',
    'x_ray': '#E7157B',
    'kinesis': '#8C4FFF',
    'app_runner': '#ED7100',
    'amplify': '#E7157B',
    'backup': '#E7157B',
    'systems_manager': '#E7157B',
    'app2container': '#ED7100',
    'secrets_manager': '#DD344C',
    'mq': '#E7157B',
    'managed_streaming_for_apache_kafka': '#8C4FFF',
}


def icon(icon_id: str, x: int, y: int, label: str = '', w: int = 50, h: int = 50,
         fill: Optional[str] = None, res_id: Optional[str] = None) -> str:
    """AWS4 resource icon + optional label below."""
    key = icon_id
    fill_color = fill or ICON_FILL.get(key, '#FF9900')
    res = res_id or key
    out = (
        f'<mxCell id="{icon_id}_{x}_{y}" value="" '
        f'style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;'
        f'fillColor={fill_color};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;'
        f'verticalAlign=top;align=center;html=1;fontSize=10;fontStyle=0;aspect=fixed;'
        f'shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res};" '
        f'vertex="1" parent="1">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
        f'</mxCell>\n'
    )
    if label:
        # y+58 per spec
        lx = x - 20
        lw = w + 40
        out += (
            f'<mxCell id="lbl_{icon_id}_{x}_{y}" value="{label}" '
            f'style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;'
            f'fontSize=10;fontColor=#232F3E;" vertex="1" parent="1">\n'
            f'  <mxGeometry x="{lx}" y="{y+58}" width="{lw}" height="20" as="geometry"/>\n'
            f'</mxCell>\n'
        )
    return out


def text_box(id_: str, x: int, y: int, w: int, h: int, text: str,
             size: int = 11, bold: bool = False, color: str = '#232F3E',
             align: str = 'center') -> str:
    fs = 1 if bold else 0
    return (
        f'<mxCell id="{id_}" value="{text}" '
        f'style="text;html=1;strokeColor=none;fillColor=none;align={align};'
        f'verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize={size};'
        f'fontStyle={fs};fontColor={color};" vertex="1" parent="1">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
        f'</mxCell>\n'
    )


def box(id_: str, x: int, y: int, w: int, h: int, title: str = '',
        fill: str = '#FFFFFF', stroke: str = '#666666', sw: int = 1,
        color: str = '#232F3E', bold: bool = True, fsize: int = 12,
        rounded: bool = True) -> str:
    fs = 1 if bold else 0
    r = 1 if rounded else 0
    return (
        f'<mxCell id="{id_}" value="{title}" '
        f'style="rounded={r};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};'
        f'strokeWidth={sw};fontSize={fsize};fontStyle={fs};fontColor={color};'
        f'verticalAlign=top;spacingTop=8;" vertex="1" parent="1">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
        f'</mxCell>\n'
    )


def multitext(id_: str, x: int, y: int, w: int, h: int, text: str,
              size: int = 10, color: str = '#232F3E', align: str = 'left') -> str:
    """Multiline text with html breaks (use &#10; for newlines)."""
    return (
        f'<mxCell id="{id_}" value="{text}" '
        f'style="text;html=1;align={align};verticalAlign=top;whiteSpace=wrap;'
        f'fontSize={size};fontColor={color};" vertex="1" parent="1">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
        f'</mxCell>\n'
    )


def group_vpc(id_: str, x: int, y: int, w: int, h: int, label: str = 'VPC',
              stroke: str = '#248814', fill: str = '#E9F3E6') -> str:
    return (
        f'<mxCell id="{id_}" value="{label}" '
        f'style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],'
        f'[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];'
        f'outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;'
        f'fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;'
        f'grIcon=mxgraph.aws4.group_vpc;strokeColor={stroke};fillColor={fill};'
        f'verticalAlign=top;align=left;spacingLeft=30;fontColor={stroke};dashed=0;" '
        f'vertex="1" parent="1">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
        f'</mxCell>\n'
    )


def group_cloud(id_: str, x: int, y: int, w: int, h: int, label: str = 'AWS Cloud',
                stroke: str = '#232F3E', fill: str = '#F2F2F2') -> str:
    return (
        f'<mxCell id="{id_}" value="{label}" '
        f'style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],'
        f'[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];'
        f'outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;'
        f'fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;'
        f'grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor={stroke};fillColor={fill};'
        f'verticalAlign=top;align=left;spacingLeft=30;fontColor={stroke};dashed=0;" '
        f'vertex="1" parent="1">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
        f'</mxCell>\n'
    )


def group_az(id_: str, x: int, y: int, w: int, h: int, label: str = 'AZ') -> str:
    return (
        f'<mxCell id="{id_}" value="{label}" '
        f'style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],'
        f'[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];'
        f'outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;'
        f'fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;'
        f'grIcon=mxgraph.aws4.group_availability_zone;strokeColor=#147EBA;fillColor=#E7F7FE;'
        f'verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=1;" '
        f'vertex="1" parent="1">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
        f'</mxCell>\n'
    )


def group_account(id_: str, x: int, y: int, w: int, h: int, label: str = 'AWS Account',
                  stroke: str = '#CD2264', fill: str = '#FCE4EC') -> str:
    return (
        f'<mxCell id="{id_}" value="{label}" '
        f'style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],'
        f'[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];'
        f'outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;'
        f'fontStyle=1;container=1;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;'
        f'grIcon=mxgraph.aws4.group_account;strokeColor={stroke};fillColor={fill};'
        f'verticalAlign=top;align=left;spacingLeft=30;fontColor={stroke};dashed=0;" '
        f'vertex="1" parent="1">\n'
        f'  <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>\n'
        f'</mxCell>\n'
    )


def arrow(id_: str, sx: int, sy: int, tx: int, ty: int, label: str = '',
          color: str = '#666666', dashed: bool = False, sw: int = 2) -> str:
    d = 1 if dashed else 0
    return (
        f'<mxCell id="{id_}" value="{label}" '
        f'style="endArrow=classic;html=1;rounded=0;strokeColor={color};strokeWidth={sw};'
        f'fontSize=10;fontColor={color};dashed={d};" edge="1" parent="1">\n'
        f'  <mxGeometry relative="1" as="geometry">\n'
        f'    <mxPoint x="{sx}" y="{sy}" as="sourcePoint"/>\n'
        f'    <mxPoint x="{tx}" y="{ty}" as="targetPoint"/>\n'
        f'  </mxGeometry>\n'
        f'</mxCell>\n'
    )


def wrap(title: str, body: str, page_w: int = 1000, page_h: int = 600,
         diagram_id: str = 'diag') -> str:
    return (
        f'<mxfile host="app.diagrams.net" modified="2026-04-20T18:00:00.000Z" agent="Claude" version="24.0.0">\n'
        f'  <diagram id="{diagram_id}" name="Diagram">\n'
        f'    <mxGraphModel dx="1422" dy="757" grid="1" gridSize="10" guides="1" tooltips="1" '
        f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" '
        f'pageHeight="{page_h}" math="0" shadow="0">\n'
        f'      <root>\n'
        f'        <mxCell id="0"/>\n'
        f'        <mxCell id="1" parent="0"/>\n'
        f'        {text_box("title", 20, 10, page_w-40, 30, title, size=14, bold=True)}\n'
        f'        {body}\n'
        f'      </root>\n'
        f'    </mxGraphModel>\n'
        f'  </diagram>\n'
        f'</mxfile>\n'
    )
