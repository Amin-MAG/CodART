from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from gen.javaLabeled.JavaLexer import JavaLexer
from gen.javaLabeled.JavaParserLabeled import JavaParserLabeled

from gen.javaLabeled.JavaParserLabeledListener import JavaParserLabeledListener


def is_equal(a, b):
    return str(a) == str(b)


def get_duplicate_continues_statements(a_statements, b_statements):
    len_a_statement = len(a_statements)
    len_b_statement = len(b_statements)

    # for any method like such as getters or setters that has few number of
    # statements. we should return None.
    if len_b_statement <= 1 or len_a_statement <= 1:
        return None

    # diagnose exact duplications
    method_a_b_duplications = []
    i = 0
    while i < len_a_statement:
        j = 0
        while j < len_b_statement:
            sa = a_statements[i]
            sb = b_statements[j]
            count_duplicate_statement = 0
            duplicates = []
            k = 0
            while is_equal(sa.statement.getText(), sb.statement.getText()) \
                    and i + k < len_a_statement and j + k < len_b_statement:
                sa = a_statements[i + k]
                sb = b_statements[j + k]
                count_duplicate_statement += 1
                duplicates.append(sa)
                k += 1
            if count_duplicate_statement != 0:
                method_a_b_duplications.append((count_duplicate_statement, duplicates))
            j += 1
        i += 1

    max_duplicate = max(method_a_b_duplications, key=lambda x: x[0])
    return max_duplicate


class Statement:
    def __init__(self, statement, expressions):
        self.statement = statement
        self.expressions = expressions

    def __str__(self):
        return "[\n\tstatement: {}\n\texpressions: {}\n]".format(
            self.statement.getText(),
            list(map(lambda x: x.getText(), self.expressions))
        )


class ExtractMethodRefactoring(JavaParserLabeledListener):

    def __init__(self, common_token_stream: CommonTokenStream = None, class_name: str = "Main"):
        self.code = ""
        self.refactor_class_name = class_name
        if common_token_stream is None:
            raise ValueError('common_token_stream is None')
        else:
            self.token_stream_re_writer = TokenStreamRewriter(common_token_stream)

        self.statements = {}
        self.is_in_target_class = False
        self.is_in_a_method = False
        self.current_method_name = ""
        self.current_statement_index = 0

    def enterClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if is_equal(ctx.IDENTIFIER(), self.refactor_class_name):
            self.is_in_target_class = True

    def exitClassDeclaration(self, ctx: JavaParserLabeled.ClassDeclarationContext):
        if is_equal(ctx.IDENTIFIER(), self.refactor_class_name):
            self.is_in_target_class = False
            self.find_duplicates()
            self.refactor()

    def enterMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        if self.is_in_target_class:
            self.is_in_a_method = True
            self.current_method_name = ctx.IDENTIFIER()
            self.statements[self.current_method_name] = []

    def exitMethodDeclaration(self, ctx: JavaParserLabeled.MethodDeclarationContext):
        self.is_in_a_method = False

    def enterStatement15(self, ctx: JavaParserLabeled.Statement0Context):
        if self.is_in_target_class:
            if self.is_in_a_method:
                self.current_statement_index = len(self.statements[self.current_method_name])
                self.statements[self.current_method_name].append(
                    Statement(ctx, [])
                )

    # def enterExpression0(self, ctx: JavaParserLabeled.Expression0Context):
    #     if self.is_in_target_class:
    #         if self.is_in_a_method:
    #             print(self.current_statement_index)
    #             print(self.statements[self.current_method_name][self.current_statement_index])
    #             print(self.statements[self.current_method_name][self.current_statement_index].expressions)
    #             self.statements[self.current_method_name][self.current_statement_index].expressions.append(ctx)

    def exitCompilationUnit(self, ctx: JavaParserLabeled.CompilationUnitContext):
        # self.token_stream_re_writer.insertAfter(
        #     index=ctx.stop.tokenIndex,
        #     text=self.code
        # )
        pass

    def find_duplicates(self):
        # it is for representing the statements of each method
        for method_name in self.statements.keys():
            print(method_name)
            statements = self.statements[method_name]
            for statement in statements:
                print(str(statement))
            print("---------------")

        # Compare each one of methods with the other methods
        methods = list(self.statements.keys())
        len_method = len(methods)
        print(len_method)
        print(list(map(lambda x: x.getText(), self.statements.keys())))
        i = 0
        while i < len_method - 1:
            j = i + 1
            while j < len_method:
                duplicate = get_duplicate_continues_statements(
                    self.statements[methods[i]],
                    self.statements[methods[j]]
                )

                # return value is None when not any duplications have been found.
                if duplicate is not None:
                    print("{} and {} have {} duplicates lines".format(
                        methods[i].getText(), methods[j].getText(), duplicate[0]),
                        list(map(lambda x: x.statement.getText(), duplicate[1])))

                j += 1
            i += 1

    def refactor(self):
        pass


if __name__ == "__main__":
    input_file = r"C:\Users\Amin\MAG\_term_6\CodART\tests\extract_method\input_file.java"
    output_file = r"C:\Users\Amin\MAG\_term_6\CodART\tests\extract_method\output_file.java"

    stream = FileStream(input_file, encoding='utf8')
    lexer = JavaLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = JavaParserLabeled(token_stream)
    parser.getTokenStream()
    parse_tree = parser.compilationUnit()
    my_listener = ExtractMethodRefactoring(common_token_stream=token_stream, class_name="Student")
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=my_listener)

    with open(output_file, mode='w', newline='') as f:
        f.write(my_listener.token_stream_re_writer.getDefaultText())
