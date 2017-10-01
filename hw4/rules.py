import tree
import re
import sys, fileinput

#generate tree from tree string
treeString = "(TOP (FRAG_PP (IN On) (NP_NNP Friday)) (PUNC .))"


def getRulesInTheTree(tree, ruleCount, pblityCountHelper):
    treeNodeQueue = []
    treeNodeQueue.append(tree.root)
    while len(treeNodeQueue) > 0:
        lhs = treeNodeQueue.pop()
        rule = [str(lhs)]
        for r in lhs.children:
            rule.append(str(r))
            if len(r.children)>0:
                treeNodeQueue.append(r)
        rule_key = ",".join(rule)
        if rule_key not in ruleCount:
            ruleCount[rule_key] = 0
        ruleCount[rule_key] = ruleCount[rule_key] + 1
    #print(ruleCount)

def readTreesAndGetRules():
    ruleCount = {}
    pblityCountHelper = {}
    for treeString in open("train.trees.pre.unk","r"):
        t = tree.Tree.from_str(treeString)
        getRulesInTheTree(t, ruleCount, pblityCountHelper)
    #Q 1
    print len(ruleCount)
    key = max(ruleCount, key=ruleCount.get)
    print(key , ruleCount[key])

readTreesAndGetRules()
