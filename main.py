from maker import Maker, Recipe, Player, Actions


if __name__ == '__main__':

    r = Recipe(name='Crimson Cider')
    r.update_fromdb()

    m = Maker(recipe=r, player=Player(80, 1500, 1350, 300))
    print(m.durability, m.progress, m.quality, m.player.cp)

    action_rotation = [
        Actions.NAME_OF_THE_ELEMENTS,
        Actions.CAREFUL_SYNTHESIS,
        Actions.BRAND_OF_THE_ELEMENTS,
        Actions.BASIC_TOUCH,
        Actions.BASIC_TOUCH,
        Actions.BASIC_TOUCH,
        Actions.BASIC_TOUCH,
        Actions.GROUNDWORK
    ]

    for action in action_rotation:
        getattr(m, action.value)()
