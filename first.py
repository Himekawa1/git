import itertools

# 根据历史数据（我方:对方 总分）
# 格式: {('A1','A2'): {('B1','B2'): (65,58)}}
historical_data = {
    ('A1', 'A2'): {('B1', 'B2'): (65, 58)},
    ('A2', 'A3'): {('B2', 'B3'): (42, 27)},
    ('A1', 'A3'): {('B1', 'B2'): (63, 61), ('B3', 'B5'): (21, 10)},
    ('A1', 'A4'): {('B2', 'B4'): (60, 57)},
    ('A1', 'A5'): {('B1', 'B5'): (60, 51)},
    ('A4', 'A5'): {('B3', 'B5'): (35, 32)},
    ('A2', 'A4'): {('B2', 'B4'): (34, 36)},
    ('A2', 'A5'): {('B3', 'B5'): (42, 28)},
    ('A3', 'A4'): {('B4', 'B5'): (21, 14), ('B3', 'B4'): (41, 41)},
}


def get_win_rate(my_pair, opp_pair):
    """
    计算我方组合对对方组合的得分率
    如果历史数据中没有对应记录，返回0.5
    """
    # 将组合排序以保证一致（双打组合顺序不影响）
    my_pair_sorted = tuple(sorted(my_pair))
    opp_pair_sorted = tuple(sorted(opp_pair))

    if my_pair_sorted in historical_data:
        if opp_pair_sorted in historical_data[my_pair_sorted]:
            my_score, opp_score = historical_data[my_pair_sorted][opp_pair_sorted]
            return my_score / (my_score + opp_score)

    # 如果没有历史数据，返回0.5
    return 0.5


def calculate_total_win_rate(my_order):
    """
    计算给定我方出场顺序下的总胜率（五个阶段的平均得分率）
    对方出场顺序固定为B1,B2,B3,B4,B5
    """
    # 对方固定顺序
    opp_order = ['B1', 'B2', 'B3', 'B4', 'B5']

    # 五个阶段的对抗组合
    stage_pairs = []

    # 阶段1: (A_i1,A_i2) vs (B1,B2)
    stage_pairs.append(((my_order[0], my_order[1]), (opp_order[0], opp_order[1])))
    # 阶段2: (A_i2,A_i3) vs (B2,B3)
    stage_pairs.append(((my_order[1], my_order[2]), (opp_order[1], opp_order[2])))
    # 阶段3: (A_i3,A_i4) vs (B3,B4)
    stage_pairs.append(((my_order[2], my_order[3]), (opp_order[2], opp_order[3])))
    # 阶段4: (A_i4,A_i5) vs (B4,B5)
    stage_pairs.append(((my_order[3], my_order[4]), (opp_order[3], opp_order[4])))
    # 阶段5: (A_i5,A_i1) vs (B5,B1)
    stage_pairs.append(((my_order[4], my_order[0]), (opp_order[4], opp_order[0])))

    # 计算每个阶段的得分率
    win_rates = []
    for my_pair, opp_pair in stage_pairs:
        win_rate = get_win_rate(my_pair, opp_pair)
        win_rates.append(win_rate)

    # 返回平均得分率
    return sum(win_rates) / len(win_rates)


def solve_problem1():
    """
    解决第一问：枚举所有可能的出场顺序，找出最佳顺序
    """
    # 我方所有选手
    players = ['A1', 'A2', 'A3', 'A4', 'A5']

    # 存储最佳结果
    best_order = None
    best_win_rate = -1
    all_results = []

    # 枚举所有可能的出场顺序（5! = 120种）
    for order in itertools.permutations(players):
        win_rate = calculate_total_win_rate(order)
        all_results.append((order, win_rate))

        # 更新最佳结果
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            best_order = order

    # 按胜率排序
    all_results.sort(key=lambda x: x[1], reverse=True)

    # 输出最佳结果
    print("最佳出场顺序: ", best_order)
    print("最佳平均得分率: ", best_win_rate)

    print("\n前10个最佳出场顺序:")
    for i, (order, win_rate) in enumerate(all_results[:10], 1):
        print(f"{i}. {order}: {win_rate:.4f}")

    return best_order, best_win_rate, all_results[:10]


def main():
    print("=== 五羽轮比比赛出场顺序问题 - 问题1求解 ===")
    print("对方出场顺序固定为: ['B1', 'B2', 'B3', 'B4', 'B5']")
    print("我方选手: ['A1', 'A2', 'A3', 'A4', 'A5']")
    print("=" * 50)

    # 求解问题1
    best_order, best_win_rate, top10 = solve_problem1()

    print("\n" + "=" * 50)
    print("结论：")
    print(f"在对方出场顺序固定为B1,B2,B3,B4,B5的情况下，")
    print(f"我方最佳出场顺序为: {best_order}")
    print(f"该顺序下的平均得分率为: {best_win_rate:.4f}")
    print(f"（即在该顺序下，我方在所有阶段对抗中平均能获得{best_win_rate * 100:.1f}%的分数）")


if __name__ == "__main__":
    main()
