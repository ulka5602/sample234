
"""
A model for how fire spread through a forest. Each 
'healthy' tree has the probability to cathc fire 
and will turn to 'burnt' out state. And then , all of its
neighours catch fire.
"""

import lib.actions as acts

from lib.display_methods import TOMATO, GREEN, RED, SPRINGGREEN, BLACK
from lib.model import Model, MBR_ACTION, NUM_MBRS, COLOR

MODEL_NAME = "forest_fire"

DEF_NUM_TREES = 10
DEF_DIM = 30
DEF_DENSITY = .44
DEF_NEW_FIRE = .01
# tree group names
HEALTHY = "Healthy"
NEW_FIRE = "New Fire"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

# state numbers: create as strings for JSON,
# convert to int when we need 'em that way
HE = "0"
NF = "1"
OF = "2"
BO = "3"
NG = "4"

TRANS_TABLE = "trans_table"
state_trans = [
    [1 - DEF_NEW_FIRE, DEF_NEW_FIRE, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, .99, .01],
    [1.0, 0.0, 0.0, 0.0, 0.0],
]

GRP_MAP = "group_map"

STATE_MAP = {HEALTHY: HE,
             NEW_FIRE: NF,
             ON_FIRE: OF,
             BURNED_OUT: BO,
             NEW_GROWTH: NG}

GRP_MAP = {HE: HEALTHY,
           NF: NEW_FIRE,
           OF: ON_FIRE,
           BO: BURNED_OUT,
           NG: NEW_GROWTH}


def tree_action(agent, **kwargs):
    """
    How should a tree change state?
    """
    old_group = agent.group_name()
    new_group = old_group  # for now!
    if old_group == HEALTHY:
        if acts.exists_neighbor(agent,
                                lambda agent: agent.group_name() == ON_FIRE):
            new_group = NEW_FIRE

    # if we didn't catch on fire above, do probabilistic transition:
    if old_group == new_group:
        curr_state = STATE_MAP[old_group]
        # we gotta do these str/int shenanigans with state cause
        # JSON only allows strings as dict keys
        new_group = GRP_MAP[str(acts.prob_state_trans(int(curr_state),
                                                      state_trans))]
        if acts.DEBUG.debug:
            if agent.group_name == NEW_FIRE:
                print("Tree spontaneously catching fire.")

    if old_group != new_group:
        if acts.DEBUG.debug:
            print(f"Add switch from {old_group} to {agent.group_name()}")
        acts.add_switch(agent, old_group, new_group)
    return acts.DONT_MOVE


ff_grps = {
    HEALTHY: {
        MBR_ACTION: tree_action,
        NUM_MBRS: DEF_NUM_TREES,
        COLOR: GREEN,
    },
    NEW_FIRE: {
        NUM_MBRS: 0,
        COLOR: TOMATO,
    },
    ON_FIRE: {
        NUM_MBRS: 0,
        COLOR: RED,
    },
    BURNED_OUT: {
        NUM_MBRS: 0,
        COLOR: BLACK,
    },
    NEW_GROWTH: {
        NUM_MBRS: 0,
        COLOR: SPRINGGREEN,
    },
}


class ForestFire(Model):
    """
    The forest fire model.
    """
    def handle_props(self, props):
        super().handle_props(props)
        density = self.get_prop("density", DEF_DENSITY)
        num_agents = int(self.height * self.width * density)
        self.grp_struct[HEALTHY]["num_mbrs"] = num_agents


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return ForestFire(serial_obj=serial_obj)
    else:
        return ForestFire(MODEL_NAME, grp_struct=ff_grps,
                          props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
