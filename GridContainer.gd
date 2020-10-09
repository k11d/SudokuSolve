extends GridContainer


var buttons_ids := []
var _now_hovering : Object 
var gvalues = []
var node_instanceID_to_gvaluesID := {}
signal grid_updated


const grid_easy := [
	[5,3,0,0,7,0,0,0,0],
	[6,0,0,1,9,5,0,0,0],
	[0,9,8,0,0,0,0,6,0],
	[8,0,0,0,6,0,0,0,3],
	[4,0,0,8,0,3,0,0,1],
	[7,0,0,0,2,0,0,0,6],
	[0,6,0,0,0,0,2,8,0],
	[0,0,0,4,1,9,0,0,5],
	[0,0,0,0,8,0,0,7,9],
]

const grid_easy_1 := [
	 [5,0,0,6,7,0,9,0,0],
	 [0,4,0,8,0,0,0,0,0],
	 [8,0,0,5,0,0,6,1,3],
	 [0,6,2,4,0,0,0,7,0],
	 [1,0,0,0,0,3,0,2,0],
	 [3,7,4,9,0,8,0,0,0],
	 [0,9,6,1,0,7,8,0,2],
	 [2,1,8,0,0,6,0,4,5],
	 [0,5,0,0,8,0,0,9,0]
 ]

const hard_grid := [
	[0,7,0,0,0,0,0,0,0],
	[0,0,0,4,7,0,1,0,0],
	[0,0,9,0,8,0,0,6,0],
	[0,3,0,0,0,0,6,0,9],
	[5,0,7,0,0,0,0,8,0],
	[0,6,0,1,9,0,0,2,0],
	[0,1,0,3,0,0,0,0,2],
	[9,0,0,8,4,0,0,0,0],
	[0,0,0,0,0,0,0,7,0]
]



func _ready():
	_now_hovering = null
	gvalues.clear()
	for y in range(9):
		for x in range(9):
			var btn = Button.new()
			btn.text = " 0 "
			gvalues.append(0)
			node_instanceID_to_gvaluesID[btn.get_instance_id()] = len(gvalues)
			btn.align = Button.ALIGN_CENTER
			add_child(btn)
			btn.set_owner(self)
			btn.connect("mouse_entered", self, "hovering_button", [btn])
			btn.connect("mouse_exited", self, "no_hovering_button", [btn])
	

func _input(event):
	if event.is_action_pressed("ui_left_click"):
		if _now_hovering:
			var old_val = int(_now_hovering.text)
			if old_val < 9:
				_now_hovering.text = " " + str(old_val + 1) + " "
				emit_signal("grid_updated", funcref(self, "get_grid"))
	if event.is_action_pressed("ui_right_click"):
		if _now_hovering:
			var old_val = int(_now_hovering.text)
			if old_val > 0:
				_now_hovering.text = " " + str(old_val - 1) + " "
				emit_signal("grid_updated", funcref(self, "get_grid"))


func get_grid():
	var ret = {}
	for n in get_children():
		ret[node_instanceID_to_gvaluesID[n.get_instance_id()]] = int(n.text)
	return ret
func hovering_button(btn):
	btn.modulate = Color(1, 0, 0, 1)
	_now_hovering = btn
func no_hovering_button(btn):
	btn.modulate = Color(1, 1, 1, 1)
	_now_hovering = null
func load_grid(grid):
	gvalues.clear()
	for row in grid:
		for val in row:
			gvalues.append(val)
	var gnodes = get_children()	
	for n in range(len(gnodes)):
		gnodes[n].text = " " + str(gvalues[n]) + " "

func _on_btnLoadEasy_pressed():
	load_grid(grid_easy)
	emit_signal("grid_updated", funcref(self, "get_grid"))
