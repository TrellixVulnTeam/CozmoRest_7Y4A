
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

from cozmo.util import degrees, distance_mm, speed_mmps, Pose
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

import cozmo
import time
import logging
import json
import sys


robot = None

def abort_actions(sdk_conn):
    robot = sdk_conn.wait_for_robot()
    robot.abort_all_actions()


# FUNCTION: ROBOT TO SAY A TEXT

text_to_say = "Una cervecita, por favor"

def say(sdk_conn):
    print("COZMO TO SAY")
    robot = sdk_conn.wait_for_robot()
    robot.say_text(text_to_say, in_parallel=True).wait_for_completed()

# FUNCTION: ROBOT TO MOVE FORWARD DURING "distance_to_go" miliseconds WITH SPEED "speed_to_go"

distance_to_go = 500
speed_to_go = 50

def go(sdk_conn):
    print("COZMO TO GO")
    robot = sdk_conn.wait_for_robot()
    robot.drive_straight(distance_mm(distance_to_go), speed_mmps(speed_to_go), in_parallel=True).wait_for_completed()

# FUNCTION: ROBOT TO TURN "degrees_to_turn" DEGREES

degrees_to_turn = 90

def turn(sdk_conn):
    print("ROTATE COZMO")
    robot = sdk_conn.wait_for_robot()
    try:
        robot.turn_in_place(degrees(int(degrees_to_turn)), in_parallel=True).wait_for_completed()
    except:
        print(sys.exc_info()[0])

# FUNCTION: ROBOT TO MOVE HIS HEAD "degrees_for_head" DEGREES

degrees_for_head = -5

def move_robot_head(sdk_conn):
    print("MOVE COZMO HEAD")
    robot = sdk_conn.wait_for_robot()
    try:
        robot.set_head_angle(degrees(int(degrees_for_head)), in_parallel=True).wait_for_completed()
    except:
        print(sys.exc_info()[0])

# FUNCTION: ROBOT TO TURN ON BACKPACK LIGHTS IN COLOR "backpack_color" DURING "time_for_lights" SECONDS

backpack_color = "RED"
time_for_lights = 2

def set_backpack_color(sdk_conn):
    print("Seting backpack lights")
    robot = sdk_conn.wait_for_robot()
    if backpack_color == "RED":
        print("Seting backpack lights to RED")
        robot.set_all_backpack_lights(cozmo.lights.red_light)
        time.sleep(int(time_for_lights))
    elif backpack_color == "GREEN":
        print("Seting backpack lights to GREEN")
        robot.set_all_backpack_lights(cozmo.lights.green_light)
        time.sleep(int(time_for_lights))
    elif backpack_color == "BLUE":
        print("Seting backpack lights to BLUE")
        robot.set_all_backpack_lights(cozmo.lights.blue_light)
        time.sleep(int(time_for_lights))
    elif backpack_color == "WHITE":
        print("Seting backpack lights to WHITE")
        robot.set_center_backpack_lights(cozmo.lights.white_light)
        time.sleep(int(time_for_lights))
    else:
        print("Seting backpack lights OFF")
        robot.set_all_backpack_lights(cozmo.lights.off_light)
        time.sleep(int(time_for_lights))

# FUNCTION: ROBOT TO PLAY AN ANIMATION

animation_id = "CubePounceLoseSession"

def play_animation(sdk_conn):
    print("PLAYING ANIMATION")
    animation_string="cozmo.anim.Triggers." + animation_id
    print(animation_string)
    robot = sdk_conn.wait_for_robot()
    robot.play_anim_trigger(animation_string + animation_id).wait_for_completed()

# FUNCTION: TURN ON THE LIGHT FOR CUBE "cube_id" IN COLOR "color_cube" DURING "color_cube_time" SECONDS

cube_id = 1
color_cube = "RED"
color_cube_time = 10

def set_cube_lights(sdk_conn):
    print("SETTING CUBE LIGHTS")
    robot = sdk_conn.wait_for_robot()
    if cube_id == "1":
        cube = robot.world.get_light_cube(LightCube1Id)
    elif cube_id == "2":
        cube = robot.world.get_light_cube(LightCube2Id)
    else:
        cube = robot.world.get_light_cube(LightCube3Id)

    if color_cube == "RED":
        cube.set_lights(cozmo.lights.red_light)
        time.sleep(int(color_cube_time))
    elif color_cube == "BLUE":
        cube.set_lights(cozmo.lights.blue_light)
        time.sleep(int(color_cube_time))
    else:
        cube.set_lights(cozmo.lights.green_light)
        time.sleep(int(color_cube_time))

# FUNCTION: ROBOT TO MOVE HIS LIFT "lift_degrees" DEGREES

lift_degrees = "-3"

def move_cozmo_lift(sdk_conn):
    print("MOVING COZMO LIFT")
    robot = sdk_conn.wait_for_robot()
    robot.move_lift(lift_degrees).wait_for_completed()

# FUNCTION: ROBOT GO TO "AXIS-X, AXIS-Y, RETRY, ROTATION_ANGLE" FROM CURRENT POSITION

go_to_axis_x = 1000
go_to_axis_y = 1000
go_to_retry = 0
go_to_rotation_angle = 45

def cozmo_go_to_pose(sdk_conn):
    print("SENDING COZMO TO POSE")
    robot = sdk_conn.wait_for_robot()
    robot.go_to_pose(Pose(1000, 2000, 0, angle_z=degrees(45)), relative_to_robot=True).wait_for_completed()

# ----------------------------
# FUNCTION: ROBOT GO TO OBJECT
# ----------------------------

cube_to_go = 1

def cozmo_go_to_object(sdk_conn):
    print("SENDING COZMO TO OBJECT %s" % cube_to_go)
    robot = sdk_conn.wait_for_robot()

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()

    cube_detination = None

    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()

    if len(cubes) < 1:
        print("Error: Cube not found")
    else:
        for cube in cubes:
            print ("Comparing cubes: %s" % cube.object_id)
            if (str(cube.object_id) == str(cube_to_go)):
                cube_detination = cube
                print ("CUBE FOUND!")
    if cube_detination:
        # Drive to 70mm away from the cube (much closer and Cozmo
        # will likely hit the cube) and then stop.
        cube_detination.set_lights(cozmo.lights.green_light)
        action = robot.go_to_object(cube_detination, distance_mm(70.0))
        action.wait_for_completed()
        print("Completed action: result = %s" % action)
        print("Done.")
    else:
        print ("CUBE NOT FOUND!!!!")

# -----------------------------
# FUNTION: ROBOT TO FIND A CUBE
#------------------------------

cube_to_find = 1

def find_cube(cube_number, robot):
    print("SEARCHING CUBE %s" % cube_number)

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()

    # Lookaround until Cozmo knows where at least 2 cubes are:
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=30)
    lookaround.stop()

    if len(cubes) < 1:
        print ("CUBE NOT FOUND")
        robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()
        return None
    else:
        cube_found = None
        for cube in cubes:
            if (str(cube.object_id) == str(cube_number)):
                cube_found = cube

    if cube_found:
        return cube_found
    else:
        print ("CUBE NOT FOUND")
        robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()
        return None

# -----------------------------
# FUNTION: ROBOT TO PICKUP CUBE
#------------------------------

cube_to_pickup = 1

def cozmo_pickup_cube(sdk_conn):
    print("COZMO TO PICKUP CUBE")
    robot = sdk_conn.wait_for_robot()

    cube_found = find_cube(cube_to_pickup, robot)
    if cube_found:
        print ("CUBE FOUND!!")
        cube_found.set_lights(cozmo.lights.green_light.flash())
        anim = robot.play_anim_trigger(cozmo.anim.Triggers.BlockReact)
        anim.wait_for_completed()

        action = robot.pickup_object(cube_found)
        print("got action", action)
        result = action.wait_for_completed(timeout=30)
        print("got action result", result)

        robot.turn_in_place(degrees(90)).wait_for_completed()

        action = robot.place_object_on_ground_here(cube_found)
        print("got action", action)
        result = action.wait_for_completed(timeout=30)
        print("got action result", result)

        anim = robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin)
        cube_found.set_light_corners(None, None, None, None)
        anim.wait_for_completed()
    else:
        print ("CUBE NOT Found")









# ---------------------------------
# FUNTION: ROBOT TO STACK TWO CUBES
#----------------------------------

cube_up = 1
cube_down = 2

def stack_cubes(sdk_conn):
    print("COZMO TRYING TO STACK TWO CUBES")
    robot = sdk_conn.wait_for_robot()

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()

    # Lookaround until Cozmo knows where at least 2 cubes are:
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()

    if len(cubes) < 2:
        print("Error: need 2 Cubes but only found", len(cubes), "Cube(s)")
    else:
        cube_to_up = None
        cube_to_down = None
        for cube in cubes:
            if (str(cube.object_id) == str(cube_up)):
                cube_to_up = cube
            elif (str(cube.object_id) == str(cube_down)):
                cube_to_down = cube

        if (cube_to_up and cube_to_down):
            # cube_to_up.set_lights(cozmo.lights.red_light)
            current_action = robot.pickup_object(cube_to_up, num_retries=3)
            current_action.wait_for_completed()
            if current_action.has_failed:
                code, reason = current_action.failure_reason
                result = current_action.result
                print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                return

            # cube_to_down.set_lights(cozmo.lights.green_light)
            current_action = robot.place_on_object(cube_to_down, num_retries=3)
            current_action.wait_for_completed()
            if current_action.has_failed:
                code, reason = current_action.failure_reason
                result = current_action.result
                print("Place On Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                return

        else:
            print ("CUBES ARE NOT AVAILABLE")
            robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()

        print("Cozmo successfully stacked 2 blocks!")

# TO RENAME IN MY NEW ENVIRONMENT
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        # Abrimos la conexión con Cozmo
        cozmo.setup_basic_logging()
        # Leemos los comandos, los parámetros y ejecutamos la orden.
        data = JSONParser().parse(request)
        print(data)

        try:
            for x in data['commands']:
                print(x['command'])
                if x['command'] == "GO":
                    print(x['params'][0]['speed'])
                    print(x['params'][1]['duration'])
                    global distance_to_go
                    global speed_to_go
                    distance_to_go = x['params'][1]['duration']
                    speed_to_go = x['params'][0]['speed']
                    try:
                        cozmo.connect(go, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "SPEAK":
                    print(x['params'][0]['text'])
                    global text_to_say
                    text_to_say = x['params'][0]['text']
                    try:
                        cozmo.connect(say, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "TURN":
                    print(x['params'][0]['degrees'])
                    global degrees_to_turn
                    degrees_to_turn = x['params'][0]['degrees']
                    try:
                        cozmo.connect(turn, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "MOVE_HEAD":
                    print(x['params'][0]['degrees'])
                    global degrees_for_head
                    degrees_for_head = x['params'][0]['degrees']
                    try:
                        cozmo.connect(move_robot_head, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "SET_BACKPACK_LIGHTS":
                    print(x['params'][0]['color'])
                    global backpack_color
                    global time_for_lights
                    backpack_color = x['params'][0]['color']
                    time_for_lights = x['params'][1]['tiempo']
                    try:
                        cozmo.connect(set_backpack_color, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "ANIMATION":
                    print(x['params'][0]['ANIMATION_ID'])
                    global animation_id
                    animation_id = x['params'][0]['ANIMATION_ID']
                    try:
                        cozmo.connect(play_animation, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "SET_CUBE_LIGHTS":
                    print(x['params'][0]['CUBE_ID'])
                    print(x['params'][1]['COLOR'])
                    print(x['params'][2]['TIME'])
                    global cube_id
                    global color_cube
                    global color_cube_time
                    cube_id = x['params'][0]['CUBE_ID']
                    color_cube = x['params'][1]['COLOR']
                    color_cube_time = x['params'][2]['TIME']
                    try:
                        cozmo.connect(set_cube_lights, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "MOVE_LIFT":
                    print(x['params'][0]['degrees'])
                    global lift_degrees
                    lift_degrees = x['params'][0]['degrees']
                    try:
                        cozmo.connect(move_cozmo_lift, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "GO_TO_POSE":
                    print(x['params'][0]['AXIS-X'])
                    print(x['params'][1]['AXIS-Y'])
                    print(x['params'][2]['RETRIES'])
                    print(x['params'][3]['ANGLE'])
                    global go_to_axis_x
                    global go_to_axis_y
                    global go_to_retry
                    global go_to_rotation_angle
                    go_to_axis_x = x['params'][0]['AXIS-X']
                    go_to_axis_y = x['params'][1]['AXIS-Y']
                    go_to_retry = x['params'][2]['RETRIES']
                    go_to_rotation_angle = x['params'][3]['ANGLE']
                    try:
                        cozmo.connect(cozmo_go_to_pose, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "GO_TO_CUBE":
                    print(x['params'][0]['CUBE'])
                    global cube_to_go
                    cube_to_go = x['params'][0]['CUBE']
                    try:
                        cozmo.connect(cozmo_go_to_object, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "CUBE_STACK":
                    print(x['params'][0]['CUBE_UP'])
                    print(x['params'][1]['CUBE_DOWN'])
                    global cube_up
                    global cube_down
                    cube_up = x['params'][0]['CUBE_UP']
                    cube_down = x['params'][1]['CUBE_DOWN']
                    try:
                        cozmo.connect(stack_cubes, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "ABORT_ACTIONS":
                    try:
                        cozmo.connect(abort_actions, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                elif x['command'] == "PICKUP_CUBE":
                    print(x['params'][0]['CUBE'])
                    print ("Step 1")
                    global pickup_cube
                    print ("Step 2")
                    pickup_cube = x['params'][0]['CUBE']
                    print ("Step 3")
                    try:
                        cozmo.connect(cozmo_pickup_cube, connector=cozmo.run.FirstAvailableConnector())
                    except cozmo.ConnectionError as e:
                        sys.exit("Connection Error: %s" % e)
                else :
                     print("UNKNOWN COMMAND")
        except (ValueError, KeyError, TypeError):
            print("JSON format error")

        # print(data["code"])
        # print(data["test"])

        # text_to_say = data["code"]
        return JsonResponse("texto completado", status=200, safe=False)

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
