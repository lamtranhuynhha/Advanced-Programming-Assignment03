import unittest
from TestUtils import TestUtils
import inspect

class TestSymbolTable(unittest.TestCase):

    def test_001(self):
        input = ["INSERT a1 number", "INSERT b2 string"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_002(self):
        input = ["INSERT x number", "INSERT y string", "INSERT x string"]
        expected = ["Redeclared: INSERT x string"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_003(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["TypeMismatch: ASSIGN y 17"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_004(self):
        input = [
            "INSERT x number",
            "ASSIGN y 17",
        ]
        expected = ["Undeclared: ASSIGN y 17"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_005(self):
        input = [
            "INSERT x number",
            "ASSIGN x y",
        ]
        expected = ["Undeclared: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 
    
    def test_006(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x y",
        ]
        expected = ["TypeMismatch: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_007(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END",
        ]
        expected = ["success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_008(self):
        input = [
            "END",
        ]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_009(self):
        input = [
            "BEGIN",
        ]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 
    
    def test_010(self):
        input = [
            "BEGIN",
            "BEGIN",
            "END",
            "BEGIN",
        ]
        expected = ["UnclosedBlock: 2"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_011(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "1", "0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 

    def test_012(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "y//0 x//1 z//1"]

        self.assertTrue(TestUtils.check(input, expected, 105))

    def test_013(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]

        self.assertTrue(TestUtils.check(input, expected, 106))

    def test_014(self):
        input = [
            "INSERT x number "
        ]
        expected = ["Invalid: INSERT x number "]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
        
    def test_015(self):
        ipnut = [
            "INSERT  a number"
            ]
        expected = ["Invalid: INSERT  a number"]
        self.assertTrue(TestUtils.check(ipnut, expected, inspect.stack()[0].function))

    def test_016(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_017(self):
        input = [
            "INSERT x number",
            "INSERT y number",
            "INSERT z string",
            "ASSIGN y x",
            "ASSIGN x y"
        ]
        expected = ["success", "success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_018(self):
        input = [
            "INSERT x number",
            "INSERT z string",
            "ASSIGN z x"
        ]
        expected = ["TypeMismatch: ASSIGN z x"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_019(self):
        input = [
            "INSERT x number",
            "ASSIGN x y"
        ]
        expected = ["Undeclared: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_020(self):
        ipnut = [
            " INSERT a number"
            ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(ipnut, expected, inspect.stack()[0].function))

    def test_021(self):
        input = ["PRINT"]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_022(self):
        input = ["RPRINT"]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_023(self):
        input = ["INSERT"]
        expected = ["Invalid: INSERT"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_024(self):
        input = ["INSERT 1x number"]
        expected = ["Invalid: INSERT 1x number"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_025(self):
        input = ["INSERT x boolean"]
        expected = ["Invalid: INSERT x boolean"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_026(self):
        input = [
            "INSERT x string",
            "ASSIGN x 'abc_'"
        ]
        expected = ["Invalid: ASSIGN x 'abc_'"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_027(self):
        input = [
            "INSERT x number",
            "ASSIGN x 12a"
        ]
        expected = ["Invalid: ASSIGN x 12a"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_028(self):
        input = ["ASSIGN x 10"]
        expected = ["Undeclared: ASSIGN x 10"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_029(self):
        input=[
            "INSERT a number",
            "BEGIN",
            "INSERT b string",
            "END",
            "BEGIN",
            "INSERT c number",
            "PRINT",
            "END"
        ]
        expected = ["success", "success", "success","a//0 c//1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    
    def test_030(self):
        input = [
            "INSERT a number",
            "INSERT b string",
            "INSERT c number",
            "INSERT d string",
            "PRINT"
        ]
        expected = ["success", "success", "success", "success", "a//0 b//0 c//0 d//0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_031(self):
        input = [
            "INSERT a number",
            "INSERT b string",
            "BEGIN",
            "INSERT c number",
            "INSERT d string",
            "RPRINT",
            "END"
        ]
        expected = ["success", "success", "success", "success", "d//1 c//1 b//0 a//0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_032(self):
        input = [
            "INSERT x number",
            "ASSIGN x x"
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_033(self):
        input = [
            "INSERT a number",
            "INSERT b number",
            "INSERT c number",
            "ASSIGN b a",
            "ASSIGN c b"
        ]
        expected = ["success", "success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_034(self):
        input = []
        expected = []
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_035(self):
        input = [
            "INSERT a number",
            "INSERT b string",
            "BEGIN",
            "INSERT c number",
            "PRINT",
            "BEGIN",
            "INSERT d string",
            "PRINT",
            "END",
            "END"
        ]
        expected = ["success", "success", "success", "a//0 b//0 c//1","success", "a//0 b//0 c//1 d//2"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_036(self):
        input = [
            "INSERT a number",
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "LOOKUP a",
            "END",
            "END",
            "END",
            "END"
        ]
        expected = ["success","0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_037(self):
        input = [
            "INSERT x number",
            "BEGIN",
            "INSERT x string",
            "BEGIN",
            "INSERT x number",
            "PRINT",
            "RPRINT",
            "END",
            "END"
        ]
        expected = ["success", "success", "success", "x//2", "x//2"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_038(self):
        input = [
            "BEGIN",
            "BEGIN",
            "BEGIN",
            "END",
            "END",
            "END"
        ]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_039(self):
        input = [
            "INSERT x number",
            "ASSIGN x 42"
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_040(self):
        input = [
            "INSERT x string",
            "ASSIGN x 'hello'"
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_041(self):
        ipnut = [
            "End "
            ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(ipnut, expected, inspect.stack()[0].function))

    def test_042(self):
        input = [
            "INSERT y@1 number"
        ]
        expected = ["Invalid: INSERT y@1 number"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_043(self):
        input = [
            "INSERT x float"
        ]
        expected = ["Invalid: INSERT x float"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_044(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 1.5"
        ]
        expected = ["Invalid: ASSIGN x 1.5"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_045(self):
        input = [
            "INSERT x string",
            "ASSIGN x 'a@1'"
        ]
        expected = ["Invalid: ASSIGN x 'a@1'"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_046(self):
        input = [
            "INSERT s string",
            "ASSIGN s ''",
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    
    def test_047(self):
        input = [
            "INSERT number number"
        ]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_048(self):
        input = [
            "PRINT",
            "RPRINT",
            "PRINT"
        ]
        expected = ["", "", ""]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    
    def test_049(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
        ]
        expected = ["UnclosedBlock: 2"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_050(self):
        input =[
            ""
        ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))