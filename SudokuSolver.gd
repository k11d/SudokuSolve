extends Node2D

var grid_nodes := []


func _ready():
	$GridContainer.connect("grid_updated", self, "recompute_grid")
	for n in $GridContainer.get_children():
		grid_nodes.append(n.get_instance_id())
	print(grid_nodes)


func recompute_grid(gvals_funcref):
	print("Got new grid values: ", gvals_funcref.call_func())
