from .scripted_reach import ScriptedReach
from .scripted_grasp import ScriptedGraspV6

scripted_policies = dict()
scripted_policies['scripted_reach'] = ScriptedReach
scripted_policies['scripted_grasp_v6'] = ScriptedGraspV6
