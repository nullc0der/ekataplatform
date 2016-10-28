import csv


def read_csv():
    f = open('csv_file.csv', 'r')
    r = csv.reader(f)
    emails = set()
    for i in r:
        e = tuple(i)
        print("first_name: %s" % i[0])
        print("last_name: %s" % i[1])
        print("email: %s" % i[2])
        emails.add(e)
    print(emails)
    print(len(emails))
    print(emails[0])


if __name__ == '__main__':
    read_csv()
