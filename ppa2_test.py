import ppa2src as functions
from pytest import *
from _pytest.monkeypatch import MonkeyPatch
import builtins

class DummyResult:
    
    def fetchall(self):
        return None

class DummyConn:

    def execute(self, input_string):
        dum_res = DummyResult()
        return dum_res

def test_calcBMI():

    under = functions.calcBMI('5 8', '110')
    assert 'Underweight' in under
    assert float(under.split()[1]) == approx(17.12802768, 0.01)

    normal = functions.calcBMI('5 7', '130')
    assert 'Normal Weight' in normal
    assert float(normal.split()[1]) == approx(20.8509690, 0.01)

    over = functions.calcBMI('6 3', '210')
    assert 'Overweight' in over
    assert float(over.split()[1]) == approx(26.88, 0.01)

    obese = functions.calcBMI('5 11', '225')
    assert 'Obese' in obese
    assert float(obese.split()[1]) == approx(32.1364808, 0.01)

def test_calcRetirement():

    reached = functions.calcRetirement('21', '100000', '35', '2000000')
    assert int(reached.split()[8]) == 63

    missed = functions.calcRetirement('40', '70000', '20', '1500000')
    assert 'ambitious' in missed

def test_calcDistance():

    line1 = functions.calcDistance('1', '1', '5', '4')
    assert line1 == approx(5.0)

    line2 = functions.calcDistance('20', '16', '56', '62')
    assert line2 == approx(58.41232747)

def test_verifyEmail():

    regular = functions.verifyEmail('me!@somewhere123.com')
    assert regular.split()[4] == 'valid!'

    dotsFront = functions.verifyEmail('.me@somewhere.com')
    assert dotsFront.split()[4] == 'invalid'

    dotsBack = functions.verifyEmail('.me@somewhere45.com')
    assert dotsBack.split()[4] == 'invalid'

    sepDots = functions.verifyEmail('me..2@somewhere.com')
    assert sepDots.split()[4] == 'invalid'

    wrongChar = functions.verifyEmail('me()@somewhere.com')
    assert wrongChar.split()[4] == 'invalid'

    twoAts = functions.verifyEmail('me@somewhere@there.com')
    assert twoAts.split()[4] == 'invalid'

def test_getBMI():

    def mock_BMI_input(x):
        values = ['5 8', '180']
        if 'height' in x:
            return values[0]
        elif 'weight' in x:
            return values[1]

    monkeypatch_one = MonkeyPatch()
    monkeypatch_one.setattr(builtins, 'input', lambda x: mock_BMI_input(x))

    dum_con_one = DummyConn()
    
    assert functions.getBMI(dum_con_one) == 'Value: 28.02768166089965 Category: Overweight\n'

def test_getDistance():

    def mock_Distance_input(x):
        values = ['1','3','4','2']
        if 'first' in x:
            if 'x' in x:
                return values[0]
            elif 'y' in x:
                return values[1]
        elif 'second' in x:
            if 'x' in x:
                return values[2]
            elif 'y' in x:
                return values[3]

    monkeypatch_two = MonkeyPatch()
    monkeypatch_two.setattr(builtins, 'input', lambda x: mock_Distance_input(x))

    dum_con_two = DummyConn()

    assert functions.getDistance(dum_con_two) == 'Distance: 3.1622776601683795\n'
