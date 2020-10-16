deposit_btc = 0
deposit_usd = 0
user_acquisition_amount = 100
user_last_calculation = 0

all_deposit_btc = 1000
all_deposit_usd = 20000

other_acquisition_amount = 500

price_btc = 0.1

log = []

type_none = 0
type_income_usd = 1
type_income_btc = 2
type_acquisitions = 3

periods = [
    [
        0,  # amount $
        0,  # amount btc
        type_none
    ]
]


def print_log():
    for s in log:
        print(s)


def add_log(text):
    log.append(text)


def get_state():
    return "deposit_btc\t" + str(deposit_btc) + "\t" + \
           "deposit_usd\t" + str(deposit_usd) + "\t" + \
           "all_deposit_btc\t" + str(all_deposit_btc) + "\t" + \
           "all_deposit_usd\t" + str(all_deposit_usd) + "\t"


def print_state(title):
    print("++++++++++++++++++", title, "+++++++++++")
    print(get_state())


def amount_acquisition_on_back_side():
    global periods
    print("acquisitions count", len(periods))
    return int(input("amount from backend:"))


def acquisition():
    global price_btc, all_deposit_usd, all_deposit_btc
    amount_acquisition = amount_acquisition_on_back_side()
    # price_btc = price_btc + len(periods) / 100
    current_acquisition = [
        amount_acquisition,
        amount_acquisition * price_btc,
        type_acquisitions
    ]
    periods.append(current_acquisition)
    all_deposit_usd = all_deposit_usd - current_acquisition[0]
    all_deposit_btc = all_deposit_btc + current_acquisition[1]
    return current_acquisition


def add_income_usd(amount_usd):
    global price_btc, all_deposit_usd, all_deposit_btc
    current_income = [
        amount_usd,
        all_deposit_usd,
        type_income_usd
    ]
    periods.append(current_income)
    all_deposit_usd = all_deposit_usd + amount_usd
    return current_income


def update_amount_for_user():
    global user_last_calculation, deposit_btc, deposit_usd, periods, user_acquisition_amount
    while user_last_calculation + 1 < len(periods):
        next_acquisitions = user_last_calculation + 1
        if periods[next_acquisitions][2] == type_acquisitions:
            if deposit_usd >= user_acquisition_amount:
                deposit_usd = deposit_usd - user_acquisition_amount
                deposit_btc = deposit_btc + periods[next_acquisitions][1] * user_acquisition_amount / \
                              periods[next_acquisitions][0]
        if periods[next_acquisitions][2] == type_income_usd:
            if deposit_usd > 0:
                deposit_usd = deposit_usd + periods[next_acquisitions][0] * deposit_usd / \
                              periods[next_acquisitions][1]
        user_last_calculation = user_last_calculation + 1


def current_period():
    return len(periods) - 1


while True:
    print(
        "\n"
        "1 deposit\n"
        "2 withdraw btc\n"
        "3 withdraw $\n"
        "4 acquisition\n"
        "5 set income btc\n"
        "6 set income $\n"
        "7 calculate user balance\n"
        "8 print state\n"
        "9 print log\n"
        "10 exit\n"
    )
    command = int(input("command:"))

    if command == 1:
        print("deposit")
        print_state("before")
        amount = int(input("amount:"))
        update_amount_for_user()
        deposit_usd = deposit_usd + amount
        all_deposit_usd = all_deposit_usd + amount
        add_log("deposit " + str(amount) + "\t" + get_state())
        print_state("after")
    if command == 2:
        print("withdraw btc")
        print_state("before")
        amount = int(input("amount:"))
        update_amount_for_user()
        if deposit_btc >= amount:
            deposit_btc = deposit_btc - amount
            all_deposit_btc = all_deposit_btc - amount
        add_log("withdraw btc " + str(amount) + "\t" + get_state())
        print_state("after")
    if command == 3:
        print("withdraw $")
        print_state("before")
        amount = int(input("amount:"))
        update_amount_for_user()
        if deposit_usd >= amount:
            deposit_usd = deposit_usd - amount
            all_deposit_usd = all_deposit_usd - amount
            add_log("withdraw $ " + str(amount) + "\t" + get_state())
        print_state("after")
    if command == 4:
        print("acquisition")
        amount = acquisition()
        add_log("acquisition " + str(amount) + "\t" + get_state())
    if command == 5:
        print("set income btc")
        print_state("before")
        amount = int(input("amount:"))
        update_amount_for_user()
        income_percent_btc = amount
        all_deposit_btc = all_deposit_btc + all_deposit_btc * income_percent_btc / 100
        add_log("set income btc " + str(amount) + "\t" + get_state())
        print_state("after")
    if command == 6:
        print("set income $")
        print_state("before")
        amount = int(input("amount:"))
        update_amount_for_user()
        add_income_usd(amount)
        add_log("set income $ " + str(amount) + "\t" + get_state())
        print_state("after")
    if command == 7:
        print("calculate user balance")
        print_state("before")
        update_amount_for_user()
        add_log("calculate user balance " + "\t" + get_state())
        print_state("after")
    if command == 8:
        print_state("just print")
    if command == 9:
        print_log()
    if command == 10:
        break
