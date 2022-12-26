from Day25 import snafu_to_decimal, dec_to_base, decimal_to_snafu


def test_decimal_to_snafu():
    assert decimal_to_snafu(1) == "1"
    assert decimal_to_snafu(2) == "2"
    assert decimal_to_snafu(3) == "1="
    assert decimal_to_snafu(4) == "1-"

    assert decimal_to_snafu(5) == "10"
    assert decimal_to_snafu(6) == "11"
    assert decimal_to_snafu(7) == "12"
    assert decimal_to_snafu(8) == "2="
    assert decimal_to_snafu(9) == "2-"

    assert decimal_to_snafu(10) == "20"
    assert decimal_to_snafu(15) == "1=0"
    assert decimal_to_snafu(20) == "1-0"
    assert decimal_to_snafu(2022) == "1=11-2"
    assert decimal_to_snafu(314159265) == "1121-1110-1=0"

def test_snafu_to_decimal():
    assert snafu_to_decimal("1") == 1
    assert snafu_to_decimal("2") == 2

    assert snafu_to_decimal("1=") == 3
    assert snafu_to_decimal("1-") == 4
    assert snafu_to_decimal("10") == 5
    assert snafu_to_decimal("11") == 6
    assert snafu_to_decimal("12") == 7
    assert snafu_to_decimal("2=") == 8
    assert snafu_to_decimal("2-") == 9

    assert snafu_to_decimal("20") == 10
    assert snafu_to_decimal("1=0") == 15
    assert snafu_to_decimal("1-0") == 20
    assert snafu_to_decimal("1=11-2") == 2022
    assert snafu_to_decimal("1-0---0") == 12345
    assert snafu_to_decimal("1121-1110-1=0") == 314159265

def test_dec_to_base():
    assert dec_to_base(1, 5) == "1"
    assert dec_to_base(2, 5) == "2"
    assert dec_to_base(5, 5) == "10"
    assert dec_to_base(6, 5) == "11"
    assert dec_to_base(24, 5) == "44"
    assert dec_to_base(15, 5) == "30"
    assert dec_to_base(16, 5) == "31"
    assert dec_to_base(2022, 5) == "31042"


