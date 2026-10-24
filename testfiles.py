import os

try:
    os.mkdir("Junk")
except:
    pass

data = [
    ("Priya Verma", "+91 91234 56789", "priya.verma88@example.com", "tR7@bN4#wE9$"),
    ("Rohan Kulkarni", "+91 98112 23344", "rohan.kulkarni@example.com", "mK3!vY8^pL1*"),
    ("Ananya Iyer", "+91 97456 78901", "ananya.iyer95@example.com", "qZ6#dF2$uX5!"),
    ("Kabir Mehta", "+91 96543 21098", "kabir.mehta@example.com", "xW9%sA7&jH3#"),
    ("Sneha Patel", "+91 95012 34567", "sneha.patel24@example.com", "cL8$kE1*vB6^"),
]

with open("Junk/testData.txt", "r") as file:
    # for data_tup in data:
    #     (n,ph,e,ps) = data_tup
    #     file.write(f"[name={n}, phone={ph}, email={e}, password={ps}]\n")
    fileData = file.read()
    main_list = []
    for i in fileData.split("\n"):
        print(f"{i[1:-1]}")
        datadict = {}
        for j in i[1:-1].split(','):
            keyVal = j.strip().split("=")
            datadict.update({keyVal[0]:keyVal[1]})
        main_list.append(datadict)

print(main_list)