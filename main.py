from maker import Maker, Recipe, Player, Actions


if __name__ == '__main__':

    r = Recipe(name='Crimson Cider')
    r.update_fromdb()

    m = Maker(recipe=r, player=Player(80, 1500, 1350, 300))
    print(m.step, m.durability, m.progress, m.quality, m.player.cp)

    action_rotation = [
        Actions.REFLECT,
        Actions.GREAT_STRIDES,
        Actions.INNOVATION,
        Actions.OBSERVE,
        Actions.BASIC_TOUCH,
        Actions.STANDARD_TOUCH,
        Actions.PREPARATORY_TOUCH,
        Actions.BYREGOTS_BLESSING,
        # Actions.CAREFUL_SYNTHESIS,
        # Actions.VENERATION,
        # Actions.GROUNDWORK
    ]

    for action in action_rotation:
        getattr(m, action.value)()
