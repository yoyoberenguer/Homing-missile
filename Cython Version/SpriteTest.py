import pygame

from SPRITES import Sprite, AbstractGroup, Group, GroupSingle, \
    collide_rect, collide_rect_ratio, collide_circle, collide_circle_ratio, spritecollide, groupcollide
import timeit
import random


class dumbclass(object):
    b = 10


if __name__ == '__main__':

    N = 100
    x = 1024
    y = 768
    screen = pygame.Surface((x, y))
    bck = pygame.Surface((100, 100))

    # TESTING SPRITE
    # INSTANTIATION WITH NO GROUP PASSED AS ARGUMENT
    print('---- TESTING SPRITE ----')
    s = Sprite()
    assert hasattr(s, 'groups'), '\nSprite class missing groups method!.'
    assert hasattr(s, '__g'), '\nSprite class missing __g class variable!.'
    print('Variable __g', s.__g)
    assert isinstance(s.__g, dict), '\n __g must be a python dict got %s ' % type(s.__g)
    assert len(s.__g) == 0, '\n __g must be null got %s ' % len(s.__g)
    assert hasattr(s, '__dict__'), '\nSprite class missing __dict__ .'
    # GROUPS TESTING
    s.groups()

    # INSTANTIATION WITH A GROUP PASSED AS ARGUMENT
    g = Group()
    s = Sprite()
    assert hasattr(s, 'add'), '\nSprite class missing add method!.'
    s.add(g)

    # sprite s should be in the group g
    assert len(s.groups()) == 1, '\nSprite should be in the group g!'
    assert hasattr(s, 'alive'), '\nSprite class missing alive method!.'
    assert s.alive() is True, '\nSprite should be alive!'
    assert hasattr(s, '__g'), '\nSprite class missing __g variable!.'
    print(s.__g.keys(), s.__g.values())
    assert hasattr(s, 'update'), '\nSprite class missing update method!.'
    assert hasattr(s, 'remove'), '\nSprite class missing remove method!.'
    # remove the sprite from group
    s.remove(g)
    assert s.alive() is False, '\nSprite should be alive!'
    print(s.__g)
    print(s.groups())
    assert hasattr(s, 'kill'), '\nSprite class missing kill method!.'
    s.kill()

    s.add(g)
    s.kill()
    print(s.__g)
    print(s.groups())
    assert s.alive() is False, '\nSprite should be alive!'

    g = Group()
    g1 = Group()
    s = Sprite()
    s.add((g, g1))
    print(s.__g)
    print(s.groups())
    s.kill()
    assert s.alive() is False, '\nSprite should be killed'
    print(s.__g)
    assert len(s.groups()) == 0, '\nSprite has no groups!'

    print('Sprite groups() method : ',
          timeit.timeit('s.groups()', 'from __main__ import s', number=N))
    print('Sprite add() method    : ',
          timeit.timeit('s.add()', 'from __main__ import s', number=N))
    print('Sprite alive() method  : ',
          timeit.timeit('s.alive()', 'from __main__ import s', number=N))
    print('Sprite update() method : ',
          timeit.timeit('s.update()', 'from __main__ import s', number=N))
    print('Sprite remove() method : ',
          timeit.timeit('s.remove()', 'from __main__ import s', number=N))
    print('Sprite kill() method   : ',
          timeit.timeit('s.kill()', 'from __main__ import s', number=N))

    print('---- TESTING AbstractGroup ----')

    g = AbstractGroup()
    assert hasattr(g, '_spritegroup') and hasattr(g, 'spritedict') \
           and hasattr(g, 'lostsprites'), '\nAbstractGroup is missing class attributes!'
    assert isinstance(g._spritegroup, bool), '\n_spritegroup should be boolean!'
    assert isinstance(g.spritedict, dict), '\n spritedict should be dict!'
    assert isinstance(g.lostsprites, list), '\nlostsprite should be a list!'
    s = Sprite()
    print('** ADD SPRITE')
    assert hasattr(g, 'add'), '\nGroup class missing add method!.'
    g.add(s)
    print('spritedict ', g.spritedict)
    print('_spritegroup ', g._spritegroup)
    print('lostsprites ', g.lostsprites)
    assert len(g.spritedict) == 1, '\n Sprite should be in the group!'
    assert hasattr(g, 'has'), '\nGroup class missing has method!.'
    assert g.has(s) is True, '\nSprite should be in the group !'
    assert hasattr(g, 'sprites'), '\nGroup class missing sprites method!.'
    print(g.sprites())

    print('** DELETE SPRITE')
    assert hasattr(g, 'remove'), '\nGroup class missing remove method!.'
    g.remove(s)
    print('spritedict ', g.spritedict)
    print('_spritegroup ', g._spritegroup)
    print('lostsprites ', g.lostsprites)
    print(g.sprites())
    assert len(g.spritedict) == 0, '\n Sprite should be in no group!'
    assert hasattr(s, 'alive'), '\nGroup class missing alive method!.'
    assert s.alive() is False, '\n Sprite should be killed!'
    assert hasattr(g, 'has'), '\nGroup class missing has method!.'
    assert g.has(s) is False, '\nSprite should be removed !'

    print('** TIMING WITH AN EMPTY GROUP')
    print('Group sprites() method : ',
          timeit.timeit('g.sprites()', 'from __main__ import g', number=N))
    print('Group add() method : ',
          timeit.timeit('g.add(s)', 'from __main__ import s, g', number=N))
    print('Group has() method : ',
          timeit.timeit('g.has(s)', 'from __main__ import s, g', number=N))
    print('Group remove(s) method : ',
          timeit.timeit('g.remove(s)', 'from __main__ import s, g', number=N))
    print('Group update(s) method : ',
          timeit.timeit('g.update(s)', 'from __main__ import s, g', number=N))
    print('Group copy() method : ',
          timeit.timeit('g.copy()', 'from __main__ import g', number=N))
    print('Group draw(SCREEN) method : ',
          timeit.timeit('g.draw(SCREEN)', 'from __main__ import SCREEN, g', number=N))
    print('Group empty() method : ',
          timeit.timeit('g.empty()', 'from __main__ import  g', number=N))
    print('Group clear() method : ',
          timeit.timeit('g.clear(SCREEN, bck)', 'from __main__ import  SCREEN, bck, g', number=N))

    s = [Sprite() for r in range(N)]
    for i in s:
        i.image = pygame.Surface((random.randint(5, x), random.randint(5, y)))
        i.rect = i.image.get_rect()

    g.empty()
    g.add(s)
    assert len(g) == N, '\nMissing sprite in group'

    print('** TIMING WITH A LOADED GROUP')
    print('Group sprites() method : ',
          timeit.timeit('g.sprites()', 'from __main__ import g', number=N))
    print('Group add() method : ',
          timeit.timeit('g.add(s)', 'from __main__ import s, g', number=N))
    print('Group has() method : ',
          timeit.timeit('g.has(s)', 'from __main__ import s, g', number=N))

    print('Group update(s) method : ',
          timeit.timeit('g.update(s)', 'from __main__ import s, g', number=N))
    print('Group copy() method : ',
          timeit.timeit('g.copy()', 'from __main__ import g', number=N))
    print(len(g.spritedict))
    print('Group draw(SCREEN) method : ',
          timeit.timeit('g.draw(SCREEN)', 'from __main__ import SCREEN, g', number=N))
    g.draw(screen)
    print('Group clear() method : ',
          timeit.timeit('g.clear(SCREEN, bck)', 'from __main__ import  SCREEN, bck, g', number=N))
    print('Group remove(s) method : ',
          timeit.timeit('g.remove(s)', 'from __main__ import s, g', number=N))
    print('Group empty() method : ',
          timeit.timeit('g.empty()', 'from __main__ import  g', number=N))

    s = Sprite()
    print('sprite id : ', id(s))
    g = GroupSingle(g)
    print('GroupSingle add method : ')
    g.add(s)
    print('GroupSingle has method : ', g.has(s))
    assert g.has(s) is True, '\nGroup g missing sprite s'
    print('s in g', s in g)
    assert (s in g) is True, '\nGroup must contains sprite s'
    print('g.__sprite : ', hasattr(g, '__sprite'))
    print('GroupSingle sprites() method   : ', g.sprites())
    print('GroupSingle _get_sprite method : ', id(g._get_sprite()))
    print('GroupSingle _set_sprite method : ', g._set_sprite(s))
    print('GroupSingle _get_sprite method : ', id(g._get_sprite()))
    print(len(g), s.alive(), s.groups(), g.spritedict)
    print('GroupSingle has_internal method : ', g.has_internal(s))
    assert g.has_internal(s) is True, '\nGroup should contain sprite s'
    f = g.copy()
    assert g == g, '\nCopy not equal '
    assert s in f, '\nSprite s should be in copy'
    print(f.sprites())
    for sprite in f:
        print(id(sprite))
    print(s.groups)
    s.kill()
    print(len(g), s.alive(), s.groups(), g.spritedict)

    s = Sprite()
    g = GroupSingle(s)
    print('ADD ', len(g), s.alive(), s.groups(), g.spritedict)

    g.remove(s)
    assert len(g) == 0, '\nGroup g is not empty'
    print('REMOVE ', len(g), s.alive(), s.groups(), g.spritedict)

    sprite1 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2 = Sprite()
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))

    assert bool(collide_rect(sprite1, sprite2)) is True, 'Both sprites should collide'
    sprite2.rect.center = (91, 91)
    rect1 = sprite1.rect
    rect2 = sprite2.rect
    import math

    distance = math.sqrt((rect1.x - rect2.x) ** 2 + (rect1.y - rect2.y) ** 2)
    print("collide_rect SPRITE : ", distance, collide_rect(sprite1, sprite2))
    print("Collide_rect pygame : ", pygame.sprite.collide_rect(sprite1, sprite2))

    print('collide_rect_ratio')
    # collide_rect_ratio
    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (81, 81)
    print("Collide rect_ratio SPRITE : ", collide_rect_ratio(2.0)(sprite1, sprite2))

    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (81, 81)
    print("Collide rect_ratio pygame :", pygame.sprite.collide_rect_ratio(2.0)(sprite1, sprite2))

    # collide_circle
    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (89, 90)
    print("Collide collide_circle SPRITE : ", collide_circle(sprite1, sprite2))
    print(timeit.timeit("collide_circle(sprite1, sprite2)",
                        "from __main__ import collide_circle, sprite1, sprite2", number=100000))

    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (89, 90)
    print("Collide collide_circle pygame : ", pygame.sprite.collide_circle(sprite1, sprite2))
    print(timeit.timeit("pygame.sprite.collide_circle(sprite1, sprite2)",
                        "from __main__ import pygame, sprite1, sprite2", number=100000))

    # collide_circle_ratio
    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (90, 90)
    print("Collide collide_circle_ratio SPRITE : ", collide_circle_ratio(1.0)(sprite1, sprite2))
    print(timeit.timeit("collide_circle_ratio(1.0)(sprite1, sprite2)",
                        "from __main__ import collide_circle_ratio, sprite1, sprite2", number=100000))

    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (90, 90)
    print("Collide collide_circle_ratio pygame : ", pygame.sprite.collide_circle_ratio(1.0)(sprite1, sprite2))
    print(timeit.timeit("pygame.sprite.collide_circle_ratio(1.0)(sprite1, sprite2)",
                        "from __main__ import pygame, sprite1, sprite2", number=100000))

    # todo SPRITE MASK TEST

    # spritecollide
    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite3 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (91, 91)
    g = Group()
    g.add(sprite2)
    sprite3.image = pygame.Surface((10, 10))
    sprite3.rect = sprite3.image.get_rect(center=(500, 500))
    g.add(sprite3)
    print('SPRITECOLLIDE SPRITE : ', timeit.timeit("spritecollide(sprite1, g, False, None)",
                                                   "from __main__ import spritecollide, sprite1, g", number=100000))
    r = spritecollide(sprite1, g, dokill=False, collided=None)
    for i in r:
        print(i, i.groups(), i.alive())

    sprite1 = pygame.sprite.Sprite()
    sprite2 = pygame.sprite.Sprite()
    sprite3 = pygame.sprite.Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (91, 91)
    g = pygame.sprite.Group()
    g.add(sprite2)
    sprite3.image = pygame.Surface((10, 10))
    sprite3.rect = sprite3.image.get_rect(center=(500, 500))
    g.add(sprite3)
    print('SPRITECOLLIDE PYGAME : ', timeit.timeit("pygame.sprite.spritecollide(sprite1, g, False, None)",
                                                   "from __main__ import pygame, sprite1, g", number=100000))
    r = pygame.sprite.spritecollide(sprite1, g, dokill=False, collided=None)
    for i in r:
        print(i, i.groups(), i.alive())

    # groupcollide
    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite3 = Sprite()
    sprite4 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (91, 91)
    g = Group()
    g.add(sprite2)
    sprite3.image = pygame.Surface((10, 10))
    sprite3.rect = sprite3.image.get_rect(center=(500, 500))
    sprite4.image = pygame.Surface((10, 10))
    sprite4.rect = sprite3.image.get_rect(center=(480, 650))
    g1 = Group()
    g1.add(sprite1, sprite4)
    g.add(sprite3)
    print('GROUPCOLLIDE SPRITE : ', timeit.timeit("groupcollide(g, g1, False, False, None)",
                                                  "from __main__ import groupcollide, g, g1", number=100000))
    r = groupcollide(g, g1, False, False, None)
    for i in r:
        print(i, i.groups(), i.alive())

    sprite1 = Sprite()
    sprite2 = Sprite()
    sprite3 = Sprite()
    sprite4 = Sprite()
    sprite1.image = pygame.Surface((10, 10))
    sprite1.rect = sprite1.image.get_rect(center=(100, 100))
    sprite2.image = pygame.Surface((10, 10))
    sprite2.rect = sprite2.image.get_rect(center=(100, 100))
    sprite2.rect.center = (91, 91)
    g = Group()
    g.add(sprite2)
    sprite3.image = pygame.Surface((10, 10))
    sprite3.rect = sprite3.image.get_rect(center=(500, 500))
    sprite4.image = pygame.Surface((10, 10))
    sprite4.rect = sprite3.image.get_rect(center=(480, 650))
    g1 = Group()
    g1.add(sprite1, sprite4)
    g.add(sprite3)
    print('GROUPCOLLIDE PYGAME : ', timeit.timeit("pygame.sprite.groupcollide(g, g1, False, False, None)",
                                                  "from __main__ import pygame, g, g1", number=100000))
    r = pygame.sprite.groupcollide(g, g1, False, False, None)
    for i in r:
        print(i, i.groups(), i.alive())
