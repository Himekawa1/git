# 问题3：检查双方是否存在稳定出场顺序（修正版）

import itertools

# 扩展历史数据
historical_data_extended = {
    ('A1', 'A2'): {('B1', 'B2'): (65, 58)},
    ('A2', 'A3'): {('B2', 'B3'): (42, 27)},
    ('A1', 'A3'): {('B1', 'B2'): (63, 61), ('B3', 'B5'): (21, 10)},
    ('A1', 'A4'): {('B2', 'B4'): (60, 57)},
    ('A1', 'A5'): {('B1', 'B5'): (60, 51)},
    ('A4', 'A5'): {('B3', 'B5'): (35, 32)},
    ('A2', 'A4'): {('B2', 'B4'): (34, 36)},
    ('A2', 'A5'): {('B3', 'B5'): (42, 28)},
    ('A3', 'A4'): {('B4', 'B5'): (21, 14), ('B3', 'B4'): (41, 41)},
    ('A1', 'A6'): {('B1', 'B3'): (37, 41)},
    ('A2', 'A6'): {('B2', 'B6'): (39, 46)},
    ('A3', 'A5'): {('B5', 'B6'): (59, 58)},
    ('A1', 'A5'): {('B1', 'B6'): (60, 54)},
    ('A5', 'A6'): {('B4', 'B5'): (39, 41)},
    ('A3', 'A4'): {('B4', 'B6'): (21, 14)},
}


def get_score_rate(my_pair, opp_pair):
    """获取得分率，没有历史数据的组合默认0.5"""
    my_pair_sorted = tuple(sorted(my_pair))
    opp_pair_sorted = tuple(sorted(opp_pair))

    if my_pair_sorted in historical_data_extended:
        if opp_pair_sorted in historical_data_extended[my_pair_sorted]:
            my_score, opp_score = historical_data_extended[my_pair_sorted][opp_pair_sorted]
            return my_score / (my_score + opp_score)

    return 0.5


def simulate_match(my_order, opp_order):
    """模拟比赛，返回我方得分和对方得分"""
    stage_pairs = [
        ((my_order[0], my_order[1]), (opp_order[0], opp_order[1])),
        ((my_order[1], my_order[2]), (opp_order[1], opp_order[2])),
        ((my_order[2], my_order[3]), (opp_order[2], opp_order[3])),
        ((my_order[3], my_order[4]), (opp_order[3], opp_order[4])),
        ((my_order[4], my_order[0]), (opp_order[4], opp_order[0]))
    ]

    my_total_score = 0
    opp_total_score = 0

    for my_pair, opp_pair in stage_pairs:
        win_rate = get_score_rate(my_pair, opp_pair)
        my_stage_score = 10 * win_rate
        opp_stage_score = 10 * (1 - win_rate)

        my_total_score += my_stage_score
        opp_total_score += opp_stage_score

        if my_total_score >= 50 or opp_total_score >= 50:
            break

    return my_total_score, opp_total_score


def does_A_win(my_order, opp_order):
    """判断我方是否获胜"""
    my_score, opp_score = simulate_match(my_order, opp_order)
    return my_score > opp_score


def does_B_win(my_order, opp_order):
    """判断对方是否获胜"""
    my_score, opp_score = simulate_match(my_order, opp_order)
    return opp_score > my_score


def check_stable_orders_for_both_sides():
    """检查双方是否存在稳定出场顺序"""

    # 所有选手
    my_all_players = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    opp_all_players = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']

    # 生成所有5人组合
    my_combinations = list(itertools.combinations(my_all_players, 5))
    opp_combinations = list(itertools.combinations(opp_all_players, 5))

    # 预计算所有顺序
    print("预计算所有顺序...")
    all_my_orders = []
    for my_comb in my_combinations:
        all_my_orders.extend(list(itertools.permutations(my_comb)))

    all_opp_orders = []
    for opp_comb in opp_combinations:
        all_opp_orders.extend(list(itertools.permutations(opp_comb)))

    print(f"我方总顺序数: {len(all_my_orders)}")
    print(f"对方总顺序数: {len(all_opp_orders)}")

    # 检查我方是否存在稳定顺序
    print("\n检查我方是否存在稳定顺序...")
    my_stable_orders = []

    for my_order in all_my_orders:
        is_stable = True
        for opp_order in all_opp_orders:
            if not does_A_win(my_order, opp_order):  # 如果有一场没赢，就不稳定
                is_stable = False
                break

        if is_stable:
            my_stable_orders.append(my_order)

    # 检查对方是否存在稳定顺序
    print("检查对方是否存在稳定顺序...")
    opp_stable_orders = []

    for opp_order in all_opp_orders:
        is_stable = True
        for my_order in all_my_orders:
            if not does_B_win(my_order, opp_order):  # 如果有一场没赢，就不稳定
                is_stable = False
                break

        if is_stable:
            opp_stable_orders.append(opp_order)

    return my_stable_orders, opp_stable_orders


# 主程序
print("正在检查双方是否存在稳定出场顺序...")
print("总枚举量:")
print("- 我方: C(6,5)×5! = 6×120 = 720 种顺序")
print("- 对方: C(6,5)×5! = 6×120 = 720 种顺序")
print("- 总对阵: 720×720 = 518,400 种")
print()

my_stable, opp_stable = check_stable_orders_for_both_sides()

print("\n" + "=" * 60)
print("检查结果:")
print()

# 我方结果
print("1. 我方稳定顺序检查:")
if my_stable:
    print(f"   ✅ 存在 {len(my_stable)} 个稳定出场顺序")
    print(f"   前5个稳定顺序:")
    for i, order in enumerate(my_stable[:5], 1):
        has_A6 = 'A6' in order
        print(f"     {i}. {order} {'(含A6)' if has_A6 else ''}")
else:
    print("   ❌ 不存在稳定出场顺序")
    print("   说明：任何我方顺序，对方都能找到一种顺序来击败我们")

print()

# 对方结果
print("2. 对方稳定顺序检查:")
if opp_stable:
    print(f"   ✅ 存在 {len(opp_stable)} 个稳定出场顺序")
    print(f"   前5个稳定顺序:")
    for i, order in enumerate(opp_stable[:5], 1):
        has_B6 = 'B6' in order
        print(f"     {i}. {order} {'(含B6)' if has_B6 else ''}")

    # 验证其中一个稳定顺序
    if opp_stable:
        test_order = opp_stable[0]
        print(f"\n   验证对方稳定顺序 {test_order}:")
        # 随机选10个我方顺序测试
        test_my_orders = all_my_orders[:10] if len(all_my_orders) >= 10 else all_my_orders
        for i, my_order in enumerate(test_my_orders, 1):
            my_score, opp_score = simulate_match(my_order, test_order)
            win = "B胜" if opp_score > my_score else "A胜" if my_score > opp_score else "平"
            print(f"     对阵 {my_order}: A得分={my_score:.1f}, B得分={opp_score:.1f} → {win}")
else:
    print("   ❌ 不存在稳定出场顺序")
    print("   说明：任何对方顺序，我方都能找到一种顺序来击败他们")

print()

# 总体结论
print("3. 总体结论:")
if not my_stable and not opp_stable:
    print("   🔄 双方都不存在绝对稳定的出场顺序")
    print("   任何固定策略都会被对方针对")
elif my_stable and not opp_stable:
    print("   ⭐ 仅我方存在稳定顺序，我方有绝对优势")
elif not my_stable and opp_stable:
    print("   ⚠️  仅对方存在稳定顺序，对方有绝对优势")
    print("   这是不合理的，需要检查数据或模型")
else:
    print("   ⚖️  双方都存在稳定顺序")
    print("   这种情况理论上可能但实际很少见")

print("=" * 60)
