from enum import Enum
import re

DEFAULT_INPUT = 'day24.txt'

class Unit(Enum):
    IMMUNE = 1
    INFECTION = 2
    NEITHER = 3

class Group:
    current_id = 1
    
    def __init__(self, unit_type, units, health, weakness, immunity,
                 damage, dam_type, initiative):
        self.unit_type = unit_type
        self.units = units
        self.health = health
        self.weakness = weakness
        self.immunity = immunity
        self.damage = damage
        self.dam_type = dam_type
        self.initiative = initiative
        self.group_id = Group.current_id
        Group.current_id += 1

    @property
    def power(self):
        return self.units * self.damage

    def __repr__(self):
        return f'Group #{self.group_id}, type: {self.unit_type}'

    def damage_dealt(self, other):
        if self.dam_type in other.weakness:
            return self.power * 2
        elif self.dam_type in other.immunity:
            return 0
        else:
            return self.power

    def take_damage(self, amount):
        self.units -= amount // self.health

    def select_target(self, enemy_groups):
        if not enemy_groups:
            return None
        enemy_groups.sort(key=lambda g:g.initiative, reverse=True)
        enemy_groups.sort(key=lambda g:g.power, reverse=True)
        enemy_groups.sort(key=lambda g:self.damage_dealt(g), reverse=True)
        if self.damage_dealt(enemy_groups[0]) == 0:
            return None
        return enemy_groups[0]

class Combat:
    def __init__(self, immune, infection):
        self.immune = immune
        self.infection = infection

    def __repr__(self):
        return f'Combat with {len(self.immune)} immune groups and ' + \
               f'{len(self.infection)} infection groups'

    def trim(self):
        self.immune = [group for group in self.immune if group.units > 0]
        self.infection = [group for group in self.infection if group.units > 0]

    def combat_over(self):
        return len(self.immune) == 0 or len(self.infection) == 0

    def total_size(self):
        return sum(group.units for group in self.immune + self.infection)

    def tick(self):
        prev_size = self.total_size()
        if self.combat_over():
            if self.immune:
                return Unit.IMMUNE, sum(group.units for group in self.immune)
            else:
                return Unit.INFECTION, sum(group.units for group in self.infection)
        action_list = self.determine_actions()
        self.take_actions(action_list)
        if self.total_size() == prev_size:
            return Unit.NEITHER, None
        self.trim()
        return None

    def determine_actions(self):
        action_list = []
        chosen = set()
        self.immune.sort(key=lambda g:g.initiative, reverse=True)
        self.immune.sort(key=lambda g:g.power, reverse=True)
        for group in self.immune:
            chosen_target = group.select_target([g for g in self.infection if g.group_id not in chosen])
            if chosen_target is not None:
                action_list.append((group, chosen_target))
                chosen.add(chosen_target.group_id)
        self.infection.sort(key=lambda g:g.initiative, reverse=True)
        self.infection.sort(key=lambda g:g.power, reverse=True)
        for group in self.infection:
            chosen_target = group.select_target([g for g in self.immune if g.group_id not in chosen])
            if chosen_target is not None:
                action_list.append((group, chosen_target))
                chosen.add(chosen_target.group_id)
        return action_list

    def take_actions(self, action_list):
        action_list.sort(key=lambda t:t[0].initiative, reverse=True)
        for attacker, defender in action_list:
            if attacker.units > 0:
                damage_dealt = attacker.damage_dealt(defender)
                defender.take_damage(damage_dealt)
                

def day_24(loc=DEFAULT_INPUT):
    with open(loc) as f:
        all_as_string = ''.join(f.readlines()).rstrip()
    immune, infect = all_as_string.split('\n\n')
    immune_lines = immune.split('\n')[1:]
    infect_lines = infect.split('\n')[1:]
    default_result = evaluate_combat(immune_lines, infect_lines)
    boost = 2
    even_immune_victory = False
    while not even_immune_victory:
        even_result = evaluate_combat(immune_lines, infect_lines, boost)
        if even_result[0] is Unit.IMMUNE:
            even_immune_victory = True
        else:
            boost += 2
    odd_result = evaluate_combat(immune_lines, infect_lines, boost - 1)
    if odd_result[0] is Unit.IMMUNE:
        return default_result[1], odd_result[1]
    else:
        return default_result[1], even_result[1]


def evaluate_combat(immune_lines, infect_lines, boost=0):
    pattern = re.compile(r'(?P<units>\d+) units each with (?P<health>\d+) ' +\
                         r'hit points (?P<weakimmune>\(.+\) )?with an attack ' +\
                         r'that does (?P<damage>\d+) (?P<dam_type>\w+) damage ' +\
                         r'at initiative (?P<initiative>\d+)')
    immune_groups = []
    infect_groups = []
    for line in immune_lines:
        m = pattern.match(line)
        units = int(m.group('units'))
        health = int(m.group('health'))
        damage = int(m.group('damage')) + boost
        dam_type = m.group('dam_type')
        initiative = int(m.group('initiative'))
        weak, immune = [], []
        if m.group('weakimmune') is not None:
            wi = m.group('weakimmune')[1:-2]
            if ';' in wi:
                if wi[0] == 'w':
                    w, i = wi.split('; ')
                else:
                    i, w = wi.split('; ')
                weak = w.split('to ')[1].split(', ')
                immune = i.split('to ')[1].split(', ')
            elif wi[0] == 'w':
                weak = wi.split('to ')[1].split(', ')
            else:
                immune = wi.split('to ')[1].split(', ')
        g = Group(Unit.IMMUNE, units, health, weak, immune,
                  damage, dam_type, initiative)
        immune_groups.append(g)
    for line in infect_lines:
        m = pattern.match(line)
        units = int(m.group('units'))
        health = int(m.group('health'))
        damage = int(m.group('damage'))
        dam_type = m.group('dam_type')
        initiative = int(m.group('initiative'))
        weak, immune = [], []
        if m.group('weakimmune') is not None:
            wi = m.group('weakimmune')[1:-2]
            if ';' in wi:
                if wi[0] == 'w':
                    w, i = wi.split('; ')
                else:
                    i, w = wi.split('; ')
                weak = w.split('to ')[1].split(', ')
                immune = i.split('to ')[1].split(', ')
            elif wi[0] == 'w':
                weak = wi.split('to ')[1].split(', ')
            else:
                immune = wi.split('to ')[1].split(', ')
        g = Group(Unit.INFECTION, units, health, weak, immune,
                  damage, dam_type, initiative)
        infect_groups.append(g)
    combat = Combat(immune_groups, infect_groups)
    result = None
    while result is None:
        result = combat.tick()
    return result
    

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_24()))
   

