import itertools
import json
from turtle import st

hire_list = [["重装干员", "生存"], ["生存", "防护"], ["输出", "防护"], ["辅助干员", "削弱"], ["术师干员", "减速", "输出"], ["特种干员", "生存"], ["辅助干员", "输出"], ["术师干员", "治疗"],  ["资深干员"], ["召唤"], ["控场"], ["爆发"], ["位移", "防护"], ["位移", "减速"], ["位移", "输出"], ["特种干员", "生存"], ["特种干员", "减速"], ["特种干员", "输出"], ["削弱", "群攻"], ["削弱", "特种干员"], ["削弱", "近战位"], ["削弱", "快速复活"], ["支援", "费用回复"], ["近卫干员", "防护"], ["治疗", "输出"], ["治疗", "减速"],["重装干员", "位移"],  ["支援", "输出"], ["支援", "治疗"],["医疗干员", "支援"],["快速复活"], ["特种干员"], ["削弱"], ["支援"], ["先锋干员", "治疗"],  ["近卫干员", "支援"], ["近卫干员", "减速"], ["狙击干员", "削弱"], ["狙击干员", "生存"], ["狙击干员", "减速"],  ["术师干员", "减速"], ["术师干员", "削弱"], ["近战位", "减速"], ["远程位", "生存"], ["远程位", "支援"],  ["治疗", "费用回复"], ["输出", "减速"], ["群攻", "减速"], ["位移"], ["支援"], ["削弱"]]
recruimentTime = 9

f = open('character.json', encoding='utf-8')
data = json.load(f)
operators = data.values()
publicRecruitmentOperators = list(filter(lambda x: bool(x['recruitment']), operators))
f.close()

f = open('tag.json', encoding="utf-8")
data = json.load(f)
tagIntToLabel = data
tagLabelToInt = {v: int(k) for k, v in data.items()}
f.close()

hire_list = [tuple(map(lambda x: tagLabelToInt[x], lst)) for lst in hire_list]

def getAllCombo(list):
    result = []
    if len(list) > 5:
        print(f"exceed max number of tags {len(list)}, using the first 5...")
        list = list[:5]
    
    for L in range(1, len(list)+1):
        for subset in itertools.combinations(list, L):
            result.append(subset)

    return result

starToTag = {6: 11, 5: 14, 2: 17}

comboEvaluation = {}

for combo in hire_list:
    # print(combo)
    comboOperators = []
    if recruimentTime == 9:
        publicRecruitmentOperators = list(filter(lambda o: o['star'] >= 3, publicRecruitmentOperators))
    for operator in publicRecruitmentOperators:
        tagset = operator["tags"] + [operator["profession"]] + [operator["position"]]
        if operator["star"] in starToTag:
            tagset += [starToTag[operator['star']]]
        if set(combo).issubset(tagset):
            comboOperators.append(operator)
            # print(operator['appellation'])

    if comboOperators:
        comboEvaluation[combo] = {
            "guaranteeStar" : min([operator["star"] for operator in comboOperators]),
            "operators" : comboOperators
        }

# print(comboEvaluation)
for c in comboEvaluation:
    print(list(map(lambda n: tagIntToLabel[str(n)], c)))
    print(comboEvaluation[c]['guaranteeStar'])
