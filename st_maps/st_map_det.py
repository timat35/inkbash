import sys
import os
from lxml import etree

base = etree.parse(open(sys.argv[1]))
root = base.getroot()
legend_nb= 0

dir_folder = os.path.dirname(__file__)



root.set("width", "565.92426")
root.set("height", "293.53516")
root.set("viewBox", "0 0 424.44319 220.15137")

map = root[1]
map.set("transform", "matrix(0.15625,0,0,0.15625,-13.296351,-136.34035)")

#get the legend index start and the legend number
for child in map:
    temp = child.get("style")
    if "rgb(94.90196" in temp:
        legend_index = map.index(child)
        legend_nb = legend_nb + 1

legend_index = legend_index-(legend_nb*2)+2


# move legend square and change stroke
for i in range(0,legend_nb) :
    map.remove(map[legend_index+i])
    temp_style = map[legend_index+i].get("style")
    temp_rep = temp_style.replace('stroke-width:0.853583', 'stroke-width:1.92')
    temp_pos = map[legend_index+i].get("d").split()
    y_coord = temp_pos[2]
    pos = "m 134.05665," + temp_pos[2] + " h 72.56641 v -38.5507 h -72.56641 z m 0,0"
    map[legend_index+i].set("style", temp_rep)
    map[legend_index+i].set("d", pos)


# move legend text
shift = float(map[legend_index+legend_nb][0].get('x')) - 219.575
for i in range(0,legend_nb) :


    for child in map[legend_index+i+legend_nb]:
        temp = float(child.get('x'))-shift
        child.set('x', str(temp))

# move legend title if exist
legend_title = map[legend_index-1]
temp = legend_title.get("style")

if "fill:rgb(0" in temp:
    shift = float(legend_title[0].get('x')) - 134.05665

    for child in legend_title:
        temp = float(child.get('x'))-shift
        child.set('x', str(temp))

    legend_title.set("transform", "matrix(1.231145,0,0,1.231145,-31.5048,-540.25869)")

# move legend title 2nd line if exist
legend_title = map[legend_index-2]
temp = legend_title.get("style")

if "fill:rgb(0" in temp:
    shift = float(legend_title[0].get('x')) - 134.05665

    for child in legend_title:
        temp = float(child.get('x'))-shift
        child.set('x', str(temp))

    legend_title.set("transform", "matrix(1.231145,0,0,1.231145,-31.5048,-420.25869)")



dis = etree.parse(open(os.path.join(dir_folder, 'disclaimer.svg')))
root_dis = dis.getroot()

#add title
if len(sys.argv) > 4:
    title = root_dis[3][1]
    title.set('x', '212.26086')
    title.set('y', '16.089844')
    temp_style = title[0].get("style")
    temp_title = temp_style.replace('font-size:4.23333311px', 'font-size:12.00000006px')
    title[0].set('style', temp_title)
    title[0].text = sys.argv[4]
    root.append(title)

#add disclaimer
g_dis = root_dis[3][0]
g_dis.set("transform", "matrix(0.9375,0,0,0.9375,-15.085697,269.42903)")

g_dis[0][0].text = "Data source: " + sys.argv[2]
g_dis[0][1].text = "Map production: " + sys.argv[3]
g_dis[0].remove(g_dis[0][3])

g_dis[1][1][0].text = "© WHO 2020. All rights reserved"

#resize graph if title present
if len(sys.argv) > 4:
    map.set("transform", "matrix(0.15625,0,0,0.15625,-13.296351,-112.25051)")
    g_dis.set("transform", "matrix(0.9375,0,0,0.9375,-15.085697,293.51887)")
    root.set("height", "325.65494")
    root.set("viewBox", "0 0 424.44319 244.24121")


root.append(g_dis)
map.remove(map[0])


base.write(sys.argv[1], pretty_print=False)
#subprocess.Popen(['inkscape', '-f=' + sys.argv[1] ])
#print("look on inkscape")





