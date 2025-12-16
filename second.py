# 问题2：对方针对我方原顺序采用最优反制时的调整策略

import itertools
import numpy as np

# 历史数据（同上）
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
    """
    my_pair_sorted = tuple(sorted(my_pair))
    opp_pair_sorted = tuple(sorted(opp_pair))

    if my_pair_sorted in historical_data:
        if opp_pair_sorted in historical_data[my_pair_sorted]:
            my_score, opp_score = historical_data[my_pair_sorted][opp_pair_sorted]
            return my_score / (my_score + opp_score)

    return 0.5


def calculate_match_result(my_order, opp_order):
    """
    计算给定双方出场顺序下的比赛结果
    返回：我方总得分（模拟50分制）
    """
    # 五个阶段的对抗组合
    stage_pairs = [
        ((my_order[0], my_order[1]), (opp_order[0], opp_order[1])),
        ((my_order[1], my_order[2]), (opp_order[1], opp_order[2])),
        ((my_order[2], my_order[3]), (opp_order[2], opp_order[3])),
        ((my_order[3], my_order[4]), (opp_order[3], opp_order[4])),
        ((my_order[4], my_order[0]), (opp_order[4], opp_order[0]))
    ]

    # 模拟50分制比赛过程
    my_total_score = 0
    opp_total_score = 0

    for my_pair, opp_pair in stage_pairs:
        win_rate = get_win_rate(my_pair, opp_pair)
        # 每阶段假设打10分，按得分率分配
        my_stage_score = 10 * win_rate
        opp_stage_score = 10 * (1 - win_rate)

        my_total_score += my_stage_score
        opp_total_score += opp_stage_score

        # 如果已经达到50分，提前结束
        if my_total_score >= 50 or opp_total_score >= 50:
            break

    return my_total_score, opp_total_score


def find_opponent_best_counter(my_fixed_order):
    """
    找出对方针对我方固定顺序的最优三种反制顺序
    """
    players = ['B1', 'B2', 'B3', 'B4', 'B5']
    best_orders = []  # 存储(顺序, 对方得分)

    for opp_order in itertools.permutations(players):
        _, opp_score = calculate_match_result(my_fixed_order, opp_order)
        best_orders.append((opp_order, opp_score))

    # 按对方得分从高到低排序
    best_orders.sort(key=lambda x: x[1], reverse=True)

    # 返回最优的三种顺序（去重相似的）
    unique_orders = []
    seen = set()

    for order, score in best_orders:
        order_str = ''.join(order)
        if order_str not in seen:
            unique_orders.append((order, score))
            seen.add(order_str)
            if len(unique_orders) >= 3:
                break

    return unique_orders[:3]


def find_best_response(counter_orders):
    """
    针对对方的三种最优反制顺序，找到我方的最佳应对顺序
    """
    my_players = ['A1', 'A2', 'A3', 'A4', 'A5']
    best_response = None
    best_worst_score = -1  # 最坏情况下的最好成绩

    all_results = []

    # 枚举所有我方顺序
    for my_order in itertools.permutations(my_players):
        # 计算在三种反制顺序下的最坏情况
        worst_score = float('inf')
        for opp_order, _ in counter_orders:
            my_score, _ = calculate_match_result(my_order, opp_order)
            worst_score = min(worst_score, my_score)

        all_results.append((my_order, worst_score))

        # 更新最佳应对（最大化最坏情况下的得分）
        if worst_score > best_worst_score:
            best_worst_score = worst_score
            best_response = my_order

    # 按最坏情况得分排序
    all_results.sort(key=lambda x: x[1], reverse=True)

    return best_response, best_worst_score, all_results[:10]


def solve_problem2():
    """
    解决第二问：对方反制时的最佳调整策略
    """
    print("=== 五羽轮比比赛出场顺序问题 - 问题2求解 ===")
    print("我方原计划出场顺序: ['A1', 'A2', 'A3', 'A4', 'A5']")
    print("=" * 60)

    # 我方固定顺序
    my_fixed_order = ('A1', 'A2', 'A3', 'A4', 'A5')

    # 1. 找出对方的最优三种反制顺序
    print("寻找对方针对我方顺序的最优三种反制顺序...")
    counter_orders = find_opponent_best_counter(my_fixed_order)

    print("\n对方最优的三种反制顺序：")
    for i, (order, opp_score) in enumerate(counter_orders, 1):
        my_score, _ = calculate_match_result(my_fixed_order, order)
        print(f"{i}. {order}: 对方预计得分 {opp_score:.1f}, 我方预计得分 {my_score:.1f}")

    # 2. 寻找我方的最佳应对顺序
    print("\n寻找我方最佳应对顺序（极小化最大损失）...")
    best_response, best_worst_score, top10 = find_best_response(counter_orders)

    print(f"\n最佳应对顺序: {best_response}")
    print(f"在最坏情况下的预计得分: {best_worst_score:.1f}")

    print(f"\n前10个最佳应对顺序（按最坏情况得分排序）:")
    for i, (order, worst_score) in enumerate(top10, 1):
        # 计算该顺序对三种反制顺序的具体表现
        scores = []
        for opp_order, _ in counter_orders:
            my_score, _ = calculate_match_result(order, opp_order)
            scores.append(my_score)
        avg_score = np.mean(scores)
        print(f"{i}. {order}: 最坏={worst_score:.1f}, 平均={avg_score:.1f}, 具体={[f'{s:.1f}' for s in scores]}")

    # 3. 详细分析最佳应对顺序的表现
    print(f"\n{'=' * 60}")
    print(f"详细分析最佳应对顺序 {best_response}:")

    for i, (opp_order, _) in enumerate(counter_orders, 1):
        my_score, opp_score = calculate_match_result(best_response, opp_order)
        win = "胜" if my_score > opp_score else "负"
        print(f"对阵对方反制顺序{i} {opp_order}:")
        print(f"  我方得分: {my_score:.1f}, 对方得分: {opp_score:.1f} → {win}")

    return best_response, counter_orders


if __name__ == "__main__":
    best_response, counter_orders = solve_problem2()

    print(f"\n{'=' * 60}")
    print("结论：")
    print("当对方针对我方原顺序(A1,A2,A3,A4,A5)采取最优反制时，")
    print(f"我方最佳调整顺序为: {best_response}")
    print("该顺序能在对方三种最优反制下保持较好的表现。")
