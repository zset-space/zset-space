""" To recover the Python script to generate this SVG, delete the line above -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%" viewBox="-18 -192 225 225">
 <title>hypersphere volume and surface area graphs</title>
 <desc>Graphs of volumes and surface areas of n-spheres of radius 1 by CMG Lee. The apparent intersection is an artifact of the differing scales. In the SVG file, hover over a point to see its decimal value.</desc>
 <style type="text/css">
  #main { font-family:Helvetica,Arial,sans-serif; font-size:12px; text-anchor:middle;
          stroke-linejoin:round; stroke:none; fill:none; }
  #main:hover            { stroke-opacity:0.2; fill-opacity:0.2; }
  .nofade, .active:hover { stroke-opacity:1;   fill-opacity:1;   }
  text      { cursor:default; }
  .pi       { font-family:Times,Times New Roman,serif; }
  .sup      { font-size:4px; }
  .bold     { font-size:8px; font-weight:bold; }
  .stroke_v { stroke:#cc00ff; }
  .stroke_s { stroke:#0000cc; }
  .fill_v   {   fill:#cc00ff; }
  .fill_s   {   fill:#0000cc; }
 </style>
 <defs>
  <radialGradient id="grad_sphere" cx="50%" cy="50%" r="50%" fx="30%" fy="30%">
   <stop offset="10%" stop-color="#000000"/>
   <stop offset="90%" stop-color="#666666"/>
  </radialGradient>
  <pattern id="pattern_grid_1" patternUnits="userSpaceOnUse" width="5" height="5">
   <rect x="0" y="0" width="9999" height="9999" stroke-opacity="0.1" stroke="#ffffff" fill="none"/>
  </pattern>
  <pattern id="pattern_grid_5" patternUnits="userSpaceOnUse" width="25" height="25">
   <rect x="0" y="0" width="9999" height="9999" stroke-opacity="0.2" stroke="#ffffff" fill="url(#pattern_grid_1)"/>
  </pattern>
  <circle id="marker_v" cx="0" cy="0" r="2" stroke="none"/>
  <circle id="marker_s" cx="0" cy="0" r="2" stroke="#0000cc" fill="none"/>
 </defs>
 <circle cx="0" cy="0" r="99999" fill="#000000"/>
 <g id="main">
  <rect id="frame" x="0" y="-175" width="150" height="175" stroke="#999999" fill="url(#pattern_grid_5)"/>
<!-- BEGIN_DYNAMIC_SVG { -->
<!-- } END_DYNAMIC_SVG -->
  <g transform="translate(0,21)" fill="#ffffff">
   <text x="0"   y="0.7ex">0</text>
   <text x="10"  y="0.7ex">1</text>
   <text x="20"  y="0.7ex">2</text>
   <text x="31"  y="0.7ex">3</text>
   <text x="50"  y="0.7ex" class="stroke_v">5</text>
   <text x="70"  y="0.7ex" class="stroke_s">7</text>
   <text x="100" y="0.7ex">10</text>
   <text x="150" y="0.7ex">15</text>
  </g>
  <g transform="translate(0,7)" fill="#ffffff">
   <circle cx="0"  cy="0" r="1"/>
   <path d="M 6,0 H 14" stroke="#666666"/>
   <circle cx="7"  cy="0" r="1"/>
   <circle cx="13" cy="0" r="1"/>
   <circle cx="20" cy="0" r="4"   fill="#999999" stroke="#666666"/>
   <circle cx="30" cy="0" r="4.7" fill="url(#grad_sphere)"/>
   <g transform="translate(40,0)" fill="url(#grad_sphere)">
    <circle  cx="0" cy="0"  r="4.7" fill="#999999"/>
    <ellipse cx="0" cy="-3" rx="2.5" ry="1.3"/>
    <ellipse cx="0" cy="-2" rx="4"   ry="2.2"/>
    <ellipse cx="0" cy="0"  rx="4.5" ry="2.5"/>
    <ellipse cx="0" cy="2"  rx="4"   ry="2.2"/>
    <ellipse cx="0" cy="3"  rx="2.5" ry="1.3"/>
   </g>
  </g>
 </g>
</svg>
<!-- Please retain this and other comments, which contain Python code to generate this SVG. """
import re, math
from fractions import Fraction
def fmt(string): ## string.format(**vars()) using tags {expression!format} by CMG Lee
 def f(tag): i_sep = tag.rfind('!'); return (re.sub(r'\.0+$', '', str(eval(tag[1:-1])))
  if (i_sep < 0) else ('{:%s}' % tag[i_sep + 1:-1]).format(eval(tag[1:i_sep])))
 return (re.sub(r'(?<!{){[^{}]+}', lambda m:f(m.group()), string)
         .replace('{{', '{').replace('}}', '}'))
def append(obj, string): return obj.append(fmt(string))
def format_tab(*arg): return '\t'.join([str(el) for el in (arg if len(arg) > 1 else arg[0])])
def tabulate(recordss):
 lens = [(-1 if type(fields[0]) in [str] else 1) *
         max([len(str(field)) for field in fields]) for fields in zip(*recordss)]
 return '\n'.join(['|'.join(['%*s' % (lens[i_col], records[i_col])
                            for i_col in range(len(recordss[0]))]) for records in recordss])
def roundm(x, multiple = 1): return int(math.floor(float(x) / multiple + 0.5)) * multiple
def hex_rgb(colour): ## convert [#]RGB to #RRGGBB and [#]RRGGBB to #RRGGBB
 return '#%s' % (colour if len(colour) > 4 else ''.join([c * 2 for c in colour])).lstrip('#')
def try_int_float(field):
 try:     return int(field)
 except:
  try:    return float(field)
  except: return field

graphs = [
 ['v', 5,None ,lambda n:pi**(n*0.5)  /gamma(n*0.5+1),[-1,-1,2,-3,-3, -2, 1, 4, 4,-3,  3,-5, 2,-6,-1, 6],
                                                     [-1,-1,1,-1,-2, -5,-4,-2,-1, 4, -3, 1,-4, 2, 4, 0]],
 ['s', 5,'8,3',lambda n:pi**(n*0.5)*2/gamma(n*0.5  ),[3, 2, -3, 3, 3,  2,-1,-3, 1, 4,  3, 4, 3, 4, 4, 6],
                                                     [1, 2, -2, 2, 3,  5,-1,-5,-5,-2, -2,-3,-4,-4,-3,-1]],
]
n_max   = 15
x_scale = 10
pi      = math.pi
gamma   = math.gamma
outs    = []
outss   = [['n', 'value', 'x', 'y', 'pi^', 'fraction']]
for graph in graphs:
 (id, scale, dash, formula, x_labels, y_labels) = graph
 out_dash    = ' stroke-dasharray="%s"' % dash if (dash) else ''
 out_path_ds = []
 out_markers = []
 (y_int_n_max, x_int_n_max) = (0, 0)
 for n in range(1, n_max + 1):
  (y, x) = (-scale * formula(n), n * x_scale)
  if (y < y_int_n_max): (y_int_n_max, x_int_n_max) = (y, x)
 print(y_int_n_max, x_int_n_max)
 for x in range(n_max * x_scale + 1):
  n      = float(x) / x_scale
  value  = formula(n) if (n > 0 or id != 's') else 0
  y      = -scale * value
  out_xy = fmt('''{x},{y!.3f}''')
  append(out_path_ds, '''{out_xy}''')
  if (x % x_scale == 0):
   n           = int(round(n))
   pi_power    = n // 2
   pi_remove   = math.pi ** -pi_power
   fraction    = Fraction(value * pi_remove).limit_denominator()
   denominator = fraction.denominator
   underline   = '_' * max(len(str(fraction.numerator)) + 1, len(str(denominator)))
   out_labels  = []
   dy_label    = 2
   if (pi_power == 0 or fraction.numerator != 1): append(out_labels, '<tspan>{fraction.numerator}</tspan>')
   if (pi_power > 0): append(out_labels, '<tspan class="pi">&#960;</tspan>')
   if (pi_power > 1): append(out_labels, '<tspan class="sup" dy="-1ex">{pi_power}</tspan><tspan class="sup" x="0" dy="1ex">&#160;</tspan>')
   if (denominator != 1): append(out_labels, '<tspan x="0">{underline}</tspan><tspan x="0" dy="1em">{denominator}</tspan>')
   # print(fmt('{fraction} pi^{pi_power}'),out_labels)
   (x_label, y_label) = (x_labels[n] * 3, y_labels[n] * 3)
   out_class          = ''' class="bold"''' if (x == x_int_n_max) else ''
   append(out_markers, r'''\
   <g class="active" transform="translate({out_xy})" stroke="#000000">
    <text id="label_{id}_{n}"{out_class} transform="translate({x_label},{y_label})" x="0" y="0" font-size="6" stroke-width="2">{''.join(out_labels)}</text>
    <use xlink:href="#label_{id}_{n}" stroke="none"/>
    <use xlink:href="#marker_{id}"/>
    <title>{id.upper()}({n - 1 if (id == 's') else n}) {'~' if (n > 1) else '='} {re.sub(r'\.?0+$', '', ('%.10f' % (value)))}</title>
   </g>''')
   outss.append([n, value, x, y, pi_power, fraction])
 y_axis = n_max * x_scale if (id == 's') else 0
 append(outs, r'''\
  <g class="stroke_{id} fill_{id}">
   <g fill="none"{out_dash}>
    <path d="M{' L'.join(out_path_ds)}"/>
    <path d="M{x_int_n_max},12.8 V{y_int_n_max!.3f} H{y_axis}" stroke-width="0.5"/>
   </g>
{'\\n'.join(out_markers)}
  </g>''')
print(tabulate(outss))

out_p = 'width="100%" height="100%" viewBox="-18 -192 225 225"'

## Compile everything into an .svg file
myself   = open(__file__, 'r').read() ## the contents of this very file
file_out = open(__file__[:__file__.rfind('.')] + '.svg', 'w') ## *.* -> *.svg
try: ## use try/finally so that file is closed even if write fails
 file_out.write('''<?xml version="1.0" encoding="utf-8"?><!%s
%s%s%s\n%s%s''' % ('-' + '-', ## because SVG comments cannot have 2 consecutive '-'s
  myself[ : myself.find('width',myself.find('<svg'))], ## assume width specified before height/viewBox
  out_p, ## replace SVG width/height/viewBox with {out_p} & dynamic SVG block with {outs} contents
  myself[myself.find('>',myself.find('<svg')) : myself.find('\n',myself.find('BEGIN_'+'DYNAMIC_SVG'))],
  '\n'.join(outs), myself[myself.rfind('\n',0,myself.find('END_'+'DYNAMIC_SVG')) : ]))
finally:
 file_out.close()

## SVG-Python near-polyglot framework version 2 by CMG Lee (Feb 2016) -->
