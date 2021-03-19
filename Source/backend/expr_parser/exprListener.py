# Generated from expr.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .exprParser import exprParser
else:
    from exprParser import exprParser

# This class defines a complete listener for a parse tree produced by exprParser.
class exprListener(ParseTreeListener):

    # Enter a parse tree produced by exprParser#equation.
    def enterEquation(self, ctx:exprParser.EquationContext):
        pass

    # Exit a parse tree produced by exprParser#equation.
    def exitEquation(self, ctx:exprParser.EquationContext):
        pass


    # Enter a parse tree produced by exprParser#rules.
    def enterRules(self, ctx:exprParser.RulesContext):
        pass

    # Exit a parse tree produced by exprParser#rules.
    def exitRules(self, ctx:exprParser.RulesContext):
        pass


    # Enter a parse tree produced by exprParser#singleRule.
    def enterSingleRule(self, ctx:exprParser.SingleRuleContext):
        pass

    # Exit a parse tree produced by exprParser#singleRule.
    def exitSingleRule(self, ctx:exprParser.SingleRuleContext):
        pass


    # Enter a parse tree produced by exprParser#expression.
    def enterExpression(self, ctx:exprParser.ExpressionContext):
        pass

    # Exit a parse tree produced by exprParser#expression.
    def exitExpression(self, ctx:exprParser.ExpressionContext):
        pass


    # Enter a parse tree produced by exprParser#multiplyingExpression.
    def enterMultiplyingExpression(self, ctx:exprParser.MultiplyingExpressionContext):
        pass

    # Exit a parse tree produced by exprParser#multiplyingExpression.
    def exitMultiplyingExpression(self, ctx:exprParser.MultiplyingExpressionContext):
        pass


    # Enter a parse tree produced by exprParser#powExpression.
    def enterPowExpression(self, ctx:exprParser.PowExpressionContext):
        pass

    # Exit a parse tree produced by exprParser#powExpression.
    def exitPowExpression(self, ctx:exprParser.PowExpressionContext):
        pass


    # Enter a parse tree produced by exprParser#signedAtom.
    def enterSignedAtom(self, ctx:exprParser.SignedAtomContext):
        pass

    # Exit a parse tree produced by exprParser#signedAtom.
    def exitSignedAtom(self, ctx:exprParser.SignedAtomContext):
        pass


    # Enter a parse tree produced by exprParser#atom.
    def enterAtom(self, ctx:exprParser.AtomContext):
        pass

    # Exit a parse tree produced by exprParser#atom.
    def exitAtom(self, ctx:exprParser.AtomContext):
        pass


    # Enter a parse tree produced by exprParser#scientific.
    def enterScientific(self, ctx:exprParser.ScientificContext):
        pass

    # Exit a parse tree produced by exprParser#scientific.
    def exitScientific(self, ctx:exprParser.ScientificContext):
        pass


    # Enter a parse tree produced by exprParser#constant.
    def enterConstant(self, ctx:exprParser.ConstantContext):
        pass

    # Exit a parse tree produced by exprParser#constant.
    def exitConstant(self, ctx:exprParser.ConstantContext):
        pass


    # Enter a parse tree produced by exprParser#variable.
    def enterVariable(self, ctx:exprParser.VariableContext):
        pass

    # Exit a parse tree produced by exprParser#variable.
    def exitVariable(self, ctx:exprParser.VariableContext):
        pass


    # Enter a parse tree produced by exprParser#func.
    def enterFunc(self, ctx:exprParser.FuncContext):
        pass

    # Exit a parse tree produced by exprParser#func.
    def exitFunc(self, ctx:exprParser.FuncContext):
        pass


    # Enter a parse tree produced by exprParser#funcname.
    def enterFuncname(self, ctx:exprParser.FuncnameContext):
        pass

    # Exit a parse tree produced by exprParser#funcname.
    def exitFuncname(self, ctx:exprParser.FuncnameContext):
        pass


    # Enter a parse tree produced by exprParser#relop.
    def enterRelop(self, ctx:exprParser.RelopContext):
        pass

    # Exit a parse tree produced by exprParser#relop.
    def exitRelop(self, ctx:exprParser.RelopContext):
        pass


