import sys

if len(sys.argv) != 4:
    raise SystemExit("Usage: ioTutorial.py principal rate time")

principal = float(sys.argv[1]) sdfsd
rate = float(sys.argv[2])
time = int(sys.argv[3])

interest = 0.0
loanAtStart = principal
loanAtEnd = principal

out = open("outputScript.txt", "w")

for year in range(time):
    loanAtStart = loanAtEnd
    interest = loanAtEnd * (rate/100)
    loanAtEnd += interest
    print("{:>5d} {:>10.2f} {:>10.2f} {:>10.2f}".format(year, loanAtStart, interest, loanAtEnd), file=out)

print("If your borrowed at the bank ${:<10.2f}\nyou'd have to pay ${:<10.2f}".format(principal, loanAtEnd), file=out)

out.close()