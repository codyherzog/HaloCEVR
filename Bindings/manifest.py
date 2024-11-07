import json

controllers = ["oculus_touch", "knuckles"]
boolActions = ["Jump","SwitchGrenades","Interact","SwitchWeapons","Melee","Flashlight","Grenade","Fire","MenuForward","MenuBack","Crouch","Zoom","Reload", "Recentre", "TwoHandGrip"]
vec1Actions = []
vec2Actions = ["Look", "Move"]
poseActions = ["Tip"]

bindings = {
    "Jump" : { "h" : "right", "b" : "joystick|north", "f" : True},
    "TwoHandGrip" : {"h" : "left", "b" : "grip", "f" : True},
    "SwitchWeapons" : {"h" : "right", "b" : "grip", "f" : True},
    "MenuBack" : {"h" : "left", "b" : "y", "f" : True},
    "SwitchGrenades" : {"h" : "left", "b" : "x", "f" : True}, 
    "Grenade" : {"h" : "right", "b" : "a", "f" : True},
    "Interact" : {"h" : "right", "b" : "b", "f" : True},
    "Zoom" : {"h" : "left", "b" : "trigger", "f" : True},
    "Fire" : {"h" : "right", "b" : "trigger", "f" : True},
    "Crouch" : {"h" : "right", "b" : "joystick|south", "f" : True},
    "Look" : {"h" : "right", "b" : "joystick", "f" : True},
    "Move" : {"h" : "left", "b" : "joystick", "f" : True}
}

manifest = {
    "default_bindings" : [],
    "actions" : [],
    "action_sets" : [
        {
            "name" : "/actions/default",
            "usage" : "leftright"
        }
    ]
}

poses = {
    "Tip" : "tip"
}

variants = ["Right Handed", "Left Handed"]

for v in variants:
    for c in controllers:
        filename = c + "_"+v.split(' ', 1)[0].lower()
        manifest["default_bindings"].append({"controller_type" : c, "binding_url" : filename + ".json"})

for b in boolActions:
    manifest["actions"].append({"name" : "/actions/default/in/" + b, "requirement" : "suggested", "type" : "boolean"})

for v in vec1Actions:
    manifest["actions"].append({"name" : "/actions/default/in/" + v, "requirement" : "suggested", "type" : "vector1"})
    
for v in vec2Actions:
    manifest["actions"].append({"name" : "/actions/default/in/" + v, "requirement" : "suggested", "type" : "vector2"})

for p in poseActions:
    manifest["actions"].append({"name" : "/actions/default/in/Left" + p, "requirement" : "suggested", "type" : "pose"})
    manifest["actions"].append({"name" : "/actions/default/in/Right" + p, "requirement" : "suggested", "type" : "pose"})

manifest["actions"].append({"name" : "/actions/default/in/LeftHand", "type" : "skeleton", "skeleton": "/skeleton/hand/left"})
manifest["actions"].append({"name" : "/actions/default/in/RightHand", "type" : "skeleton", "skeleton": "/skeleton/hand/right"})

try:
    with open("actions.json", "w") as f:
        f.write(json.dumps(manifest, indent=4))
except:
    print ("failed to create manifest")
else:
    print ("successfully created manifest")

#todo: merge thumbstick dpad actions


swapmap = {
    "oculus_touch" : {
        "a" : "x",
        "b" : "y",
        "x" : "a",
        "y" : "b"
    }
}

for v in variants:
    for c in controllers:
        
        filename = c + "_"+v.split(' ', 1)[0].lower()
        
        invert = "left" in v.lower()
        
        controller = {
            "bindings" : {
                "/actions/default" : {
                    "haptics" : [],
                    "poses" : [],
                    "sources" : [],
                    "skeleton" : []
                }
            },
            "controller_type" : c,
            "description" : "(" + v + ") Autogenerated bindings for " + c,
            "name" : "(" + v + ") " + c
        }
        
        controller["bindings"]["/actions/default"]["skeleton"].append({"output" : "/actions/default/in/LeftHand", "path" : "/user/hand/left/input/skeleton/left"})
        controller["bindings"]["/actions/default"]["skeleton"].append({"output" : "/actions/default/in/RightHand", "path" : "/user/hand/right/input/skeleton/right"})
        
        for p in poses:
            controller["bindings"]["/actions/default"]["poses"].append({"output" : "/actions/default/in/Left"+p, "path" : "/user/hand/left/pose/"+poses[p]});
            controller["bindings"]["/actions/default"]["poses"].append({"output" : "/actions/default/in/Right"+p, "path" : "/user/hand/right/pose/"+poses[p]});
        
        for binding in bindings:
            b = bindings[binding]
            
            parameters = {}
            
            mode = "button"
            
            inputs = b["b"].split("|")
            
            inputtype = "click"
            
            finalhand = b["h"]
            
            if invert and b["f"] == True:
                if finalhand == "left":
                    finalhand = "right"
                else:
                    finalhand = "left"
            
            if inputs[0] == "joystick":
                if c == "knuckles":
                    inputs[0] = "thumbstick"
            
                if len(inputs) > 1:
                    mode = "dpad"
                    parameters["sub_mode"] = "touch"
                    inputtype = inputs[1]
                    
                    needsMerge = False
                    
                    for entry in controller["bindings"]["/actions/default"]["sources"]:
                        if entry["mode"] == mode and entry["path"] == "/user/hand/" + finalhand + "/input/" + inputs[0]:
                            needsMerge = True
                            break
                    
                    if needsMerge:
                        entry["inputs"][inputtype] = {"output" : "/actions/default/in/" + binding}
                        continue
                else:
                    mode = "joystick"
                    inputtype = "position"
            elif inputs[0] == "grip":
                parameters["click_activate_threshold"] = 0.8
                parameters["click_deactivate_threshold"] = 0.7
            elif inputs[0] == "x":
                if c == "knuckles":
                    inputs[0] = "a"
            elif inputs[0] == "y":
                if c == "knuckles":
                    inputs[0] = "b"
            elif inputs[0] == "thumbrest":
                if c == "knuckles":
                    inputs[0] = "trackpad"
            
                       
            input = {}
            input[inputtype] = {"output" : "/actions/default/in/" + binding}
            
            finalinput = inputs[0]
            
            if invert and b["f"] == True and c in swapmap and finalinput in swapmap[c]:
                finalinput = swapmap[c][finalinput]

            
            controller["bindings"]["/actions/default"]["sources"].append({"inputs" : input, "mode" : mode, "path" : "/user/hand/" + finalhand + "/input/" + finalinput, "parameters" : parameters})
        
        try:
            with open(filename+".json", "w") as f:
                f.write(json.dumps(controller, indent=4))
        except:
            print ("failed to create " + filename + ".json")
        else:
            print ("successfully created " + filename + ".json")
            


































