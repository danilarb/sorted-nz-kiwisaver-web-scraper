# Sorted NZ KiwiSaver final balance calculator

Generates an estimated KiwiSaver balance based on your income and retirement age with all % contribution options.

This program runs on Python 3.11

### Required packages:
- selenium
- bs4
- dotenv

Scrapes https://smartinvestor.sorted.org.nz/kiwisaver-and-managed-funds/ for all NZ KiwiSaver funds and generates a 
`.csv` and `.json` file with each applicable fund formatted as follows:

#### CSV:
```csv
Provider,Fund Name,Fund Link,Fund Category,Fee %,Return % (last 5 years),"Estimated Final Balance (Salary Sacrifice at 3%, Employer Contribution at 3% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 4%, Employer Contribution at 3% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 6%, Employer Contribution at 3% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 8%, Employer Contribution at 3% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 10%, Employer Contribution at 3% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 3%, Employer Contribution at 4% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 4%, Employer Contribution at 4% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 6%, Employer Contribution at 4% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 8%, Employer Contribution at 4% and maximum Government Contribution)","Estimated Final Balance (Salary Sacrifice at 10%, Employer Contribution at 4% and maximum Government Contribution)"
```

#### JSON:
```json
[
    {
        "Provider": "AMP KIWISAVER SCHEME",
        "Fund Name": "AMP CASH FUND",
        "Fund Link": "https://smartinvestor.sorted.org.nz/kiwisaver-and-managed-funds/SCH10367/OFR10393/FND130/",
        "Fund Category": "Defensive",
        "Fee %": 0.9,
        "Return % (last 5 years)": 0.94,
        "Estimated Final Balance (Salary Sacrifice at 3%, Employer Contribution at 3% and maximum Government Contribution)": 155959.67,
        "Estimated Final Balance (Salary Sacrifice at 4%, Employer Contribution at 3% and maximum Government Contribution)": 178104.03,
        "Estimated Final Balance (Salary Sacrifice at 6%, Employer Contribution at 3% and maximum Government Contribution)": 222392.76,
        "Estimated Final Balance (Salary Sacrifice at 8%, Employer Contribution at 3% and maximum Government Contribution)": 266681.49,
        "Estimated Final Balance (Salary Sacrifice at 10%, Employer Contribution at 3% and maximum Government Contribution)": 310970.22,
        "Estimated Final Balance (Salary Sacrifice at 3%, Employer Contribution at 4% and maximum Government Contribution)": 178104.03,
        "Estimated Final Balance (Salary Sacrifice at 4%, Employer Contribution at 4% and maximum Government Contribution)": 200248.4,
        "Estimated Final Balance (Salary Sacrifice at 6%, Employer Contribution at 4% and maximum Government Contribution)": 244537.13,
        "Estimated Final Balance (Salary Sacrifice at 8%, Employer Contribution at 4% and maximum Government Contribution)": 288825.86,
        "Estimated Final Balance (Salary Sacrifice at 10%, Employer Contribution at 4% and maximum Government Contribution)": 333114.59
    }
]
```

### Before running:
Rename `.env.example` to `.env` and fill in each field.

### To run:
Run `main.py`

### TODO:
- Add flat fees to % (such as membership fees)
- Add risk value
