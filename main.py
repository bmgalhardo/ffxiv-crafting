from maker import Maker, Recipe, Player, Actions


if __name__ == '__main__':

    r = Recipe(name='Crimson Cider')
    r.update_fromdb()

    p = Player(80, 1500, 1350, 300)
    m = Maker(recipe=r, player=p)
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
    print(p.available_actions())
    p.check_rotation(action_rotation)

    for action in action_rotation:
        getattr(m, action.value.function)()
