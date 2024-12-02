def generate_initial_plan(pg_dict, lifter_weight_list):
    """
    根据当前状态生成初步任务分配计划
    - pg_dict: 剩余箱子的体积和重量映射字典
    - lifter_weight_list: 所有代理的举重能力列表
    """
    plan = {}
    for box, weight in pg_dict.items():
        if not isinstance(box, str):
            # 如果 box 不是字符串，则将其格式化为字符串
            box = f"box[{box}V]"
        # 根据任务重量选择满足条件的代理
        selected_agents = []
        for agent in lifter_weight_list:
            if sum(selected_agents) + agent >= weight:
                selected_agents.append(agent)
                break
        plan[box] = selected_agents
    return plan

def calculate_agent_utility(agent_capability, task_weight, collaboration_cost):
    """
    计算代理的收益
    - agent_capability: 代理的举重能力
    - task_weight: 分配给代理的任务重量
    - collaboration_cost: 协作成本
    """
    if agent_capability >= task_weight:
        return agent_capability - task_weight - collaboration_cost
    else:
        return -float('inf')  # 超出能力范围，收益为负无穷

def simulate_follower_responses(plan, lifter_weight_list, collaboration_cost=0.1):
    """
    模拟代理反馈
    - plan: 中央规划器分配的任务计划
    - lifter_weight_list: 所有代理的举重能力列表
    - collaboration_cost: 协作成本
    """
    responses = {}
    for box, agents in plan.items():
        if isinstance(box, float):
            # 确保 box 为字符串格式
            box = f"box[{box}V]"
        task_weight = float(box.split('[')[-1].strip('V]'))
        utility = sum(calculate_agent_utility(agent, task_weight, collaboration_cost) for agent in agents)
        responses[box] = "Accept" if utility > 0 else "Reject"
    return responses

def optimize_plan_based_on_responses(plan, responses, lifter_weight_list):
    """
    根据代理反馈优化任务分配计划
    - plan: 初始任务分配计划
    - responses: 代理反馈（接受/拒绝）
    - lifter_weight_list: 所有代理的举重能力列表
    """
    optimized_plan = plan.copy()
    for box, response in responses.items():
        if isinstance(box, float):
            # 确保 box 为字符串格式
            box = f"box[{box}V]"
        if response == "Reject":
            weight = float(box.split('[')[-1].strip('V]'))
            alternative_agents = [agent for agent in lifter_weight_list if agent >= weight]
            optimized_plan[box] = alternative_agents[:1]  # 选择替代代理
    return optimized_plan
pg_dict = {3.0: 3.0, 5.0: 5.0}
lifter_weight_list = [1.5, 3.5, 5.0]

# plan = generate_initial_plan(pg_dict, lifter_weight_list)
# print("Generated Plan:", plan)
# responses = simulate_follower_responses(plan, lifter_weight_list)
# print("Responses:", responses)
# responses = {'box[3.0V]': 'Reject', 'box[5.0V]': 'Accept'}
# optimized_plan = optimize_plan_based_on_responses(plan, responses, lifter_weight_list)
# print("Optimized Plan:", optimized_plan)
